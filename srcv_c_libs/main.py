# This Python file uses the following encoding: utf-8
import sys
import os
from math import radians, sin, cos

from PyQt5 import QtWidgets #,uic
# from darktheme.widget_template import DarkPalette

import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QMessageBox, QColorDialog
from PyQt5.QtGui import QColor
from ui_mainwindow import Ui_project

from wingl import setHeightWF, setParticleSize, winGL, chHeightWF, chFarWF
from particle import up_down_WL

BACKGROUNDSTRING = "background-color: %s"

#teta_x = 0
#teta_y = 0
#teta_z = 0
CANCEL_FL = 0

class project(QtWidgets.QMainWindow, Ui_project):
    def __init__(self, *args, **kwargs):
        super(project, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.curColor = QColor(0, 0, 255, 1)
        self.colorWindow = None

        self.isActiveWF = True

        self.translateVec = {"w": False, "s": False, "a": False, "d": False}

        # Взаимодействие с окном

        # Водопад
        self.wf_run_btn.clicked.connect(self.controllWaterfall)
        self.sliderHeightWF.valueChanged.connect(self.changeHeightWF)
        self.sliderSpeedWF.valueChanged.connect(self.changeSpeedWF)
        self.sliderAmountParticles.valueChanged.connect(self.changeParticlesAmount)
        self.radiobutton.toggled.connect(self.day)
        self.radiobutton2.toggled.connect(self.night)

        # Камера
        # Перемещение
        self.cam_move_up_btn.clicked.connect(self.moveUp)
        self.cam_move_down_btn.clicked.connect(self.moveDown)
        self.cam_move_left_btn.clicked.connect(self.moveForward)
        self.cam_move_right_btn.clicked.connect(self.moveBack)
        self.cam_move_forward_btn.clicked.connect(self.moveLeft)
        self.cam_move_back_btn.clicked.connect(self.moveRight)

        # Масштабирование
        self.cam_scale_inc_btn.clicked.connect(self.scaleUp)
        self.cam_sclale_dec_btn.clicked.connect(self.scaleDown)

        # Поворот
        self.cam_spin_up_btn.clicked.connect(self.spinLeftY)
        self.cam_spin_down_btn.clicked.connect(self.spinRightY)
        self.cam_spin_left_btn.clicked.connect(self.spinLeftX)
        self.cam_spin_right_btn.clicked.connect(self.spinRightX)
        self.cam_spin_back_btn.clicked.connect(self.spinLeftZ)
        self.cam_spin_forward_btn.clicked.connect(self.spinRightZ)

        # Управление сценой
        self.transf_scene_control_btn.clicked.connect(self.cntl_scene_msg)

        self.exit_btn.clicked.connect(exit)

        # Таймер
        timer = QtCore.QTimer(self)
        timer.setInterval(1)
        timer.timeout.connect(self.timerActions)
        timer.start()

        timerW = QtCore.QTimer(self)
        timerW.setInterval(300)
        timerW.timeout.connect(self.timerUpdateWaterColor)
        timerW.start()

    def timerActions(self):
        if self.colorWindow:
            self.curColor = self.colorWindow.currentColor()
            self.colorBtn.setStyleSheet(
                BACKGROUNDSTRING % self.curColor.name()
            )

        if (self.isActiveWF):
            self.winGL.makeWaterfall()

        self.winGL.update(self.curColor.getRgbF(), self.translateVec)
        self.setWindowTitle("Артюхин Николай ИУ7-51Б Количество частиц воды: %5s,  %5s fps "
                            % (self.winGL.getAmountParticles(), self.winGL.getFPS()))

    def timerUpdateWaterColor(self):
        self.winGL.updateWaterColor()

    # Управление водопадом
    def controllWaterfall(self):
        global CANCEL_FL
        self.isActiveWF = not self.isActiveWF
        CANCEL_FL = 0
        self.winGL.init_pos_WF()

    def changeSpeedWF(self, value):
        self.winGL.changeSpeedWF(value)

    def changeAngleWF(self, value):
        self.winGL.changeAngleWF(value)

    def changeParticleSize(self, value):
        setParticleSize(value)

    def changeParticlesAmount(self, value):
        self.winGL.changeParticlesAmount(value)

    def changeHeightWF(self, value):
        if CANCEL_FL == 0:
            setHeightWF(value)
            self.winGL.changeHeightAliveWF(value)
            self.winGL.changeHeightRock(value)

    # Масштабирование
    def scaleUp(self):
        self.winGL.scale(1)

    def scaleDown(self):
        self.winGL.scale(-1)

    # Перемещение
    def moveUp(self):
        self.winGL.translate((0, 1, 0))

    def moveDown(self):
        self.winGL.translate((0, -1, 0))

    def moveLeft(self):
        self.winGL.translate((1, 0, 0))

    def moveRight(self):
        self.winGL.translate((-1, 0, 0))

    def moveForward(self):
        self.winGL.translate((0, 0, -1))

    def moveBack(self):
        self.winGL.translate((0, 0, 1))

    # Поворот
    def spinLeftX(self):
        self.winGL.spin((0, -1, 0))

    def spinRightX(self):
        self.winGL.spin((0, 1, 0))

    def spinLeftY(self):
        self.winGL.spin((1, 0, 0))

    def spinRightY(self):
        self.winGL.spin((-1, 0, 0))

    def spinLeftZ(self):
        self.winGL.spin((sin(radians(5)), cos(radians(5)), 0))  # -1 1 0

    def spinRightZ(self):
        self.winGL.spin((sin(radians(-5)), -cos(radians(5)), 0))  # 1 -1 0

    def night(self):
        self.winGL.changecolor()

    def day(self):
        self.winGL.changecolor2()

    def cntl_scene_msg(self):
        m = QMessageBox(self.centralwidget)
        m.setWindowTitle("Управление сценой")
        m.setText("Управление сценой производится с помощью следующих клавиш:\n"
                  "1) Поворот сцены вокруг Ox (по/против часовой стрелки) - клавиши 1, 2;\n"
                  "2) Поворот сцены вокруг Oy (по/против часовой стрелки) - клавиши 3, 4;\n"
                  "3) Поворот сцены вокруг Oz (по/против часовой стрелки) - клавиши 5, 6;\n"
                  "4) Приближение/удаление сцены - клавиши W, S;\n"
                  "5) Перемещение сцены влево/вправо - клавиши A, D;\n"
                  "6) Перемещение сцены вперед/назад - клавиши F, C;\n"
                  "7) Перемещение сцены вверх/вниз - клавиши H, B.\n"
                  "Динамический обзор сцены (включение) - ЛКМ по сцене + перемещение курсора мыши\n"
                  "Динамический обзор сцены (выключение) - ЛКМ по сцене")
        m.exec()

    def keyPressEvent(self, event):
        global CANCEL_FL
        #global teta_x, teta_y, teta_z
        if (event.key() == Qt.Key_W):
            self.translateVec["w"] = True
        elif (event.key() == Qt.Key_S):
            self.translateVec["s"] = True
        elif (event.key() == Qt.Key_A):
            self.translateVec["a"] = True
        elif (event.key() == Qt.Key_D):
            self.translateVec["d"] = True
        elif (event.key() == Qt.Key_1):
            CANCEL_FL = 1
            teta = radians(3)
            #teta_x -= teta
            self.winGL.rotate_scene_ox(teta)
            self.winGL.deleteExtraParticles()
            if self.isActiveWF:
                self.isActiveWF = not self.isActiveWF
        elif (event.key() == Qt.Key_2):
            CANCEL_FL = 1
            teta = radians(-3)
            #teta_x -= teta
            self.winGL.rotate_scene_ox(teta)
            self.winGL.deleteExtraParticles()
            if self.isActiveWF:
                self.isActiveWF = not self.isActiveWF
        elif (event.key() == Qt.Key_3):
            CANCEL_FL = 1
            teta = radians(3)
            #teta_y -= teta
            self.winGL.rotate_scene_oy(teta)
            self.winGL.deleteExtraParticles()
            if self.isActiveWF:
                self.isActiveWF = not self.isActiveWF
        elif (event.key() == Qt.Key_4):
            CANCEL_FL = 1
            teta = radians(-3)
            #teta_y -= teta
            self.winGL.rotate_scene_oy(teta)
            self.winGL.deleteExtraParticles()
            if self.isActiveWF:
                self.isActiveWF = not self.isActiveWF
        elif (event.key() == Qt.Key_5):
            CANCEL_FL = 1
            teta = radians(3)
            #teta_z -= teta
            self.winGL.rotate_scene_oz(teta)
            self.winGL.deleteExtraParticles()
            if self.isActiveWF:
                self.isActiveWF = not self.isActiveWF
        elif (event.key() == Qt.Key_6):
            CANCEL_FL = 1
            teta = radians(-3)
            #teta_z -= teta
            self.winGL.rotate_scene_oz(teta)
            self.winGL.deleteExtraParticles()
            if self.isActiveWF:
                self.isActiveWF = not self.isActiveWF
        elif (event.key() == Qt.Key_H):
            st = 0.5
            self.winGL.up_down_scene(st)
            self.winGL.WF_ch(st)
            chHeightWF(st)
            up_down_WL(st)
        elif (event.key() == Qt.Key_B):
            print('B')
            st = -0.5
            self.winGL.up_down_scene(st)
            self.winGL.WF_ch(st)
            chHeightWF(st)
            up_down_WL(st)
        elif (event.key() == Qt.Key_F):
            st = 1
            self.winGL.frw_bck_scene(st)
            self.winGL.WF_ch2(st)
            chFarWF(st)
        elif (event.key() == Qt.Key_C):
            st = -1
            self.winGL.frw_bck_scene(st)
            self.winGL.WF_ch2(st)
            chFarWF(st)

    def keyReleaseEvent(self, event):
        if (event.key() == Qt.Key_W):
            self.translateVec["w"] = False
        elif (event.key() == Qt.Key_S):
            self.translateVec["s"] = False
        elif (event.key() == Qt.Key_A):
            self.translateVec["a"] = False
        elif (event.key() == Qt.Key_D):
            self.translateVec["d"] = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = project()
    widget.show()
    sys.exit(app.exec_())