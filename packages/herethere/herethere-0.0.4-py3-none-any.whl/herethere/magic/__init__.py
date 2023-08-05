"""herethere.magic"""
from herethere.here.magic import MagicHere
from herethere.there.magic import MagicThere


def load_ipython_extension(ipython):
    """Hook for `%load_extension` IPython command."""
    ipython.register_magics(MagicHere(ipython))
    ipython.register_magics(MagicThere(ipython))
