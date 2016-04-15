#!/usr/bin/python
import sys
import GA_gui
from PyQt4 import QtGui


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = GA_gui.Gui()
    
    print ex.getAttributes()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()