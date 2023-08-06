try:
    from .__version__ import version as __version__
except ModuleNotFoundError:
    __version__ = '?.?.?'
    try:
        import setuptools_scm
        __version__ = setuptools_scm.get_version(fallback_version=__version__)
    except LookupError:
        pass


from .store import XoteStore
