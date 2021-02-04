import copy
import os

from PyQt5 import QtCore, QtWidgets

from config import ffmpeg_version
from config import settings
from config.theme import THEME_SYSTEM, THEME_LIGHT, THEME_DARK, get_stylesheet
from gui.options import Ui_Options


class OptionsWindow(Ui_Options, QtWidgets.QDialog):
    def __init__(self, parent, config: dict):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.config = copy.deepcopy(config)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self._init_callbacks()
        self.update_widgets()

    def _init_callbacks(self):
        self.btn_open_presets.clicked.connect(self.on_open_presets_clicked)
        self.btn_refresh_presets.clicked.connect(self.on_refresh_presets)
        self.btn_help.clicked.connect(self.on_help_clicked)
        self.btn_open_folder.clicked.connect(self.on_browse_folder)
        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.on_cancel_clicked)
        self.btn_reset.clicked.connect(self.on_reset_clicked)

        self.combo_preset.currentIndexChanged.connect(self.on_select_preset)
        self.spin_fps.valueChanged.connect(self.on_change_fps)
        self.spin_width.valueChanged.connect(self.on_change_width)
        self.spin_height.valueChanged.connect(self.on_change_height)

        self.btn_theme_system_default.clicked.connect(self.on_set_theme_system)
        self.btn_theme_light.clicked.connect(self.on_set_theme_light)
        self.btn_theme_dark.clicked.connect(self.on_set_theme_dark)

        self.btn_ffmpeg_system.clicked.connect(self.on_use_system_ffmpeg)
        self.btn_ffmpeg_bundled.clicked.connect(self.on_use_bundled_ffmpeg)
        self.btn_ffmpeg_help.clicked.connect(self.on_ffmpeg_help_clicked)

    @staticmethod
    def on_open_presets_clicked():
        os.startfile(settings.PRESETS_PATH)

    def on_refresh_presets(self):
        self.update_preset_widget()

    def on_help_clicked(self):
        msg = [
            "Presets are .txt files that store an FFmpeg command. "
            "The following variables must be present:",
            "", "",
            "<FFMPEG> Path to the ffmpeg binary",
            "<FPS> Frames per second",
            "<X> Region x-offset",
            "<Y> Region y-offset",
            "<SIZE> Video resolution",
            "<OUTPUT> Output file, not including extension",
        ]
        QtWidgets.QMessageBox.information(self, "FFmpeg Command", "\n".join(msg))

    def on_browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="choose folder",
            directory=self.line_edit_save_path.text(),
        )

        if folder == "":
            return

        self.config['default_save_path'] = folder
        self.update_widgets()

    def on_ok_clicked(self):
        self.force_config_update()
        self.accept()

    def on_cancel_clicked(self):
        self.reject()

    def on_reset_clicked(self):
        result = QtWidgets.QMessageBox.question(
            self,
            "Reset",
            "This will reset all settings and clear all presets.\nContinue?")
        if result == QtWidgets.QMessageBox.Yes:
            self.reset_config()

    def on_select_preset(self):
        preset = self.combo_preset.currentText()
        if preset == "":
            return
        self.config['preset'] = preset

    def on_change_fps(self):
        self.config['default_fps'] = self.spin_fps.value()

    def on_change_width(self):
        self.config['default_width'] = self.spin_width.value()

    def on_change_height(self):
        self.config['default_height'] = self.spin_height.value()

    def on_set_theme_system(self):
        self.config['theme'] = THEME_SYSTEM
        self.refresh_theme()

    def on_set_theme_light(self):
        self.config['theme'] = THEME_LIGHT
        self.refresh_theme()

    def on_set_theme_dark(self):
        self.config['theme'] = THEME_DARK
        self.refresh_theme()

    def on_use_system_ffmpeg(self):
        self.config['ffmpeg_version'] = ffmpeg_version.FFMPEG_SYSTEM

    def on_use_bundled_ffmpeg(self):
        self.config['ffmpeg_version'] = ffmpeg_version.FFMPEG_BUNDLED

    def on_ffmpeg_help_clicked(self):
        msg = [
            "Specify whether to use a version of FFmpeg already installed on the system, or the one that comes bundled "
            "with PolarBear.",
            "",
            "Regardless of which option is chosen, the bundled version will always be used as a fallback.",
            ""
        ]
        system_ffmpeg = ffmpeg_version.get_system_ffmpeg()
        if system_ffmpeg is None:
            msg += ["No FFmpeg was found on your system."]
        else:
            msg += ["FFmpeg installation found:", system_ffmpeg]
        QtWidgets.QMessageBox.information(self, "FFmpeg Help", "\n".join(msg))

    def refresh_theme(self):
        stylesheet_file = get_stylesheet(self.config['theme'])
        with open(stylesheet_file, 'r') as ss:
            self.setStyleSheet(ss.read())

    def update_widgets(self):
        """ Set up UI from config. """
        # Preset combo box
        self.update_preset_widget()

        # Other settings
        self.line_edit_save_path.setText(self.config['default_save_path'])
        self.spin_fps.setValue(self.config['default_fps'])
        self.spin_width.setValue(self.config['default_width'])
        self.spin_height.setValue(self.config['default_height'])

        # Theme
        theme_button_map = {
            THEME_SYSTEM: self.btn_theme_system_default,
            THEME_LIGHT: self.btn_theme_light,
            THEME_DARK: self.btn_theme_dark,
        }
        theme_button: QtWidgets.QPushButton = theme_button_map.get(self.config['theme'])
        theme_button.setChecked(True)

        # FFmpeg Version
        ffmpeg_button_map = {
            ffmpeg_version.FFMPEG_SYSTEM: self.btn_ffmpeg_system,
            ffmpeg_version.FFMPEG_BUNDLED: self.btn_ffmpeg_bundled,
        }
        ffmpeg_button: QtWidgets.QPushButton = ffmpeg_button_map.get(self.config['ffmpeg_version'])
        ffmpeg_button.setChecked(True)

    def update_preset_widget(self):
        self.combo_preset.blockSignals(True)

        self.combo_preset.clear()
        for preset in settings.get_preset_names():
            self.combo_preset.addItem(preset)

        if self.config['preset'] is not None:
            self.combo_preset.setCurrentText(self.config['preset'])
        else:
            self.combo_preset.setCurrentIndex(0)

        self.combo_preset.blockSignals(False)

    def reset_config(self):
        self.config = settings.default_settings
        settings.reset_presets()
        self.update_widgets()

    def force_config_update(self):
        self.on_select_preset()
        self.on_change_fps()
        self.on_change_width()
        self.on_change_height()
