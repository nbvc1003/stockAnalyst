from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QApplication, QWidget, QTableWidget, QTableWidgetItem
import sys
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Tables"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400

        self.qtd_rows = 100

        self.table_widget = QTableWidget()

        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.creating_tables()
        self.show()

    def creating_tables(self):
        self.table_widget = QTableWidget()
        self.table_widget.setAutoScroll(True)
        self.table_widget.setRowCount(self.qtd_rows)
        self.table_widget.setColumnCount(2)

        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        vbox = QVBoxLayout()

        for text, slot in (('SrollUp', self.btn_scroll_up), ("PageUp", self.btn_page_up), ("PageDown", self.btn_page_down), ('SrollDown', self.btn_scroll_down)):
            button = QPushButton(text)
            vbox.addWidget(button)
            button.clicked.connect(slot)

        for i in range(0, self.qtd_rows):
            self.table_widget.setItem(i, 0, QTableWidgetItem("Name_" + str(i)))
            self.table_widget.setItem(i, 1, QTableWidgetItem("Email"))

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(self.table_widget)

        hBox = QHBoxLayout()
        hBox.addLayout(vBoxLayout)
        hBox.addLayout(vbox)

        self.setLayout(hBox)

    def btn_page_up(self):
        self.table_widget.scrollToTop()

    def btn_page_down(self):
        self.table_widget.scrollToBottom()

    def btn_scroll_up(self):
        scrollBar = self.table_widget.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() - scrollBar.singleStep() * 10)


    def btn_scroll_down(self):
        scrollBar = self.table_widget.verticalScrollBar()
        scrollBar.setValue(scrollBar.value() + scrollBar.singleStep() * 10)



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())