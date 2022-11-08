"""Sets up the terminal color scheme."""

import functools
import os
import sys

from eliud.utils import termcolors

try:
    import colorama

    colorama.init()
except (ImportError, OSError):
    HAS_COLORAMA = False
else:
    HAS_COLORAMA = True


def supports_color() -> bool:
    """Return True if the running system's terminal supports color,
    and False otherwise.

    :return: True if the terminal supports color, and False otherwise
    """

    def vt_codes_enabled_in_windows_registry() -> bool:
        """Check the Windows Registry to see if VT code handling has been enabled
        by default, see https://superuser.com/a/1300251/447564.
        """
        try:
            # winreg is only available on Windows.
            import winreg
        except ImportError:
            return False
        else:
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console")
                reg_key_value, _ = winreg.QueryValueEx(reg_key, "VirtualTerminalLevel")
            except FileNotFoundError:
                return False
            else:
                return reg_key_value == 1

    # isatty is not always implemented.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    return is_a_tty and (
        sys.platform != "win32"
        or HAS_COLORAMA
        or "ANSICON" in os.environ
        or  # noqa: W504
        # Windows Terminal supports VT codes.
        "WT_SESSION" in os.environ
        or  # noqa: W504
        # Microsoft Visual Studio Code's built-in terminal supports colors.
        os.environ.get("TERM_PROGRAM") == "vscode"
        or vt_codes_enabled_in_windows_registry()
    )


class Style:
    pass


def make_style(config_string: str = "") -> Style:
    """Create a Style object from the given config_string.

    If config_string is empty eliud.utils.termcolors.DEFAULT_PALETTE is used.
    """

    style = Style()

    color_settings = termcolors.parse_color_setting(config_string)

    # The nocolor palette has all available roles.
    # Use that palette as the basis for populating
    # the palette as defined in the environment.
    for role in termcolors.PALETTES[termcolors.NOCOLOR_PALETTE]:
        if color_settings:
            format = color_settings.get(role, {})
            style_func = termcolors.make_style(**format)
        else:

            def style_func(x):
                return x

        setattr(style, role, style_func)

    return style


@functools.lru_cache(maxsize=None)
def no_style() -> Style:
    """Return s Style object with no color scheme."""
    return make_style("nocolor")


def color_style(force_color=False) -> Style:
    """Return s Style object from the Eliud color scheme."""
    if not force_color and not supports_color():
        return no_style()
    return make_style(os.environ.get("ELIUD_COLORS", ""))
