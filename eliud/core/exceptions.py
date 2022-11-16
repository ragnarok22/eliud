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


class ObjectDoesNotExist(Exception):
    """The requested object does not exist"""

    silent_variable_failure = True


class FieldDoesNotExist(Exception):
    """The requested model field does not exist"""
