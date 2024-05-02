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
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def on_pick(self, event):
        """ Toggle visibility of picked data points. """
        ind = event.ind[0]  # index of the picked point
        self.visibility[ind] = not self.visibility[ind]  # Toggle visibility
        self.update_plot()
    
    def update_plot(self):
        colors = ['blue' if vis else 'none' for vis in self.visibility]
        self.points.set_facecolors(colors)
        self.draw()
    
    def compute_fit(self):
        """ Recalculate the fit using only visible data points and update the plot. """
        #after toggling 
        plot_data.update_indexes()

        self.axes.relim()
        self.axes.autoscale_view()
        self.draw()

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

        self.plotCanvas = PlotCanvas(self, width=5, height=4)
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

        fitButton = QPushButton('(Re)Fit', self)
        fitButton.clicked.connect(self.plotCanvas.compute_fit)
        self.layout.addWidget(fitButton)

        exitButton = QPushButton('Exit', self)
        exitButton.clicked.connect(QCoreApplication.instance().quit)
        self.layout.addWidget(exitButton)

    def load_data(self):
        simulated_file, _ = QFileDialog.getOpenFileName(self, "Select Simulated Data File", "", "ODS Files (*.ods)")
        experimental_file, _ = QFileDialog.getOpenFileName(self, "Select Experimental Data File", "", "NPZ Files (*.npz)")
        if simulated_file and experimental_file:
            try:
                imported_data = ImportData._import(simulated_file, experimental_file, 10)  # 10 is the sheet index
                iso_data = IsoCurve.create_object(imported_data.simulated_data, imported_data.experimental_data)
                self.controller(iso_data)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load or process data: {str(e)}")
                raise e

    def controller(self, iso_data, fitted_indexes = None):
                    if fitted_indexes is not None:
                        iso_data.fit_indices = fitted_indexes

                    iso_data.create_fit_properties()

                    plot_data = Plotters.create_object(iso_data.iso_data, iso_data.fit_range,   iso_data.fit_values, iso_data.fit_parameters, iso_data.fit_indices)
                    plot_data.update_plot()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())