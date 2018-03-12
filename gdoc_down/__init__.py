import pkg_resources

with open(pkg_resources.resource_filename('gdoc_down', 'VERSION'), 'r') as file:
    __version__ = file.read().strip()
# :obj:`str`: version

# API
from .core import GDocDown