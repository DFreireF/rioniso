import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QLoggingCategory, QCoreApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backend_bases import PickEvent
import matplotlib.pyplot as plt

from rioniso.model import IsoCurve
from rioniso.importdata import ImportData
from rioniso.plotters import Plotters

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.plotters = Plotters()  # Initialize Plotters
        #self.plotters._set_fig(width=15, height=8, dpi=300, fs = 18)
        super().__init__(self.plotters.fig)
        self.setParent(parent)
        self.mpl_connect('pick_event', self.on_pick)

    def on_pick(self, event):
        """ Toggle visibility of picked data points. """
        index = event.ind[0]  # Get the first (and should be only) index
        self.plotters.toggle_visibility(index)
        print("Picked index:", index)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Isochronous Curve Monitoring'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        QLoggingCategory.setFilterRules('*.warning=false\n*.critical=false') #logging annoying messages
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.plotCanvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.plotCanvas, self)

        # Layout with vertical box
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.plotCanvas)
        self.setCentralWidget(self.widget)

        loadButton = QPushButton('Load Data', self)
        loadButton.clicked.connect(self.load_data)
        self.layout.addWidget(loadButton)

        loadlabelsButton = QPushButton('Load Labels', self)
        loadlabelsButton.clicked.connect(self.load_lables)
        self.layout.addWidget(loadlabelsButton)

        fitButton = QPushButton('(Re)Fit', self)
        fitButton.clicked.connect(self.recompute_fit)
        self.layout.addWidget(fitButton)

        exitButton = QPushButton('Exit', self)
        exitButton.clicked.connect(QCoreApplication.instance().quit)
        self.layout.addWidget(exitButton)

    def load_data(self):
        simulated_file, _ = QFileDialog.getOpenFileName(self, "Select Simulated Data File", "", "ODS Files (*.ods)")
        experimental_file, _ = QFileDialog.getOpenFileName(self, "Select Experimental Data File", "", "NPZ Files (*.npz)")
        if simulated_file and experimental_file:
            try:
                self.imported_data = ImportData._import(simulated_file, experimental_file, 10)  # 10 is the sheet index
                self.iso_data = IsoCurve.create_object(self.imported_data.simulated_data, self.imported_data.experimental_data)
                self.plotCanvas.plotters.marker_visibility = [True] * np.shape(self.iso_data.iso_data)[0]
                self.controller(self.iso_data)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load or process data: {str(e)}")
                raise e

    def controller(self, iso_data, fitted_indexes = None, fig = False):
        if fitted_indexes is not None:
            iso_data.fit_indices = fitted_indexes
        iso_data.create_fit_properties()

        self.plotCanvas.plotters.mean_freq = np.asarray(iso_data.iso_data[:, 1], dtype=float) * 1e-6
        self.plotCanvas.plotters.sigma_freq = np.asarray(iso_data.iso_data[:, 3], dtype=float)
        self.plotCanvas.plotters.sigma_freq_err = np.asarray(iso_data.iso_data[:, 4], dtype=float)
        self.plotCanvas.plotters.names = iso_data.iso_data[:, 0]
        self.plotCanvas.plotters.xfit = iso_data.fit_range * 1e-6
        self.plotCanvas.plotters.yfit = iso_data.fit_values
        self.plotCanvas.plotters.fit_parameters = iso_data.fit_parameters
        #self.plotCanvas.plotters.fitted_indexes = iso_data.fit_indices

        self.plotCanvas.plotters.update_plot(fig = fig)

    def recompute_fit(self):
        """ Recalculate the fit using only visible data points and update the plot. """
        #after toggling 
        new_indices = self.plotCanvas.plotters.update_indexes()
        self.controller(self.iso_data, fitted_indexes = new_indices, fig = True)
    
    def load_lables(self):
        self.plotCanvas.plotters.handle_labels()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())