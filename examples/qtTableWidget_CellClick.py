
import sys

import os
from subprocess import Popen, PIPE
from PyQt5.QtWidgets import *


class Root(QMainWindow):
    def __init__(self, parent=None):
        print('  self.__init__ - Initializes QMainWindow')
        QMainWindow.__init__(self, parent)
        # Create Table Widget
        self.filesTable = QTableWidget()
        self.filesTable.cellClicked.connect(self.updateUiCellClick)

        # Init Table Widget
        self.filesTable.clear()
        self.filesTable.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.filesTable.setColumnCount(4)
        self.filesTable.setHorizontalHeaderLabels(['Name', 'TimeStamp', 'Type', 'ls -l'])
        # Init Widgets

        self.setCentralWidget(self.filesTable)
        self.populate_table("/")

    def populate_table(self, path):
        # Verify that it is a directory.
        if not os.path.isdir(path):
            return

        os.chdir(path)
        current_items = os.listdir()
        print(current_items)
        currentItemsLsProcess = Popen(['notepad.exe', '-l'], stdout=PIPE, stderr=PIPE)


        currentItemsLsProcessResult = currentItemsLsProcess.communicate()
        if currentItemsLsProcessResult[1].decode('utf-8'):
            QMessageBox.warning(self, 'Files - ls -l Error',
                                'ls -l responded with non-blank stderr.Error is shown here:'
                                '<br><code>{}</code><br><hr><br>Error LsStderr (e-lsstderr)<br>'
                                '<hr><br>If you want to support the team, go to the '
                                '<a href="https://github.com/">GitHub Repository</a>.'.format(
                                    currentItemsLsProcessResult[1].decode('utf-8')))
            return

        self.filesTable.clear()
        currentItemsLs = currentItemsLsProcessResult[0].decode('utf-8').split('\n')[1:-1]
        self.filesTable.setRowCount(len(current_items))

        for i, values in enumerate(zip(current_items, currentItemsLs)):
            name, ls = values
            self.filesTable.setItem(i, 0, QTableWidgetItem(name))
            self.filesTable.setItem(i, 3, QTableWidgetItem(ls))

        self.setWindowTitle('{}'.format(path))

    def updateUiCellClick(self, row, _):
        path = os.path.join(os.getcwd(), self.filesTable.item(row, 0).text())
        self.populate_table(path)


if __name__ == '__main__':
    print('i Execute instance')
    app = QApplication(sys.argv)
    root = Root()
    root.show()
    status = app.exec_()
    print(' | Done')
    sys.exit(status)