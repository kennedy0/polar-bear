import copy
import json
import os
import platform
import shutil
from typing import List


APP_NAME = "PolarBear"
CONFIG_PATH = os.path.join(
    os.path.expanduser("~"),
    ".config",
    APP_NAME.replace(' ', '_'))
CONFIG_FILE = os.path.join(CONFIG_PATH, f"{APP_NAME.replace(' ', '_')}.config")


def get_presets_src():
    if platform.system() == "Windows":
        return os.path.join(os.path.dirname(__file__), "presets", "windows")
    elif platform.system() == "Linux":
        return os.path.join(os.path.dirname(__file__), "presets", "linux")
    else:
        raise NotImplementedError(f"Platform not supported: {platform.system()}")


PRESETS_PATH = os.path.join(CONFIG_PATH, "presets")
PRESETS_SRC = get_presets_src()

LOG_PATH = os.path.join(CONFIG_PATH, "logs")


default_settings = {
    'preset': None,
    'default_save_path': os.path.join(os.path.expanduser("~"), "Desktop"),
    'default_fps': 60,
    'default_width': 800,
    'default_height': 600,
}


def load_config() -> dict:
    """ Load config dict from file. """
    if not os.path.isfile(CONFIG_FILE):
        create_config_file()

    if not os.path.isdir(PRESETS_PATH):
        reset_presets()

    with open(CONFIG_FILE, 'r') as fp:
        config = json.load(fp)

    # If the config is missing any default values, add them.
    for key, value in default_settings.items():
        if key not in config.keys():
            config.update({key: value})

    return config


def save_config(config: dict):
    """ Save config dict to file. """
    try:
        os.makedirs(CONFIG_PATH)
    except OSError:
        pass

    with open(CONFIG_FILE, 'w') as fp:
        fp.write(json.dumps(config, indent=4))


def create_config_file():
    save_config(config=copy.deepcopy(default_settings))


def reset_presets():
    try:
        shutil.rmtree(PRESETS_PATH)
    except OSError:
        pass

    shutil.copytree(PRESETS_SRC, PRESETS_PATH)


def get_preset_files() -> List[str]:
    return [os.path.join(PRESETS_PATH, file) for file in os.listdir(PRESETS_PATH)]


def get_preset_names() -> List[str]:
    return [preset_name_from_file(file) for file in get_preset_files()]


def preset_name_from_file(file: str) -> str:
    return os.path.splitext(os.path.basename(file))[0]


def file_from_preset_name(preset: str) -> str:
    return os.path.join(PRESETS_PATH, f"{preset}.txt")
