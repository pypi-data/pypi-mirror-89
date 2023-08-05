
import numpy as np
from replay_trajectory_classification.bins import atleast_2d


def fit_occupancy(position, place_bin_centers, model,
                  model_kwargs, is_track_interior):
    '''

    Parameters
    ----------
    position : ndarray, shape (n_time, n_position_dims)
    place_bin_centers : ndarray, shape (n_bins, n_position_dims)
    model : model class
    model_kwargs : dict
    is_track_interior : ndarray, shape (n_bins,)

    Returns
    -------
    occupancy : ndarray, shape (n_bins,)
    occupancy_model : model class instance

    '''
    not_nan_position = np.all(~np.isnan(atleast_2d(position)), axis=1)
    occupancy_model = model(
        **model_kwargs).fit(atleast_2d(position[not_nan_position]))
    occupancy = np.zeros((place_bin_centers.shape[0],))
    occupancy[is_track_interior] = np.exp(occupancy_model.score_samples(
        atleast_2d(place_bin_centers[is_track_interior])))
    return occupancy, occupancy_model


def fit_marginal_model(multiunit, position, place_bin_centers,
                       model, model_kwargs, is_track_interior):
    '''

    Parameters
    ----------
    multiunit : ndarray, shape (n_time, n_features)
    position : ndarray, shape (n_time, n_position_dims)
    place_bin_centers : ndarray, shape (n_bins, n_position_dims)
    model : class
    model_kwargs : dict
    is_track_interior : ndarray, shape (n_bins,)

    Returns
    -------
    marginal_density : ndarray, shape (n_bins,)

    '''
    is_spike = np.any(~np.isnan(multiunit), axis=1)
    marginal_density = np.zeros((place_bin_centers.shape[0],))
    if is_spike.sum() > 0:
        not_nan_position = np.all(~np.isnan(atleast_2d(position)), axis=1)
        marginal_model = (model(**model_kwargs)
                          .fit(atleast_2d(position)[is_spike &
                                                    not_nan_position]))

        marginal_density[is_track_interior] = np.exp(
            marginal_model.score_samples(
                atleast_2d(place_bin_centers[is_track_interior])))
    return marginal_density


def train_joint_model(multiunit, position, model, model_kwargs):
    '''Fits a density model to the joint pdf of position and mark.

    Parameters
    ----------
    multiunit : ndarray, shape (n_time, n_features)
    position : ndarray, shape (n_time, n_position_dims)
    model : model class
    model_kwargs : dict

    Returns
    -------
    fitted_joint_model : model class instance

    '''
    multiunit, position = atleast_2d(multiunit), atleast_2d(position)
    is_spike = (np.any(~np.isnan(multiunit), axis=1) &
                np.all(~np.isnan(position), axis=1))
    not_nan_marks = np.any(~np.isnan(multiunit), axis=0)

    return (model(**model_kwargs)
            .fit(np.concatenate((multiunit[is_spike][:, not_nan_marks],
                                 position[is_spike]), axis=1)))


def estimate_mean_rate(multiunit):
    '''

    Parameters
    ----------
    multiunit : ndarray, shape (n_time, n_features)

    Returns
    -------
    mean_rate : float

    '''
    is_spike = np.any(~np.isnan(multiunit), axis=1)
    return is_spike.mean()


def estimate_intensity(density, occupancy, mean_rate):
    '''

    Parameters
    ----------
    density : ndarray, shape (n_bins,)
    occupancy : ndarray, shape (n_bins,)
    mean_rate : float

    Returns
    -------
    intensity : ndarray, shape (n_bins,)

    '''
    return np.exp(np.log(mean_rate) + np.log(density) - np.log(occupancy))


def estimate_ground_process_intensity(multiunit, position, place_bin_centers,
                                      occupancy, mean_rate, model,
                                      model_kwargs, is_track_interior):
    '''

    Parameters
    ----------
    multiunit : ndarray, shape (n_time, n_marks)
    position : ndarray, shape (n_time, n_position_dims)
    place_bin_centers : ndarray, (n_bins, n_position_dims)
    occupancy : ndarray, (n_bins, n_position_dims)
    mean_rate : float
    model : sklearn model
    model_kwargs : dict
    is_track_interior : ndarray, shape (n_bins,)

    Returns
    -------
    ground_process_intensity : ndarray, shape (1, n_bins)

    '''
    marginal_pdf = fit_marginal_model(
        multiunit, position, place_bin_centers, model, model_kwargs,
        is_track_interior)
    ground_process_intensity = np.zeros((1, place_bin_centers.shape[0],))
    ground_process_intensity[:, is_track_interior] = estimate_intensity(
        marginal_pdf[is_track_interior], occupancy[is_track_interior],
        mean_rate)
    return ground_process_intensity


def estimate_joint_mark_intensity(
        multiunit, place_bin_centers, occupancy, joint_model, mean_rate,
        is_track_interior):
    '''

    Parameters
    ----------
    multiunit : ndarray, shape (n_time, n_marks)
    place_bin_centers : ndarray, (n_bins, n_position_dims)
    occupancy : ndarray, (n_bins, n_position_dims)
    joint_model : sklearn model
    mean_rate : float
    is_track_interior : ndarray, shape (n_bins,)

    Returns
    -------
    joint_mark_intensity : ndarray, shape (n_time, n_bins)

    '''
    multiunit = np.atleast_2d(multiunit)
    n_bins = place_bin_centers.shape[0]
    n_time = multiunit.shape[0]
    is_nan = np.any(np.isnan(multiunit), axis=1)
    n_spikes = np.sum(~is_nan)
    joint_mark_intensity = np.ones((n_time, n_bins))
    interior_bin_inds = np.nonzero(is_track_interior)[0]

    if n_spikes > 0:
        zipped = zip(interior_bin_inds, place_bin_centers[interior_bin_inds],
                     occupancy[interior_bin_inds])
        for bin_ind, bin, bin_occupancy in zipped:
            joint_mark_intensity[~is_nan, bin_ind] = estimate_intensity(
                np.exp(joint_model.score_samples(
                    np.concatenate((multiunit[~is_nan],
                                    bin * np.ones((n_spikes, 1))), axis=1))),
                bin_occupancy, mean_rate)

    return joint_mark_intensity


def poisson_mark_log_likelihood(joint_mark_intensity,
                                ground_process_intensity,
                                time_bin_size=1):
    '''Probability of parameters given spiking indicator at a particular
    time and associated marks.

    Parameters
    ----------
    joint_mark_intensity : ndarray, shape (n_time, n_bins)
    ground_process_intensity : ndarray, shape (1, n_bins)
    time_bin_size : int, optional

    Returns
    -------
    poisson_mark_log_likelihood : ndarray, shape (n_time, n_bins)

    '''
    return np.log(joint_mark_intensity + np.spacing(1)) - (
        (ground_process_intensity + np.spacing(1)) * time_bin_size)


def fit_multiunit_likelihood(position, multiunits, place_bin_centers,
                             model, model_kwargs, occupancy_model,
                             occupancy_kwargs, is_track_interior=None):
    '''

    Parameters
    ----------
    position : ndarray, shape (n_time, n_position_dims)
    multiunits : ndarray, shape (n_time, n_marks, n_electrodes)
    place_bin_centers : ndarray, shape ( n_bins, n_position_dims)
    model : sklearn model
    model_kwargs : dict
    occupancy_model : sklearn model
    occupancy_kwargs : dict
    is_track_interior : None or ndarray, shape (n_bins,)

    Returns
    -------
    joint_pdf_models : list of sklearn models, shape (n_electrodes,)
    ground_process_intensities : list of ndarray, shape (n_electrodes,)
    occupancy : ndarray, (n_bins, n_position_dims)
    mean_rates : ndarray, (n_electrodes,)

    '''

    if is_track_interior is None:
        is_track_interior = np.ones((place_bin_centers.shape[0],),
                                    dtype=np.bool)
    occupancy, _ = fit_occupancy(position, place_bin_centers, occupancy_model,
                                 occupancy_kwargs, is_track_interior)
    mean_rates = []
    ground_process_intensities = []
    joint_pdf_models = []

    for multiunit in np.moveaxis(multiunits, -1, 0):
        mean_rates.append(estimate_mean_rate(multiunit))
        ground_process_intensities.append(
            estimate_ground_process_intensity(
                multiunit, position, place_bin_centers, occupancy,
                mean_rates[-1], model, model_kwargs, is_track_interior))
        joint_pdf_models.append(
            train_joint_model(multiunit, position, model, model_kwargs))

    return joint_pdf_models, ground_process_intensities, occupancy, mean_rates


def estimate_multiunit_likelihood(multiunits, place_bin_centers,
                                  joint_pdf_models,
                                  ground_process_intensities, occupancy,
                                  mean_rates, is_track_interior=None):
    '''

    Parameters
    ----------
    multiunits : ndarray, shape (n_time, n_marks, n_electrodes)
    place_bin_centers : ndarray, (n_bins, n_position_dims)
    joint_pdf_models : list of sklearn models, shape (n_electrodes,)
    ground_process_intensities : list of ndarray, shape (n_electrodes,)
    occupancy : ndarray, (n_bins, n_position_dims)
    mean_rates : ndarray, (n_electrodes,)

    Returns
    -------
    log_likelihood : (n_time, n_bins)

    '''
    if is_track_interior is None:
        is_track_interior = np.ones((place_bin_centers.shape[0],),
                                    dtype=np.bool)

    n_bin = place_bin_centers.shape[0]
    n_time = multiunits.shape[0]
    log_likelihood = np.zeros((n_time, n_bin))

    zipped = zip(np.moveaxis(multiunits, -1, 0), joint_pdf_models,
                 mean_rates, ground_process_intensities)
    for multiunit, joint_model, mean_rate, ground_process_intensity in zipped:
        joint_mark_intensity = estimate_joint_mark_intensity(
            multiunit, place_bin_centers, occupancy, joint_model, mean_rate,
            is_track_interior)
        log_likelihood += poisson_mark_log_likelihood(
            joint_mark_intensity, np.atleast_2d(ground_process_intensity))

    mask = np.ones_like(is_track_interior, dtype=np.float)
    mask[~is_track_interior] = np.nan

    return log_likelihood * mask
