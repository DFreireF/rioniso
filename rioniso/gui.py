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
        self.iso_data = None
        #self.fit_range = None
        #self.fit_values = None
        #self.fit_parameters = None
        self.visibility = None
        self.fit_line, = self.axes.plot([], [], 'r-', visible=False)
        self.points = None  # To store the scatter plot references
        #self.cid = self.mpl_connect('pick_event', self.on_pick)

    def plot_data(self, iso_data, fit_range, fit_values, fit_parameters):

        self.iso_data = iso_data
        self.fit_range = fit_range
        self.fit_values = fit_values
        self.fit_parameters = fit_parameters
        self.visibility = np.ones(iso_data.shape[0], dtype=bool)

        self.axes.clear()  # Clear existing plot
        self.axes.plot(fit_range, fit_values, 'r-', label='Fit')

        # Plot data points with picker set to True for interactivity
        self.points = self.axes.scatter(iso_data[:, 1].astype(float), iso_data[:, 3].astype(float), color='blue', picker=5)
        self.axes.legend()
        self.draw()

    def on_pick(self, event):
        """ Toggle visibility of picked data points. """
        ind = event.ind[0]  # index of the picked point
        self.visibility[ind] = not self.visibility[ind]  # Toggle visibility
        self.update_plot()
    
    def update_plot(self):
        colors = ['blue' if vis else 'none' for vis in self.visibility]
        self.points.set_facecolors(colors)
        self.draw()
    
    def compute_fit(self):#MODIFY
        """ Recalculate the fit using only visible data points and update the plot. """
        if self.iso_data is None:
            return
        # Filter data points that are visible
        filtered_data = self.iso_data[self.visibility, :]
        x = filtered_data[:, 1].astype(float)
        y = filtered_data[:, 3].astype(float)
        # Simple linear fit for demonstration
        
        fit_params = np.polyfit(x, y, 1)
        fit_line = np.poly1d(fit_params)
        self.fit_line.set_data(x, fit_line(x))
        self.fit_line.set_visible(True)
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

        fitButton = QPushButton('Compute Fit', self)
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
                iso_data = IsoCurve(imported_data.simulated_data, imported_data.experimental_data)
                plots = Plotters(iso_data.iso_data, iso_data.fit_range, iso_data.fit_values, iso_data.fit_parameters)
                self.plotCanvas.update_plot(iso_data.iso_data, iso_data.fit_range, iso_data.fit_values, iso_data.fit_parameters)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load or process data: {str(e)}")
                raise e

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())