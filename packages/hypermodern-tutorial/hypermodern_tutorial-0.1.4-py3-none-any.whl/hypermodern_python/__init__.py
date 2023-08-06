"""The hypermodern Python project."""
# try:
#     from importlib.metadata import version, PackageNotFoundError  # type: ignore
# except ImportError:  # pragma: no cover
#     from importlib_metadata import version, PackageNotFoundError  # type: ignore


# try:
#     __version__ = version('hypermodern-tutorial')
# except PackageNotFoundError:  # pragma: no cover
#     __version__ = "unknown"

import pkg_resources  # type: ignore
__version__ = pkg_resources.get_distribution('hypermodern-tutorial').version
