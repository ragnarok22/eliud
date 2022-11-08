"""Global Eliud exceptions and warning classes"""


class ImproperlyConfigured(Exception):
    """Eliud is somehow improperly configured"""

    pass


class AppRegistryNotReady(Exception):
    """The eliud.apps registry is not populated yet"""

    pass
