# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\a\git\PolarBear\ui\options.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Options(object):
    def setupUi(self, Options):
        Options.setObjectName("Options")
        Options.resize(536, 281)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        Options.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Options)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.group_theme = QtWidgets.QGroupBox(Options)
        self.group_theme.setTitle("")
        self.group_theme.setObjectName("group_theme")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.group_theme)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_theme_system_default = QtWidgets.QPushButton(self.group_theme)
        self.btn_theme_system_default.setCheckable(True)
        self.btn_theme_system_default.setChecked(True)
        self.btn_theme_system_default.setAutoExclusive(True)
        self.btn_theme_system_default.setFlat(True)
        self.btn_theme_system_default.setObjectName("btn_theme_system_default")
        self.horizontalLayout.addWidget(self.btn_theme_system_default)
        self.btn_theme_light = QtWidgets.QPushButton(self.group_theme)
        self.btn_theme_light.setCheckable(True)
        self.btn_theme_light.setAutoExclusive(True)
        self.btn_theme_light.setFlat(True)
        self.btn_theme_light.setObjectName("btn_theme_light")
        self.horizontalLayout.addWidget(self.btn_theme_light)
        self.btn_theme_dark = QtWidgets.QPushButton(self.group_theme)
        self.btn_theme_dark.setCheckable(True)
        self.btn_theme_dark.setAutoExclusive(True)
        self.btn_theme_dark.setFlat(True)
        self.btn_theme_dark.setObjectName("btn_theme_dark")
        self.horizontalLayout.addWidget(self.btn_theme_dark)
        self.gridLayout.addWidget(self.group_theme, 6, 2, 1, 2)
        self.group_ffmpeg = QtWidgets.QGroupBox(Options)
        self.group_ffmpeg.setTitle("")
        self.group_ffmpeg.setObjectName("group_ffmpeg")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.group_ffmpeg)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_ffmpeg_system = QtWidgets.QPushButton(self.group_ffmpeg)
        self.btn_ffmpeg_system.setCheckable(True)
        self.btn_ffmpeg_system.setChecked(True)
        self.btn_ffmpeg_system.setAutoExclusive(True)
        self.btn_ffmpeg_system.setFlat(True)
        self.btn_ffmpeg_system.setObjectName("btn_ffmpeg_system")
        self.horizontalLayout_2.addWidget(self.btn_ffmpeg_system)
        self.btn_ffmpeg_bundled = QtWidgets.QPushButton(self.group_ffmpeg)
        self.btn_ffmpeg_bundled.setCheckable(True)
        self.btn_ffmpeg_bundled.setAutoExclusive(True)
        self.btn_ffmpeg_bundled.setFlat(True)
        self.btn_ffmpeg_bundled.setObjectName("btn_ffmpeg_bundled")
        self.horizontalLayout_2.addWidget(self.btn_ffmpeg_bundled)
        self.gridLayout.addWidget(self.group_ffmpeg, 7, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Options)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Options)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(Options)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.spin_width = QtWidgets.QSpinBox(Options)
        self.spin_width.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_width.setMinimum(2)
        self.spin_width.setMaximum(9999)
        self.spin_width.setSingleStep(2)
        self.spin_width.setProperty("value", 800)
        self.spin_width.setObjectName("spin_width")
        self.gridLayout.addWidget(self.spin_width, 4, 2, 1, 2)
        self.spin_fps = QtWidgets.QSpinBox(Options)
        self.spin_fps.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_fps.setMinimum(1)
        self.spin_fps.setMaximum(9999)
        self.spin_fps.setProperty("value", 30)
        self.spin_fps.setObjectName("spin_fps")
        self.gridLayout.addWidget(self.spin_fps, 3, 2, 1, 2)
        self.label_6 = QtWidgets.QLabel(Options)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.line_edit_save_path = QtWidgets.QLineEdit(Options)
        self.line_edit_save_path.setObjectName("line_edit_save_path")
        self.gridLayout.addWidget(self.line_edit_save_path, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(Options)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.spin_height = QtWidgets.QSpinBox(Options)
        self.spin_height.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_height.setMinimum(2)
        self.spin_height.setMaximum(9999)
        self.spin_height.setSingleStep(2)
        self.spin_height.setProperty("value", 600)
        self.spin_height.setObjectName("spin_height")
        self.gridLayout.addWidget(self.spin_height, 5, 2, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(4, 4, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Options)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.btn_open_folder = QtWidgets.QPushButton(Options)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_open_folder.sizePolicy().hasHeightForWidth())
        self.btn_open_folder.setSizePolicy(sizePolicy)
        self.btn_open_folder.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_open_folder.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_open_folder.setObjectName("btn_open_folder")
        self.gridLayout.addWidget(self.btn_open_folder, 2, 3, 1, 1)
        self.btn_ffmpeg_help = QtWidgets.QPushButton(Options)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ffmpeg_help.sizePolicy().hasHeightForWidth())
        self.btn_ffmpeg_help.setSizePolicy(sizePolicy)
        self.btn_ffmpeg_help.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_ffmpeg_help.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_ffmpeg_help.setObjectName("btn_ffmpeg_help")
        self.gridLayout.addWidget(self.btn_ffmpeg_help, 7, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(Options)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_open_presets = QtWidgets.QPushButton(Options)
        self.btn_open_presets.setObjectName("btn_open_presets")
        self.gridLayout_3.addWidget(self.btn_open_presets, 1, 1, 1, 1)
        self.btn_refresh_presets = QtWidgets.QPushButton(Options)
        self.btn_refresh_presets.setObjectName("btn_refresh_presets")
        self.gridLayout_3.addWidget(self.btn_refresh_presets, 1, 2, 1, 1)
        self.btn_help = QtWidgets.QPushButton(Options)
        self.btn_help.setObjectName("btn_help")
        self.gridLayout_3.addWidget(self.btn_help, 1, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 2, 1, 2)
        self.combo_preset = QtWidgets.QComboBox(Options)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_preset.sizePolicy().hasHeightForWidth())
        self.combo_preset.setSizePolicy(sizePolicy)
        self.combo_preset.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.combo_preset.setObjectName("combo_preset")
        self.gridLayout.addWidget(self.combo_preset, 0, 2, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_reset = QtWidgets.QPushButton(Options)
        self.btn_reset.setObjectName("btn_reset")
        self.horizontalLayout_5.addWidget(self.btn_reset)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.btn_ok = QtWidgets.QPushButton(Options)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout_5.addWidget(self.btn_ok)
        self.btn_cancel = QtWidgets.QPushButton(Options)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_5.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Options)
        QtCore.QMetaObject.connectSlotsByName(Options)

    def retranslateUi(self, Options):
        _translate = QtCore.QCoreApplication.translate
        Options.setWindowTitle(_translate("Options", "options"))
        self.btn_theme_system_default.setText(_translate("Options", "System Default"))
        self.btn_theme_light.setText(_translate("Options", "Light"))
        self.btn_theme_dark.setText(_translate("Options", "Dark"))
        self.btn_ffmpeg_system.setText(_translate("Options", "Prefer User Installed"))
        self.btn_ffmpeg_bundled.setText(_translate("Options", "Always Use Bundled"))
        self.label_2.setText(_translate("Options", "FFmpeg Version"))
        self.label_8.setText(_translate("Options", "Default Width"))
        self.label_9.setText(_translate("Options", "Default Height"))
        self.label_6.setText(_translate("Options", "Default Save Path"))
        self.label_7.setText(_translate("Options", "Default FPS"))
        self.label.setText(_translate("Options", "Theme"))
        self.btn_open_folder.setText(_translate("Options", "🗀"))
        self.btn_ffmpeg_help.setText(_translate("Options", "?"))
        self.label_10.setText(_translate("Options", "Preset"))
        self.btn_open_presets.setText(_translate("Options", "Open Presets Folder"))
        self.btn_refresh_presets.setText(_translate("Options", "Refresh Presets"))
        self.btn_help.setText(_translate("Options", "Presets Help"))
        self.btn_reset.setText(_translate("Options", "Reset"))
        self.btn_ok.setText(_translate("Options", "Ok"))
        self.btn_cancel.setText(_translate("Options", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Options = QtWidgets.QDialog()
    ui = Ui_Options()
    ui.setupUi(Options)
    Options.show()
    sys.exit(app.exec_())
