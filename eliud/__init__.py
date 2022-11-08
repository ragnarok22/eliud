from eliud.utils.version import get_version

VERSION = (0, 1, 0, "alpha", 0)
__version__ = get_version(VERSION)


def setup():
    """
    Configure the settings (this happens as a side effect of accessing the
    first setting), configure logging and populate the app registry.
    """
    from eliud.apps import apps
    from eliud.conf import settings
    from eliud.utils.log import configure_logging

    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    apps.populate(settings.INSTALLED_APPS)
