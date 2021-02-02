import os
import platform
from enum import Enum


from PyQt5.QtWidgets import QApplication


THEMES_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "themes")
LIGHT_STYLE_SHEET = os.path.join(THEMES_PATH, "light.qss")
DARK_STYLE_SHEET = os.path.join(THEMES_PATH, "dark.qss")


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"
    DEFAULT = LIGHT


def get_theme() -> Theme:
    if platform.system() == "Windows":
        return get_theme_windows()
    elif platform.system() == "Linux":
        return get_theme_linux()
    else:
        return Theme.DEFAULT


def get_theme_windows() -> Theme:
    import winreg

    # noinspection PyBroadException
    try:
        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(key=winreg.HKEY_CURRENT_USER, sub_key=sub_key) as registry_key:
            value, type_id = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
        if value == 0:
            return Theme.DARK
        else:
            return Theme.LIGHT
    except Exception:
        return Theme.DEFAULT


def get_theme_linux() -> Theme:
    return Theme.DEFAULT


def get_stylesheet(theme: Theme) -> str:
    if theme == Theme.LIGHT:
        return LIGHT_STYLE_SHEET
    elif theme == Theme.DARK:
        return DARK_STYLE_SHEET
    else:
        return get_stylesheet(Theme.DEFAULT)
