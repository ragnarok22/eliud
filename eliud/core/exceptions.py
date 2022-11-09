"""Global Eliud exceptions and warning classes"""


class ImproperlyConfigured(Exception):
    """Eliud is somehow improperly configured"""

    pass


class AppRegistryNotReady(Exception):
    """The eliud.apps registry is not populated yet"""


class SuspiciousOperation(Exception):
    """The user did something suspicious"""


class SuspiciousFileOperation(SuspiciousOperation):
    """A Suspicious filesystem operation was attempted"""
