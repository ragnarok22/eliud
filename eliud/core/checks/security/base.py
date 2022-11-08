from eliud.conf import settings
from eliud.core.exceptions import ImproperlyConfigured

from .. import Tags, Warning, register

SECRET_KEY_INSECURE_PREFIX = "eliud-insecure-"
SECRET_KEY_MIN_LENGTH = 50
SECRET_KEY_MIN_UNIQUE_CHARACTERS = 5

SECRET_KEY_WARNING_MSG = (
    f"Your %s has less than {SECRET_KEY_MIN_LENGTH} characters, less than "
    f"{SECRET_KEY_MIN_UNIQUE_CHARACTERS} unique characters, or it's prefixed "
    f"with '{SECRET_KEY_INSECURE_PREFIX}' indicating that it was generated "
    f"automatically by Eliud. Please generate a long and random value, "
    f"otherwise many of Eliud's security-critical features will be "
    f"vulnerable to attack."
)

W009 = Warning(
    SECRET_KEY_WARNING_MSG % "SECRET_KEY",
    id="security.W009",
)

W018 = Warning(
    "You should not have DEBUG set to True in deployment.",
    id="security.W018",
)

W025 = Warning(SECRET_KEY_WARNING_MSG, id="security.W025")


def _security_middleware():
    return "eliud.middleware.security.SecurityMiddleware" in settings.MIDDLEWARE


def _check_secret_key(secret_key):
    return (
        len(set(secret_key)) >= SECRET_KEY_MIN_UNIQUE_CHARACTERS
        and len(secret_key) >= SECRET_KEY_MIN_LENGTH
        and not secret_key.startswith(SECRET_KEY_INSECURE_PREFIX)
    )


@register(Tags.security, deploy=True)
def check_secret_key(app_configs, **kwargs):
    try:
        secret_key = settings.SECRET_KEY
    except (ImproperlyConfigured, AttributeError):
        passed_check = False
    else:
        passed_check = _check_secret_key(secret_key)
    return [] if passed_check else [W009]


@register(Tags.security, deploy=True)
def check_secret_key_fallbacks(app_configs, **kwargs):
    warnings = []
    try:
        fallbacks = settings.SECRET_KEY_FALLBACKS
    except (ImproperlyConfigured, AttributeError):
        warnings.append(Warning(W025.msg % "SECRET_KEY_FALLBACKS", id=W025.id))
    else:
        for index, key in enumerate(fallbacks):
            if not _check_secret_key(key):
                warnings.append(
                    Warning(W025.msg % f"SECRET_KEY_FALLBACKS[{index}]", id=W025.id)
                )
    return warnings


@register(Tags.security, deploy=True)
def check_debug(app_configs, **kwargs):
    passed_check = not settings.DEBUG
    return [] if passed_check else [W018]
