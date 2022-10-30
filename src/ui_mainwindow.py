from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QRadioButton


class Ui_project(object):
    def setupUi(self, project):
        project.setObjectName("Course project Artiukhin Nikolay IU7-51B")
        project.resize(1800, 750)
        font = QtGui.QFont()
        font.setPointSize(10)
        project.setFont(font)
        self.centralwidget = QtWidgets.QWidget(project)
        self.centralwidget.setObjectName("centralwidget")

        self.winGL = winGL(project)
        self.winGL.setGeometry(QtCore.QRect(500, 10, 800, 720))
        self.winGL.setObjectName("winGL")

        self.groupBox_1 = QtWidgets.QGroupBox(self)
        self.groupBox_1.setGeometry(QtCore.QRect(1320, 10, 400, 600))
        self.groupBox_1.setObjectName("groupBox_1")

        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_1)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 30, 350, 100))
        self.groupBox_2.setObjectName("groupBox_2")

        self.wf_run_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.wf_run_btn.setGeometry(QtCore.QRect(30, 30, 300, 60))
        self.wf_run_btn.setObjectName("wf_run_btn")

        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_1)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 150, 350, 90))
        self.groupBox_3.setObjectName("groupBox_3")

        self.radiobutton = QtWidgets.QRadioButton("День", self.groupBox_3)
        self.radiobutton.setChecked(True)
        self.radiobutton.setGeometry(QtCore.QRect(30, 30, 100, 42))
        self.radiobutton.setObjectName("radiobut1")
        self.radiobutton2 = QtWidgets.QRadioButton("Ночь", self.groupBox_3)
        self.radiobutton2.setChecked(False)
        self.radiobutton2.setGeometry(QtCore.QRect(150, 30, 271, 42))
        self.radiobutton2.setObjectName("radiobut2")

        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_1)
        self.groupBox_4.setGeometry(QtCore.QRect(30, 260, 350, 230))
        self.groupBox_4.setObjectName("groupBox_4")

        self.label_1 = QtWidgets.QLabel(self.groupBox_4)
        self.label_1.setGeometry(QtCore.QRect(30, 20, 300, 50))
        self.label_1.setObjectName("label_1")

        self.sliderHeightWF = QtWidgets.QSlider(self.groupBox_4)
        self.sliderHeightWF.setMinimum(-12)
        self.sliderHeightWF.setMaximum(10)
        self.sliderHeightWF.setPageStep(10)
        self.sliderHeightWF.setProperty("value", 0)
        self.sliderHeightWF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderHeightWF.setGeometry(QtCore.QRect(30, 60, 300, 30))
        self.sliderHeightWF.setObjectName("sliderHeightWF")

        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 300, 50))
        self.label_2.setObjectName("label_2")

        self.sliderSpeedWF = QtWidgets.QSlider(self.groupBox_4)
        self.sliderSpeedWF.setGeometry(QtCore.QRect(30, 120, 300, 30))
        self.sliderSpeedWF.setMinimum(10)
        self.sliderSpeedWF.setMaximum(1000)
        self.sliderSpeedWF.setSingleStep(50)
        self.sliderSpeedWF.setPageStep(10)
        self.sliderSpeedWF.setProperty("value", 98)
        self.sliderSpeedWF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderSpeedWF.setObjectName("sliderSpeedWF")

        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 300, 50))
        self.label_3.setObjectName("label_3")

        self.sliderAmountParticles = QtWidgets.QSlider(self.groupBox_4)
        self.sliderAmountParticles.setMinimum(0)
        self.sliderAmountParticles.setMaximum(70)
        self.sliderAmountParticles.setSingleStep(5)
        self.sliderAmountParticles.setPageStep(10)
        self.sliderAmountParticles.setProperty("value", 50)
        self.sliderAmountParticles.setOrientation(QtCore.Qt.Horizontal)
        self.sliderAmountParticles.setGeometry(QtCore.QRect(30, 180, 300, 30))
        self.sliderAmountParticles.setObjectName("sliderAmountParticles")

        self.exit_btn = QtWidgets.QPushButton(self.groupBox_1)
        self.exit_btn.setGeometry(QtCore.QRect(100, 520, 200, 50))
        self.exit_btn.setObjectName("exit_btn")

        self.groupBox_5 = QtWidgets.QGroupBox(self)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 10, 400, 600))
        self.groupBox_5.setObjectName("groupBox_5")

        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_6.setGeometry(QtCore.QRect(30, 30, 350, 200))
        self.groupBox_6.setObjectName("groupBox_6")

        self.cam_move_up_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.cam_move_up_btn.setGeometry(QtCore.QRect(100, 40, 70, 30))
        self.cam_move_up_btn.setObjectName("cam_move_up_btn")

        self.cam_move_down_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.cam_move_down_btn.setGeometry(QtCore.QRect(100, 100, 70, 30))
        self.cam_move_down_btn.setObjectName("cam_move_down_btn")

        self.cam_move_right_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.cam_move_right_btn.setGeometry(QtCore.QRect(180, 70, 50, 30))
        self.cam_move_right_btn.setObjectName("cam_move_right_btn")

        self.cam_move_left_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.cam_move_left_btn.setGeometry(QtCore.QRect(41, 70, 50, 30))
        self.cam_move_left_btn.setObjectName("cam_move_left_btn")

        self.cam_move_forward_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.cam_move_forward_btn.setGeometry(QtCore.QRect(50, 140, 70, 30))
        self.cam_move_forward_btn.setObjectName("cam_move_forward_btn")

        self.cam_move_back_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.cam_move_back_btn.setGeometry(QtCore.QRect(160, 140, 70, 30))
        self.cam_move_back_btn.setObjectName("cam_move_back_btn")

        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_7.setGeometry(QtCore.QRect(30, 250, 350, 100))
        self.groupBox_7.setObjectName("groupBox_7")

        self.cam_scale_inc_btn = QtWidgets.QPushButton(self.groupBox_7)
        self.cam_scale_inc_btn.setGeometry(QtCore.QRect(50, 35, 70, 40))
        self.cam_scale_inc_btn.setObjectName("cam_scale_inc_btn")

        self.cam_sclale_dec_btn = QtWidgets.QPushButton(self.groupBox_7)
        self.cam_sclale_dec_btn.setGeometry(QtCore.QRect(160, 35, 70, 40))
        self.cam_sclale_dec_btn.setObjectName("cam_sclale_dec_btn")

        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_8.setGeometry(QtCore.QRect(30, 370, 350, 200))
        self.groupBox_8.setObjectName("groupBox_8")

        self.cam_spin_up_btn = QtWidgets.QPushButton(self.groupBox_8)
        self.cam_spin_up_btn.setGeometry(QtCore.QRect(100, 40, 70, 30))
        self.cam_spin_up_btn.setObjectName("cam_spin_up_btn")

        self.cam_spin_down_btn = QtWidgets.QPushButton(self.groupBox_8)
        self.cam_spin_down_btn.setGeometry(QtCore.QRect(100, 100, 70, 30))
        self.cam_spin_down_btn.setObjectName("cam_spin_down_btn")

        self.cam_spin_right_btn = QtWidgets.QPushButton(self.groupBox_8)
        self.cam_spin_right_btn.setGeometry(QtCore.QRect(180, 70, 50, 30))
        self.cam_spin_right_btn.setObjectName("cam_spin_right_btn")

        self.cam_spin_left_btn = QtWidgets.QPushButton(self.groupBox_8)
        self.cam_spin_left_btn.setGeometry(QtCore.QRect(41, 70, 50, 30))
        self.cam_spin_left_btn.setObjectName("cam_spin_left_btn")

        self.cam_spin_forward_btn = QtWidgets.QPushButton(self.groupBox_8)
        self.cam_spin_forward_btn.setGeometry(QtCore.QRect(50, 140, 70, 30))
        self.cam_spin_forward_btn.setObjectName("cam_spin_forward_btn")

        self.cam_spin_back_btn = QtWidgets.QPushButton(self.groupBox_8)
        self.cam_spin_back_btn.setGeometry(QtCore.QRect(160, 140, 70, 30))
        self.cam_spin_back_btn.setObjectName("cam_spin_back_btn")

        self.transf_scene_control_btn = QtWidgets.QPushButton(self)
        self.transf_scene_control_btn.setGeometry(QtCore.QRect(120, 640, 200, 50))
        self.transf_scene_control_btn.setObjectName("transf_scene_control_btn")

        self.retranslateUi(project)
        QtCore.QMetaObject.connectSlotsByName(project)

    def retranslateUi(self, project):
        _translate = QtCore.QCoreApplication.translate
        project.setWindowTitle(_translate("project", "Курсовая работа по компьютерной графике Артюхин Николай ИУ7-51Б"))
        self.groupBox_1.setTitle(_translate("project", "Водопад"))
        self.groupBox_2.setTitle(_translate("project", "Моделирование водопада"))
        self.wf_run_btn.setText(_translate("project", "Запуск/остановка"))
        self.groupBox_3.setTitle(_translate("project", "Время суток"))
        self.groupBox_4.setTitle(_translate("project", "Параметры водопада"))
        self.label_1.setText(_translate("project", "Высота водопада"))
        self.label_2.setText(_translate("project", "Скорость течения воды"))
        self.label_3.setText(_translate("project", "Количество частиц воды"))
        self.groupBox_5.setTitle(_translate("project", "Камера"))
        self.groupBox_6.setTitle(_translate("project", "Перемещение"))
        self.cam_move_up_btn.setText(_translate("project", "↑"))
        self.cam_move_right_btn.setText(_translate("project", "→"))
        self.cam_move_left_btn.setText(_translate("project", "←"))
        self.cam_move_down_btn.setText(_translate("project", "↓"))
        self.cam_move_forward_btn.setText(_translate("project", "Вперед"))
        self.cam_move_back_btn.setText(_translate("project", "Назад"))
        self.groupBox_7.setTitle(_translate("project", "Масштабирование"))
        self.cam_scale_inc_btn.setText(_translate("project", "+"))
        self.cam_sclale_dec_btn.setText(_translate("project", "-"))
        self.groupBox_8.setTitle(_translate("project", "Поворот"))
        self.cam_spin_right_btn.setText(_translate("project", "→"))
        self.cam_spin_left_btn.setText(_translate("project", "←"))
        self.cam_spin_up_btn.setText(_translate("project", "↑"))
        self.cam_spin_down_btn.setText(_translate("project", "↓"))
        self.cam_spin_back_btn.setText(_translate("project", "⟳"))
        self.cam_spin_forward_btn.setText(_translate("project", "⟲"))
        self.transf_scene_control_btn.setText(_translate("project", "Управление сценой"))
        self.exit_btn.setText(_translate("project", "Выход"))

from wingl import winGL