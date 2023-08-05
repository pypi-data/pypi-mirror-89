import logging
import numpy as np

from .dist import sample_from


def subspace(num_samples, rng, size=None):
    n = num_samples
    is_scalar = size is None or size == 1

    if is_scalar:
        return (rng.permutation(n) + rng.random(size=n)) / n

    return np.stack([
        (rng.permutation(n) + rng.random(size=n)) / n
        for _ in range(size)],
                    axis=-1)


def subspaces(num_samples, rng, params, update=None):
    if update is None:
        tbl = {}
    else:
        tbl = update

    if isinstance(params, list):
        for param in params:
            tbl[param] = subspace(num_samples, rng)
    elif isinstance(params, dict):
        for param, size in params.items():
            tbl[param] = subspace(num_samples, rng, size)
    else:
        raise ValueError('Invalid value for params')

    return tbl


def param_values(ss_samples, param_dists):
    out = {}

    for param, info in param_dists.items():
        samples = ss_samples[param]
        dist_name = info['function']
        dist_kwargs = info['args']
        out[param] = sample_from(samples, dist_name, dist_kwargs)

    return out


def _shape(param, info):
    if 'shape' not in info:
        return None

    shape = info['shape']
    if isinstance(shape, int):
        return shape
    else:
        msg = 'Invalid prior shape {} for {}'.format(shape, param)
        raise ValueError(msg)


def _check_indep_prior(param, info):
    logger = logging.getLogger(__name__)

    if 'function' not in info:
        raise ValueError('Missing prior function for {}'.format(param))
    elif not isinstance(info['function'], str):
        raise ValueError('Invalid prior function for {}'.format(param))

    if 'args' not in info:
        raise ValueError('Missing prior arguments for {}'.format(param))
    elif not isinstance(info['args'], dict):
        raise ValueError('Invalid prior arguments for {}'.format(param))

    _shape(param, info)

    known_keys = ['function', 'args', 'shape']
    extra_keys = [k for k in info if k not in known_keys]
    if extra_keys:
        logger.warning('Extra prior keys for %s: %s', param, extra_keys)


def _check_dep_prior(param, info):
    logger = logging.getLogger(__name__)

    _shape(param, info)

    known_keys = ['shape']
    extra_keys = [k for k in info if k not in known_keys]
    if extra_keys:
        logger.warning('Extra prior keys for %s: %s', param, extra_keys)


def param_samples(n, indep_priors, dep_priors, rng):
    for (name, info) in indep_priors.items():
        _check_indep_prior(name, info)

    for (name, info) in dep_priors.items():
        _check_dep_prior(name, info)

    indep_params_tbl = {
        param: _shape(param, info)
        for param, info in indep_priors.items()}
    dep_params_tbl = {
        param: _shape(param, info)
        for param, info in dep_priors.items()}

    ss_samples = subspaces(n, rng, indep_params_tbl)
    ss_samples = subspaces(n, rng, dep_params_tbl, update=ss_samples)

    return ss_samples


def _prior_fn(values):
    return lambda: values


class Sampler:
    def __init__(self):
        self.num_samples = 0
        self.indep_params = []
        self.dep_params = []
        self.sample_subspace = {}
        self.sample_values = {}

    def define_scenario(self, scen_data, settings):
        indep = scen_data['model']['priors']
        dep = scen_data['model'].get('dependent_priors', {})
        n = scen_data['parameters']['particles']
        seed = scen_data['parameters']['prng_seed']

        rng = np.random.default_rng(seed)
        ss_samples = param_samples(n, indep, dep, rng)

        self.num_samples = n
        self.indep_params = sorted(list(indep.keys()))
        self.dep_params = sorted(list(dep.keys()))
        self.sample_subspace = ss_samples
        self.sample_values = param_values(ss_samples, indep)

    def update_params(self, scen_data, settings, params):
        # NOTE: we must construct prior functions in a separate function.
        # See https://docs.python.org/3/faq/programming.html for details:
        # Why do lambdas defined in a loop with different values all return
        # the same result?

        # Define the prior functions for the independent parameters.
        for param in self.indep_params:
            values = self.sample_values[param]
            params['model']['prior'][param] = _prior_fn(values)

        if not self.dep_params:
            return

        # Pass the independent parameter values to the model, so that it can
        # define the prior distributions for each dependent parameter.
        dep_dists = settings.model.dependent_dists(params['model']['prior'])

        # Ensure the model has defined the expected distributions.
        expect_dists = set(self.dep_params)
        actual_dists = set(dep_dists.keys())
        if expect_dists != actual_dists:
            raise ValueError('Inconsistent dependent parameters')

        # Draw sample values for each dependent parameter.
        for (param, dist_fn) in dep_dists.items():
            values = dist_fn(self.sample_subspace[param])
            self.sample_values[param] = values
            params['model']['prior'][param] = _prior_fn(values)
