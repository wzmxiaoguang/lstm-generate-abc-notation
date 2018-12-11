import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import pygame
import numpy as np
import time


class SpectrumAnalyzer:
    def __init__(self, parent):
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.centralWid = QtGui.QWidget(self.parent)
        self.centralWid.setGeometry(0, 200, 700, 500)
        self.lay = QtGui.QVBoxLayout()
        self.centralWid.setLayout(self.lay)

        self.specWid = pg.PlotWidget()
        self.specItem = self.specWid.getPlotItem()
        self.specItem.setMouseEnabled(x=False, y=False)
        self.specItem.setYRange(-200, 200)
        self.specItem.setXRange(0, 1000, padding=0)
        self.lay.addWidget(self.specWid)

    def getdata(self):
        sampling_rate = 500
        fft_size = 500
        t = np.arange(0, 1000, 1000/sampling_rate)
        x = np.sin(2*np.pi*156.25*t) + 2*np.sin(2*np.pi*234.375*t)
        xs = x[:fft_size]
        xf = np.fft.rfft(xs)/fft_size
        freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
        xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
        return t[:fft_size], xs*50

    def mainLoop(self):
        xx, yy = self.getdata()
        y0 = np.zeros([500])
        count = 0
        while 1:
            if pygame.mixer.music.get_busy():
                a = np.random.rand(500)
                self.specItem.plot(x=xx, y=yy*a, clear=True)
            else:
                self.specItem.plot(x=xx, y=y0, clear=True)
            QtGui.QApplication.processEvents()
            time.sleep(0.05)
