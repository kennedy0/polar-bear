import datetime
import os
import shlex
import subprocess
import threading
from typing import TextIO

from PyQt5 import QtWidgets, QtGui, QtCore

from gui.main_window import Ui_MainWindow

from config import settings
from config.ffmpeg_version import get_ffmpeg_binary
from config.theme import get_stylesheet
from config.resources import ICON_FILE
from .options_window import OptionsWindow
from __version__ import __version__


class ScreenRecorder(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, title: str):
        super().__init__()

        self.ffmpeg_process = None

        self.mouse_start = None
        self.window_pos_start = None
        self.window_width_start = None
        self.window_height_start = None

        self.is_recording = False

        self.config = dict()
        self.last_directory = None

        self.setupUi(self)
        self._init_ui_style()
        self._init_callbacks()
        self._load_config()

        self.lbl_title.setText(title)
        self.btn_about.setIcon(QtGui.QIcon(ICON_FILE))
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))

        self.set_recording_state(recording=False)
        self.group_title.setFocus()

    def _init_ui_style(self):
        # Set window flags.
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, on=True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on=True)

        # Set the "resize handle" borders.
        border_size = 10
        border_widgets = [self.resize_top_left, self.resize_top, self.resize_top_right,
                          self.resize_left, self.resize_right,
                          self.resize_bottom_left, self.resize_bottom, self.resize_bottom_right]
        for widget in border_widgets:
            widget.setMinimumSize(border_size, border_size)

    def _init_callbacks(self):
        self.btn_ffmpeg_command.clicked.connect(self.on_ffmpeg_command_clicked)
        self.btn_about.clicked.connect(self.on_about_clicked)
        self.btn_close.clicked.connect(self.on_close_clicked)
        self.btn_options.clicked.connect(self.on_options_clicked)
        self.btn_record.clicked.connect(self.on_record_clicked)
        self.btn_stop.clicked.connect(self.on_stop_clicked)
        self.spin_width.editingFinished.connect(self.on_edit_width)
        self.spin_height.editingFinished.connect(self.on_edit_height)

    def _load_config(self):
        """ Load config from file and apply settings. """
        self.config = settings.load_config()

        # If the saved preset does not exist, clear it
        if self.config['preset'] not in settings.get_preset_names():
            self.config['preset'] = None

        # If there is no preset, load the first one
        if self.config['preset'] is None:
            preset_files = settings.get_preset_files()
            if not len(preset_files):
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error Loading Preset",
                    "No preset files were found.\nAdd or reset the presets with the Options menu.")
                self.apply_settings()
                return
            preset = settings.preset_name_from_file(file=preset_files[0])
            self.config['preset'] = preset

        self.apply_settings()

    def set_theme(self, theme: str):
        stylesheet_file = get_stylesheet(theme)
        with open(stylesheet_file, 'r') as ss:
            self.setStyleSheet(ss.read())

    def apply_settings(self):
        self.last_directory = self.config['default_save_path']
        self.set_fps(self.config['default_fps'])
        self.set_window_width(self.config['default_width'])
        self.set_window_height(self.config['default_height'])
        self.set_theme(theme=self.config['theme'])

    def on_ffmpeg_command_clicked(self):
        ffmpeg_cmd = self.build_ffmpeg_cmd(file="OUTPUT")
        ffmpeg_cmd = ffmpeg_cmd.replace(" -", "<br />-")
        ffmpeg_msg = QtWidgets.QMessageBox(self)
        ffmpeg_msg.setText(ffmpeg_cmd)
        ffmpeg_msg.setWindowTitle("FFmpeg Command")

        self.hide()
        ffmpeg_msg.exec()
        self.show()

    def on_about_clicked(self):
        msg = [
            f"Version {__version__}",
            "<a href=\"https://github.com/kennedy0/PolarBear/releases/latest\" style=\"color: darkgray;\">"
            "Download the latest version from GitHub</a>"
        ]
        about = QtWidgets.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setText("<br /><br />".join(msg))
        about.setWindowTitle("About PolarBear")

        self.hide()
        about.exec()
        self.show()

    def on_close_clicked(self):
        settings.save_config(self.config)
        self.close()

    def on_options_clicked(self):
        self.hide()
        options = OptionsWindow(parent=self, config=self.config)
        result = options.exec_()
        self.show()

        if result == QtWidgets.QDialog.Accepted:
            self.config = options.config
            self.apply_settings()

    def on_record_clicked(self):
        # noinspection PyBroadException
        try:
            self.validate_ffmpeg_command()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error Loading Preset", str(e))
            return

        file_name = self.get_video_file_path()
        if file_name is None:
            return
        self.last_directory = os.path.dirname(file_name)

        # Start ffmpeg subprocess
        ffmpeg_str = self.build_ffmpeg_cmd(file=file_name)
        log_file = self.create_log_file(video_file_path=file_name)

        if os.name == "nt":
            creation_flags = subprocess.CREATE_NO_WINDOW
            ffmpeg_cmd = shlex.split(ffmpeg_str, posix=False)
        else:
            creation_flags = 0
            ffmpeg_cmd = shlex.split(ffmpeg_str)

        self.ffmpeg_process = subprocess.Popen(
            ffmpeg_cmd,
            creationflags=creation_flags,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
        )

        self.set_recording_state(True)
        thread = threading.Thread(target=self.poll_subprocess, args=(log_file,))
        thread.start()

    def on_stop_clicked(self):
        if isinstance(self.ffmpeg_process, subprocess.Popen):
            # Send a quit signal to ffmpeg.
            self.ffmpeg_process.communicate(b"q")

    def on_edit_width(self):
        self.set_window_width(self.spin_width.value())

    def on_edit_height(self):
        self.set_window_height(self.spin_height.value())

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.LeftButton:
            # Get start positions to calculate offsets during resizing.
            self.mouse_start = a0.pos()
            self.window_pos_start = self.pos()
            self.window_width_start = self.width()
            self.window_height_start = self.height()
        else:
            super().mousePressEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        super().mouseReleaseEvent(a0)
        self.mouse_start = None
        self.round_size()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self.mouse_start is not None and a0.buttons() == QtCore.Qt.LeftButton and not self.is_recording:
            mouse_x = a0.pos().x()
            mouse_y = a0.pos().y()
            offset_x = mouse_x - self.mouse_start.x()
            offset_y = mouse_y - self.mouse_start.y()

            # Default x/y/w/h for the setGeometry call.
            x = self.window_pos_start.x()
            y = self.window_pos_start.y()
            w = self.window_width_start
            h = self.window_height_start

            # Calculate new position and/or size based on the region grabbed.
            if self.group_title.underMouse():
                x = self.pos().x() + offset_x
                y = self.pos().y() + offset_y
            elif self.resize_right.underMouse():
                w = self.window_width_start + offset_x
            elif self.resize_left.underMouse():
                x = self.pos().x() + offset_x
                w = self.width() - offset_x
            elif self.resize_bottom.underMouse():
                h = self.window_height_start + offset_y
            elif self.resize_top.underMouse():
                y = self.pos().y() + offset_y
                h = self.height() - offset_y
            elif self.resize_bottom_right.underMouse():
                w = self.window_width_start + offset_x
                h = self.window_height_start + offset_y
            elif self.resize_bottom_left.underMouse():
                x = self.pos().x() + offset_x
                w = self.width() - offset_x
                h = self.window_height_start + offset_y
            elif self.resize_top_right.underMouse():
                y = self.pos().y() + offset_y
                w = self.window_width_start + offset_x
                h = self.height() - offset_y
            elif self.resize_top_left.underMouse():
                x = self.pos().x() + offset_x
                y = self.pos().y() + offset_y
                w = self.width() - offset_x
                h = self.height() - offset_y
            self.setGeometry(x, y, w, h)
        else:
            super().mouseMoveEvent(a0)

    def set_fps(self, fps: int):
        self.fps.setValue(fps)

    def set_window_width(self, width: int):
        width_padding = self.width() - self.capture_region.width()
        self.resize(width + width_padding, self.height())
        self.round_size()

    def set_window_height(self, height: int):
        height_padding = self.height() - self.capture_region.height()
        self.resize(self.width(), height + height_padding)
        self.round_size()

    def round_size(self):
        """ Ensure that the video resolution is a multiple of 2. Odd values cause encoding errors with yuv420p. """
        if self.capture_region.width() % 2 != 0:
            self.resize(self.width() + 1, self.height())
        if self.capture_region.height() % 2 != 0:
            self.resize(self.width(), self.height() + 1)

    def build_ffmpeg_cmd(self, file: str) -> str:
        ffmpeg_binary = get_ffmpeg_binary(self.config['ffmpeg_version'])
        fps = str(self.fps.value())
        x = str(self.capture_region.mapToGlobal(QtCore.QPoint(0, 0)).x())
        y = str(self.capture_region.mapToGlobal(QtCore.QPoint(0, 0)).y())
        w = str(self.capture_region.width())
        h = str(self.capture_region.height())

        cmd_str = self.read_preset_file()
        cmd_str = cmd_str.replace("<FFMPEG>", ffmpeg_binary)
        cmd_str = cmd_str.replace("<FPS>", fps)
        cmd_str = cmd_str.replace("<X>", x)
        cmd_str = cmd_str.replace("<Y>", y)
        cmd_str = cmd_str.replace("<SIZE>", f"{w}x{h}")
        cmd_str = cmd_str.replace("<OUTPUT>", file)

        return cmd_str

    def read_preset_file(self):
        preset_file = settings.file_from_preset_name(preset=self.config['preset'])
        with open(preset_file, "r") as fp:
            lines = [line.strip() for line in fp.readlines()]
        command = " ".join(lines)
        return command

    def validate_ffmpeg_command(self):
        cmd = self.read_preset_file()

        if not cmd.startswith("<FFMPEG>"):
            raise RuntimeError(f"Invalid FFmpeg command; command must start with \"<FFMPEG>\"")

        required_keywords = ["<FFMPEG>", "<FPS>", "<X>", "<Y>", "<SIZE>", "<OUTPUT>", "-y"]
        for keyword in required_keywords:
            if cmd.find(keyword) < 0:
                raise RuntimeError(f"Invalid FFmpeg command; keyword not found: {keyword}")

    def get_video_file_path(self) -> str or None:
        extension = self.get_output_extension()
        file_name, _filter = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Save Video As",
            directory=self.last_directory,
            filter=f"{extension.strip('.')} (*{extension})"
        )

        # If dialog was cancelled, return None.
        if file_name == "":
            return None

        # Strip the extension from the file name; it'll be added in the ffmpeg command.
        if file_name.endswith(extension):
            file_name = os.path.splitext(file_name)[0]
        return file_name

    def get_output_extension(self) -> str:
        """ Parse the ffmpeg command and get its file extension. """
        cmd = self.read_preset_file()
        file_name = cmd.split(" ")[-1].strip("\"")
        extension = os.path.splitext(file_name)[-1]
        return extension

    @staticmethod
    def create_log_file(video_file_path: str) -> TextIO:
        try:
            os.makedirs(settings.LOG_PATH)
        except OSError:
            pass
        video_file_name = os.path.basename(video_file_path)
        log_file_name = datetime.datetime.now().strftime(f"%Y%m%d_%H%M%S_{video_file_name}.log")
        log_file_path = os.path.join(settings.LOG_PATH, log_file_name)
        return open(log_file_path, 'w')

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        super().resizeEvent(a0)
        self.update_mask()
        self.update_resolution_spin_boxes()

    def moveEvent(self, a0: QtGui.QMoveEvent):
        super().moveEvent(a0)
        self.update_mask()

    def update_mask(self):
        """ Sets a mask the size of the Window geometry, and subtracts the rect of the capture_region. """
        window_rect = self.main_widget.frameGeometry()
        main_widget_region = QtGui.QRegion(window_rect)
        capture_rect = self.capture_region.frameGeometry()
        capture_region = QtGui.QRegion(capture_rect)
        mask = main_widget_region.subtracted(capture_region)
        self.setMask(mask)

    def update_resolution_spin_boxes(self):
        """ Update the resolution spin boxes to reflect the capture region size. """
        self.spin_width.setValue(self.capture_region.frameGeometry().width())
        self.spin_height.setValue(self.capture_region.frameGeometry().height())

    def set_recording_state(self, recording: bool):
        """ Enable / Disable UI elements for recording. """
        self.is_recording = recording
        all_interactable_widgets = [
            self.spin_width,
            self.spin_height,
            self.fps,
            self.btn_close,
            self.btn_options,
            self.btn_ffmpeg_command,
            self.btn_about,
            self.btn_record,
            self.btn_stop,
        ]
        if self.is_recording:
            self.lbl_status.setText("<span style=\"color:red\">●</span> Recording")
            self.lbl_title.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
            for widget in all_interactable_widgets:
                widget.setEnabled(False)
            self.btn_stop.setEnabled(True)
        else:
            self.lbl_status.setText("■ Stopped")
            self.lbl_title.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
            for widget in all_interactable_widgets:
                widget.setEnabled(True)
            self.btn_stop.setEnabled(False)

    def poll_subprocess(self, log_file: TextIO):
        """ Wait for ffmpeg subprocess to end; close log file and set the recording state. """
        while self.ffmpeg_process.poll() is None:
            pass
        log_file.close()
        self.ffmpeg_process = None
        self.set_recording_state(False)
