import os
import platform


THEMES_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "themes")
LIGHT_STYLE_SHEET = os.path.join(THEMES_PATH, "light.qss")
DARK_STYLE_SHEET = os.path.join(THEMES_PATH, "dark.qss")


THEME_LIGHT = "light"
THEME_DARK = "dark"
THEME_SYSTEM = "system"


def get_theme() -> str:
    if platform.system() == "Windows":
        return get_theme_windows()
    elif platform.system() == "Linux":
        return get_theme_linux()
    else:
        return THEME_LIGHT


def get_theme_windows() -> str:
    import winreg

    # noinspection PyBroadException
    try:
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(key=winreg.HKEY_CURRENT_USER, sub_key=sub_key) as registry_key:
            value, type_id = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
        if value == 0:
            return THEME_DARK
        else:
            return THEME_LIGHT
    except Exception:
        return THEME_LIGHT


def get_theme_linux() -> str:
    return THEME_LIGHT


def get_stylesheet(theme: str) -> str:
    if theme == THEME_SYSTEM:
        # Get theme dynamically from system settings
        theme = get_theme()

    if theme == THEME_LIGHT:
        return LIGHT_STYLE_SHEET
    elif theme == THEME_DARK:
        return DARK_STYLE_SHEET
    else:
        # Default to light
        return LIGHT_STYLE_SHEET
