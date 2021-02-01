import os


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESOURCES_DIR = os.path.join(PROJECT_DIR, "resources")


def get_icon():
    if os.name == "nt":
        return os.path.join(RESOURCES_DIR, "icon.ico")
    else:
        return os.path.join(RESOURCES_DIR, "icon.png")


ICON_FILE = get_icon()


