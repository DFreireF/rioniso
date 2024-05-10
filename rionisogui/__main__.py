import sys
from PyQt5.QtWidgets import QApplication
from rionisogui.gui import App

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
