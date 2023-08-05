"""A Latin hypercube sampler for scenario modelling."""

from . import version

__package_name__ = 'lhs'
__author__ = 'Rob Moss'
__email__ = 'rgmoss@unimelb.edu.au'
__copyright__ = '2020, Rob Moss'
__license__ = 'BSD 3-Clause License'
__version__ = version.__version__


from .dist import sample_from
from .sample import Sampler
from .summary import LhsSamples
