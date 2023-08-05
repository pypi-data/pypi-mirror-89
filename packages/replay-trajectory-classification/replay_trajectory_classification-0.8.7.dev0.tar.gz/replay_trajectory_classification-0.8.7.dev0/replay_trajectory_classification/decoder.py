from copy import deepcopy
from logging import getLogger

import joblib
import numpy as np
import sklearn
import xarray as xr
from replay_trajectory_classification.bins import (atleast_2d, get_centers,
                                                   get_grid, get_track_grid,
                                                   get_track_interior)
from replay_trajectory_classification.core import (_acausal_decode,
                                                   _causal_decode, mask,
                                                   scaled_likelihood)
from replay_trajectory_classification.initial_conditions import \
    uniform_on_track
from replay_trajectory_classification.misc import NumbaKDE
from replay_trajectory_classification.multiunit_likelihood import (
    estimate_multiunit_likelihood, fit_multiunit_likelihood)
from replay_trajectory_classification.spiking_likelihood import (
    estimate_place_fields, estimate_spiking_likelihood)
from replay_trajectory_classification.state_transition import \
    CONTINUOUS_TRANSITIONS
from sklearn.base import BaseEstimator

logger = getLogger(__name__)

sklearn.set_config(print_changed_only=False)

_DEFAULT_CLUSTERLESS_MODEL_KWARGS = dict(
    bandwidth=np.array([24.0, 24.0, 24.0, 24.0, 6.0, 6.0]))
_DEFAULT_TRANSITIONS = ['random_walk', 'uniform', 'identity']


class _DecoderBase(BaseEstimator):
    def __init__(self, place_bin_size=2.0, replay_speed=40, movement_var=0.05,
                 position_range=None, transition_type='random_walk',
                 initial_conditions_type='uniform_on_track',
                 infer_track_interior=True):
        self.place_bin_size = place_bin_size
        self.replay_speed = replay_speed
        self.movement_var = movement_var
        self.position_range = position_range
        self.transition_type = transition_type
        self.initial_conditions_type = initial_conditions_type
        self.infer_track_interior = infer_track_interior

        if 2 * np.sqrt(replay_speed * movement_var) < place_bin_size:
            logger.warning('Place bin size is too small for a random walk '
                           'continuous state transition')

    def fit_place_grid(self, position, track_graph=None,
                       edge_order=None, edge_spacing=15,
                       infer_track_interior=True, is_track_interior=None):
        if track_graph is None:
            (self.edges_, self.place_bin_edges_, self.place_bin_centers_,
             self.centers_shape_) = get_grid(
                position, self.place_bin_size, self.position_range,
                self.infer_track_interior)
            self.infer_track_interior = infer_track_interior

            if is_track_interior is None and self.infer_track_interior:
                self.is_track_interior_ = get_track_interior(
                    position, self.edges_)
            elif is_track_interior is None and not self.infer_track_interior:
                self.is_track_interior_ = np.ones(
                    self.centers_shape_, dtype=np.bool)
        else:
            (
                self.place_bin_centers_,
                self.place_bin_edges_,
                self.is_track_interior_,
                self.distance_between_nodes_,
                self.centers_shape_,
                self.edges_,
                self.track_graph_with_bin_centers_edges_,
                self.original_nodes_df_,
                self.place_bin_edges_nodes_df_,
                self.place_bin_centers_nodes_df_,
                self.nodes_df_
            ) = get_track_grid(track_graph, edge_order,
                               edge_spacing, self.place_bin_size)

    def fit_initial_conditions(self, position=None):
        logger.info('Fitting initial conditions...')
        self.initial_conditions_ = uniform_on_track(self.place_bin_centers_,
                                                    self.is_track_interior_)

    def fit_state_transition(
            self, position, is_training=None, replay_speed=None,
            transition_type='random_walk'):
        logger.info('Fitting state transition...')
        if is_training is None:
            is_training = np.ones((position.shape[0],), dtype=np.bool)
        is_training = np.asarray(is_training).squeeze()
        if replay_speed is not None:
            self.replay_speed = replay_speed
        self.transition_type = transition_type

        try:
            self.state_transition_ = CONTINUOUS_TRANSITIONS[transition_type](
                self.place_bin_centers_, self.is_track_interior_,
                position, self.edges_, is_training, self.replay_speed,
                self.position_range, self.movement_var,
                np.asarray(self.place_bin_centers_nodes_df_.node_id),
                self.distance_between_nodes_)
        except AttributeError:
            self.state_transition_ = CONTINUOUS_TRANSITIONS[transition_type](
                self.place_bin_centers_, self.is_track_interior_,
                position, self.edges_, is_training, self.replay_speed,
                self.position_range, self.movement_var,
                None, None)

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def save_model(self, filename='model.pkl'):
        joblib.dump(self, filename)

    @staticmethod
    def load_model(filename='model.pkl'):
        return joblib.load(filename)

    def copy(self):
        return deepcopy(self)

    def convert_results_to_xarray(self, results, time):
        n_position_dims = self.place_bin_centers_.shape[1]
        n_time = time.shape[0]

        if n_position_dims > 1:
            dims = ['time', 'x_position', 'y_position']
            coords = dict(
                time=time,
                x_position=get_centers(self.edges_[0]),
                y_position=get_centers(self.edges_[1]),
            )
        else:
            dims = ['time', 'position']
            coords = dict(
                time=time,
                position=get_centers(self.edges_[0]),
            )
        new_shape = (n_time, *self.centers_shape_)
        try:
            results = xr.Dataset(
                {key: (dims, mask(value,
                                  self.is_track_interior_.ravel(order='F'))
                       .reshape(new_shape).swapaxes(-1, -2))
                 for key, value in results.items()},
                coords=coords)
        except ValueError:
            results = xr.Dataset(
                {key: (dims, mask(value,
                                  self.is_track_interior_.ravel(order='F'))
                       .reshape(new_shape))
                 for key, value in results.items()},
                coords=coords)

        return results


class SortedSpikesDecoder(_DecoderBase):
    def __init__(self, place_bin_size=2.0, replay_speed=40, movement_var=0.05,
                 position_range=None, knot_spacing=10,
                 spike_model_penalty=1E1,
                 transition_type='random_walk',
                 initial_conditions_type='uniform_on_track',
                 infer_track_interior=True):
        '''

        Attributes
        ----------
        place_bin_size : float, optional
            Approximate size of the position bins.
        replay_speed : int, optional
            How many times faster the replay movement is than normal movement.
        movement_var : float, optional
            How far the animal is can move in one time bin during normal
            movement.
        position_range : sequence, optional
            A sequence of `n_position_dims`, each an optional (lower, upper)
            tuple giving the outer bin edges for position.
            An entry of None in the sequence results in the minimum and maximum
            values being used for the corresponding dimension.
            The default, None, is equivalent to passing a tuple of
            `n_position_dims` None values.
        knot_spacing : float, optional
        spike_model_penalty : float, optional
        transition_type : ('empirical_movement' | 'random_walk' |
                           'uniform', 'identity')
        initial_conditions_type : ('uniform' | 'uniform_on_track')
        infer_track_interior : bool, optional

        '''
        super().__init__(place_bin_size, replay_speed, movement_var,
                         position_range, transition_type,
                         initial_conditions_type, infer_track_interior)
        self.knot_spacing = knot_spacing
        self.spike_model_penalty = spike_model_penalty

    def fit_place_fields(self, position, spikes, is_training=None):
        logger.info('Fitting place fields...')
        if is_training is None:
            is_training = np.ones((position.shape[0],), dtype=np.bool)
        is_training = np.asarray(is_training).squeeze()
        self.place_fields_ = estimate_place_fields(
            position[is_training], spikes[is_training],
            self.place_bin_centers_, penalty=self.spike_model_penalty,
            knot_spacing=self.knot_spacing)

    def plot_place_fields(self, sampling_frequency=1, col_wrap=5):
        '''Plots the fitted 2D place fields for each neuron.

        Parameters
        ----------
        sampling_frequency : float, optional
        col_wrap : int, optional

        Returns
        -------
        g : xr.plot.FacetGrid instance

        '''
        try:
            g = (self.place_fields_.unstack('position') * sampling_frequency
                 ).plot(x='x_position', y='y_position', col='neuron',
                        hue='encoding_group', col_wrap=col_wrap)
        except ValueError:
            g = (self.place_fields_ * sampling_frequency).plot(
                x='position', col='neuron', hue='encoding_group',
                col_wrap=col_wrap)

        return g

    def fit(self, position, spikes, is_training=None, is_track_interior=None,
            track_graph=None, edge_order=None,
            edge_spacing=15):
        '''

        Parameters
        ----------
        position : ndarray, shape (n_time, n_position_dims)
        spikes : ndarray, shape (n_time, n_neurons)
        is_training : None or bool ndarray, shape (n_time), optional
            Time bins to be used for encoding.
        is_track_interior : None or bool ndaarray, shape (n_x_bins, n_y_bins)
        track_graph : networkx.Graph
        edge_order : array_like
        edge_spacing : None, float or array_like

        Returns
        -------
        self

        '''
        position = atleast_2d(np.asarray(position))
        spikes = np.asarray(spikes)
        self.fit_place_grid(position, track_graph,
                            edge_order, edge_spacing,
                            self.infer_track_interior, is_track_interior)
        self.fit_initial_conditions(position)
        self.fit_state_transition(
            position, is_training, transition_type=self.transition_type)
        self.fit_place_fields(position, spikes, is_training)

        return self

    def predict(self, spikes, time=None, is_compute_acausal=True):
        '''

        Parameters
        ----------
        spikes : ndarray, shape (n_time, n_neurons)
        time : ndarray or None, shape (n_time,), optional
        is_compute_acausal : bool, optional

        Returns
        -------
        results : xarray.Dataset

        '''
        spikes = np.asarray(spikes)

        results = {}
        results['likelihood'] = scaled_likelihood(
            estimate_spiking_likelihood(
                spikes, np.asarray(self.place_fields_)))
        results['causal_posterior'] = _causal_decode(
            self.initial_conditions_, self.state_transition_,
            results['likelihood'])

        if is_compute_acausal:
            results['acausal_posterior'] = (
                _acausal_decode(results['causal_posterior'][..., np.newaxis],
                                self.state_transition_))

        n_time = spikes.shape[0]
        if time is None:
            time = np.arange(n_time)

        return self.convert_results_to_xarray(results, time)


class ClusterlessDecoder(_DecoderBase):
    '''

    Attributes
    ----------
    place_bin_size : float, optional
        Approximate size of the position bins.
    replay_speed : int, optional
        How many times faster the replay movement is than normal movement.
    movement_var : float, optional
        How far the animal is can move in one time bin during normal
        movement.
    position_range : sequence, optional
        A sequence of `n_position_dims`, each an optional (lower, upper)
        tuple giving the outer bin edges for position.
        An entry of None in the sequence results in the minimum and maximum
        values being used for the corresponding dimension.
        The default, None, is equivalent to passing a tuple of
        `n_position_dims` None values.
    model : scikit-learn density estimator, optional
    model_kwargs : dict, optional
    occupancy_model : scikit-learn density estimator, optional
    occupancy_kwargs : dict, optional
    transition_type : ('empirical_movement' | 'random_walk' |
                       'uniform', 'identity')
    initial_conditions_type : ('uniform' | 'uniform_on_track')

    '''

    def __init__(self, place_bin_size=2.0, replay_speed=40, movement_var=0.05,
                 position_range=None, model=NumbaKDE,
                 model_kwargs=_DEFAULT_CLUSTERLESS_MODEL_KWARGS,
                 occupancy_model=None, occupancy_kwargs=None,
                 transition_type='random_walk',
                 initial_conditions_type='uniform_on_track',
                 infer_track_interior=True):
        super().__init__(place_bin_size, replay_speed, movement_var,
                         position_range, transition_type,
                         initial_conditions_type, infer_track_interior)
        self.model = model
        self.model_kwargs = model_kwargs
        if occupancy_model is None:
            self.occupancy_model = model
            self.occupancy_kwargs = model_kwargs
        else:
            self.occupancy_model = occupancy_model
            self.occupancy_kwargs = occupancy_kwargs

    def fit_multiunits(self, position, multiunits, is_training=None):
        '''

        Parameters
        ----------
        position : array_like, shape (n_time, n_position_dims)
        multiunits : array_like, shape (n_time, n_marks, n_electrodes)
        is_training : None or array_like, shape (n_time,)

        '''
        logger.info('Fitting multiunits...')
        if is_training is None:
            is_training = np.ones((position.shape[0],), dtype=np.bool)
        is_training = np.asarray(is_training).squeeze()

        (self.joint_pdf_models_, self.ground_process_intensities_,
         self.occupancy_, self.mean_rates_) = fit_multiunit_likelihood(
            position[is_training], multiunits[is_training],
            self.place_bin_centers_, self.model, self.model_kwargs,
            self.occupancy_model, self.occupancy_kwargs,
            self.is_track_interior_.ravel(order='F'))

    def fit(self, position, multiunits, is_training=None,
            is_track_interior=None, track_graph=None,
            edge_order=None, edge_spacing=15):
        '''

        Parameters
        ----------
        position : array_like, shape (n_time, n_position_dims)
        multiunits : array_like, shape (n_time, n_marks, n_electrodes)
        is_training : None or array_like, shape (n_time,)
        is_track_interior : None or ndarray, shape (n_x_bins, n_y_bins)
        track_graph : networkx.Graph
        edge_order : array_like
        edge_spacing : None, float or array_like

        Returns
        -------
        self

        '''
        position = atleast_2d(np.asarray(position))
        multiunits = np.asarray(multiunits)

        self.fit_place_grid(position, track_graph,
                            edge_order, edge_spacing,
                            self.infer_track_interior, is_track_interior)
        self.fit_initial_conditions(position)
        self.fit_state_transition(
            position, is_training, transition_type=self.transition_type)
        self.fit_multiunits(position, multiunits, is_training)

        return self

    def predict(self, multiunits, time=None, is_compute_acausal=True):
        '''

        Parameters
        ----------
        multiunits : array_like, shape (n_time, n_marks, n_electrodes)
        time : None or ndarray, shape (n_time,)
        is_compute_acausal : bool, optional
            Use future information to compute the posterior.

        Returns
        -------
        results : xarray.Dataset

        '''
        multiunits = np.asarray(multiunits)

        results = {}
        results['likelihood'] = scaled_likelihood(
            estimate_multiunit_likelihood(
                multiunits, self.place_bin_centers_,
                self.joint_pdf_models_, self.ground_process_intensities_,
                self.occupancy_, self.mean_rates_,
                self.is_track_interior_.ravel(order='F')))
        results['causal_posterior'] = _causal_decode(
            self.initial_conditions_, self.state_transition_,
            results['likelihood'])

        if is_compute_acausal:
            results['acausal_posterior'] = (
                _acausal_decode(results['causal_posterior'][..., np.newaxis],
                                self.state_transition_))

        n_time = multiunits.shape[0]
        if time is None:
            time = np.arange(n_time)

        return self.convert_results_to_xarray(results, time)
