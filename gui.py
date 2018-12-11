from sample import sample
from win32api import GetSystemMetrics
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from mode import *
import music21
import pygame
import sys
import os


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.setWindowTitle("人工智能音乐生成")
        self.setGeometry(GetSystemMetrics(0)/2 - 350, GetSystemMetrics(1)/2 - 350, 700, 700)
        self.setFont(QtGui.QFont("", 20, QtGui.QFont.Bold))
        pygame.mixer.init()
        self.secnum = 50
        if not os.path.isdir(os.getcwd() + '\\music'):
            os.mkdir(os.getcwd() + '\\music')

        self.button1 = QPushButton(self)
        self.button1.setText("播放")
        self.button1.setGeometry(250, 90, 100, 50)
        self.button1.clicked.connect(self.play)

        self.button2 = QPushButton(self)
        self.button2.setText("停止")
        self.button2.setGeometry(350, 90, 100, 50)
        self.button2.clicked.connect(self.stop)

        self.button3 = QPushButton(self)
        self.button3.setText("上一首")
        self.button3.setGeometry(150, 90, 100, 50)
        self.button3.clicked.connect(self.pre)

        self.button4 = QPushButton(self)
        self.button4.setText("下一首")
        self.button4.setGeometry(450, 90, 100, 50)
        self.button4.clicked.connect(self.next)
        self.sa = SpectrumAnalyzer(self)

    def play(self):
        abcpath = os.getcwd() + '\\music\\' + str(self.secnum) + '.abc'
        midipath = os.getcwd() + '\\music\\' + str(self.secnum) + '.mid'
        if not os.path.exists(midipath):
            sample(self.secnum)
            music21.converter.parse(abcpath).write('midi', midipath)
        pygame.mixer.music.load(midipath)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def pre(self):
        self.secnum -= 1
        self.play()

    def next(self):
        self.secnum += 1
        self.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = MainWidget()
    myshow.show()
    myshow.sa.mainLoop()
    sys.exit(app.exec_())
