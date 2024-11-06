import sys
import numpy as np
from PIL import Image
import pyqtgraph as pg
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
from Fourier.deconvolution import get_complex_spectrum, \
    get_complex_spectrum_part, get_amplitude, get_phase, get_opd


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.image_path = ''
        self.interf = ''

        # Подключение графического интерфейса
        uic.loadUi('gui.ui', self)
        self.loadImagePushButton.clicked.connect(self.load_image)
        self.getAmplitude.clicked.connect(self.calc_amplitude)
        self.set.clicked.connect(self.set_center_coord)
        # self.read.clicked.connect(self.write_center_coord)
        # TODO: Переименовать кнопку "read" как "calc_phase"
        self.read.clicked.connect(self.calc_phase)

    def plot_interf(self, img):
        """
        Отображение графика с интерферограммой
        """
        self.InterfPlot.clear()
        self.InterfPlot.addItem(pg.ImageItem(img), axisOrder='row-major')
        self.InterfPlot.setAspectLocked(True)

    def open_file_dialog(self):
        """
        Открытие файлового диалога для выбора интерферограммы
        """
        filename, ok = QFileDialog.getOpenFileName(
            self, "Select a File", "D:\\", "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
           self.image_path = Path(filename)

    def load_image(self):
        """
        Загрузка интерферограммы
        """
        self.open_file_dialog()
        img = Image.open(self.image_path)
        img = img.convert('L')
        img = np.asarray(img)
        self.interf = img
        self.plot_interf(self.interf)

    def plot(self, widget, img):
        """
        Отображение графика с интерферограммой
        """
        widget.clear()
        widget.addItem(pg.ImageItem(img), axisOrder='row-major')
        widget.setAspectLocked(True)

    def calc_amplitude(self):
        # complex spectrum
        self.cs = get_complex_spectrum(self.interf)
        # complex spectrum amplitude
        self.csa = get_amplitude(self.cs)
        self.plot(self.OtherPlot, self.csa)

    def calc_phase(self):
        self.cs_cutted = get_complex_spectrum_part(self.csa, self.cs,
                                                   self.x0, self.y0, self.r)

        self.ph = get_phase(self.cs_cutted)
        self.opd = get_opd(self.ph, 630)
        self.plot(self.OtherPlot, self.ph)

    def set_center_coord(self):
        self.x0, self.y0, self.r = list(map(int, self.lineEdit.text().split(',')))

    # TODO: Удалить второй lineEdit widget
    def write_center_coord(self):
        self.lineEdit_2.setText(str(self.x0) + ', ' + str(self.y0))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())