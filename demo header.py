from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import operator

# This class was generated from the Qt Creator
class Ui_tableView_ex(object):
    def setupUi(self, tableView_ex):
        tableView_ex.setObjectName("tableView_ex")
        tableView_ex.resize(800, 600)
        self.centralwidget = QWidget(tableView_ex)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.myTable = QTableView(self.centralwidget)
        self.myTable.setObjectName("monTablo")
        self.gridLayout.addWidget(self.myTable, 0, 0, 1, 1)
        tableView_ex.setCentralWidget(self.centralwidget)

        self.retranslateUi(tableView_ex)
        QMetaObject.connectSlotsByName(tableView_ex)

    def retranslateUi(self, tableView_ex):
        _translate = QCoreApplication.translate
        tableView_ex.setWindowTitle(_translate("tableView_ex", "MainWindow"))


class TableTest(QMainWindow, Ui_tableView_ex):
    def __init__(self, parent=None):
        super(TableTest, self).__init__(parent)
        self.setupUi(self)

        self.model = TableModel()
        self.myTable.setModel(self.model)
        self.myTable.setShowGrid(False)

        self.hView = HeaderView(self.myTable)
        self.myTable.setHorizontalHeader(self.hView)
        self.myTable.verticalHeader().hide()

        # adding alternate colours
        self.myTable.setAlternatingRowColors(True)
        self.myTable.setStyleSheet("alternate-background-color: rgb(209, 209, 209)"
                                   "; background-color: rgb(244, 244, 244);")

        # self.myTable.setSortingEnabled(True)
        # self.myTable.sortByColumn(1, Qt.AscendingOrder)


class HeaderView(QHeaderView):
    def __init__(self, parent):
        QHeaderView.__init__(self, Qt.Horizontal, parent)
        self.model = TableModel()
        self.setModel(self.model)

        # Setting font for headers only
        self.font = QFont("Helvetica", 12)
        self.setFont(self.font)

        # Changing section backgroud color. font color and font weight
        self.setStyleSheet("::section{background-color: pink; color: green; font-weight: bold}")

        self.setSectionResizeMode(1)
        self.setSectionsClickable(True)


class TableModel(QAbstractTableModel):

    def __init__(self):
        QAbstractTableModel.__init__(self)
        super(TableModel, self).__init__()

        self.headers = ["Name", "Age", "Grades"]
        self.stocks = [["George", "26", "80%"],
                       ["Bob", "16", "95%"],
                       ["Martha", "22", "98%"]]
        self.data = pd.DataFrame(self.stocks, columns=self.headers)

    def update(self, in_data):
        self.data = in_data

    def rowCount(self, parent=None):
        return len(self.data.index)

    def columnCount(self, parent=None):
        return len(self.data.columns.values)

    def setData(self, index, value, role=None):
        if role == Qt.EditRole:
            row = index.row()
            col = index.column()
            column = self.data.columns.values[col]
            self.data.set_value(row, column, value)
            self.update(self.data)
            return True

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data.iloc[row, col]
            return value

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.data.columns.values[section]

# -----------------NOT WORKING!!!---------------
# =================================================

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self.data = sorted(self.data, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.data.reverse()
        self.layoutChanged.emit()
# =================================================


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    main_window = TableTest()
    main_window.show()
    app.exec_()
    sys.exit()