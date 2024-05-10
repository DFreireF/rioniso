import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QLoggingCategory, QCoreApplication
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backend_bases import PickEvent
import matplotlib.pyplot as plt

from rioniso.model import IsoCurve
from rioniso.importdata import ImportData
from rioniso.plotters import Plotters

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.plotters = Plotters(width=10, height=6, dpi=300, fs = 14)  # Initialize Plotters
        super().__init__(self.plotters.fig)
        self.setParent(parent)
        self.plotters.fig.canvas.mpl_connect('pick_event', self.on_pick)

    def on_pick(self, event):
        """ Toggle visibility of picked data points. """
        self.plotters.handle_events(event)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Isochronous Curve Monitoring'
        self.left = 100
        self.top = 100
        self.width = QDesktopWidget().screenGeometry(-1).width()
        self.height = QDesktopWidget().screenGeometry(-1).height()
        QLoggingCategory.setFilterRules('*.warning=false\n*.critical=false') #logging annoying messages
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            font-size: 18pt;
            font-family = Times;
        """)

        self.plotCanvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.plotCanvas, self)

        # Layout with vertical box
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.plotCanvas)
        self.setCentralWidget(self.widget)
        
        font = QFont("Times", 15)
        font.setBold(True)

        loadButton = QPushButton('Load Data', self)
        loadButton.setFont(font)
        loadButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #355E3B;
            }
        """)
        loadButton.clicked.connect(self.load_data)

        loadlabelsButton = QPushButton('Toggle Labels', self)
        loadlabelsButton.setStyleSheet("""
            QPushButton {
                background-color: #7ec8e3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0000ff;
            }
        """)
        loadlabelsButton.setFont(font)
        loadlabelsButton.clicked.connect(self.load_lables)

        fitButton = QPushButton('(Re)Fit', self)
        fitButton.setStyleSheet("""
            QPushButton {
                background-color: #7ec8e3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0000ff;
            }
        """)
        fitButton.setFont(font)
        fitButton.clicked.connect(self.recompute_fit)
        exitButton = QPushButton('Exit', self)
        exitButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #821d30;
            }
        """)
        exitButton.setFont(font)
        exitButton.clicked.connect(QCoreApplication.instance().quit)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(loadButton)
        hbox_buttons.addWidget(loadlabelsButton)
        hbox_buttons.addWidget(fitButton)
        hbox_buttons.addWidget(exitButton)    
        self.layout.addLayout(hbox_buttons)

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

    def controller(self, iso_data, fitted_indexes = None):
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

        self.plotCanvas.plotters.update_plot()

    def recompute_fit(self):
        """ Recalculate the fit using only visible data points and update the plot. """
        #after toggling 
        new_indices = self.plotCanvas.plotters.update_indexes()
        self.controller(self.iso_data, fitted_indexes = new_indices)
    
    def load_lables(self):
        self.plotCanvas.plotters.handle_labels()