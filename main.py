# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 01:52:19 2022

@author: lynat
"""
from PyQt5.QtCore import QAbstractTableModel, Qt, QAbstractListModel
#from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5 import QtWidgets, uic
import sys
import struct
cfg = []
typeStruct = {'int32':'I','float':'f', 'double':'d', 'long':'l', 'int':'i', 'int64':'q'}
uSpace = (b'\x00\x00').decode('utf-16')
game = "JD"
path = "data/elements.data"

log = open('log.txt', 'w', encoding='utf8')

def cfg2py(txt):
    strStruct = ''
    num=[1]
    typ=[typeStruct[txt[0]]]
    for n in txt[1:]:
        if n.startswith('wstring'):
            typ.append(n[8:] + 's')
            num.append(1)
        elif n in typeStruct:
            if typeStruct[n]==typ[-1]:
                num[-1]+=1
            else:
                typ.append(typeStruct[n])
                num.append(1)
        else:
            print(n, 'Unknow type struct')
            
    for n in range(len(typ)):
        if num[n]>1:
            strStruct+= str(num[n])+typ[n]
        else:
            strStruct+= typ[n]
            
    return strStruct
    
def cfgLoad():
    global cfg
    x = open(r'G:\users\Downloads\source El\sELedit\configs\JD_reborn_17class_v168.cfg', 'r', encoding='utf8', errors='ignore').read().split('\n')
    
    for j in range(3,len(x), 5):
        tbl_Name = x[j]
        tbl_Step = int(x[j+1])-4
        tbl_Item = x[j+2].split(';')
        tbl_Type = x[j+3].split(';')
        tbl_PySt = cfg2py(tbl_Type)
        cfg.append([tbl_Name, tbl_Step,tbl_Item, tbl_Type, tbl_PySt])


def data2list(data, size, itemStruct):
    print(size[0], struct.calcsize(itemStruct),itemStruct)
    ls = []
    for i in range(size[1]):
        sData = data[i*size[0]:(i+1)*size[0]]
        ls.append(struct.unpack(itemStruct, sData))
    return ls

cfgLoad()
list_tbl = [x[0] for x in cfg]
el_tbl = []
with open('elements.data', 'rb') as f:
    hdr = f.read(4)
    for n in range(5):
        cf=cfg[n]
        tbl = []
        tbl_pass = f.read(cf[1])
        tbl_size = struct.unpack('<II', f.read(8))
        print(f.tell(),tbl_size,cf[1],cf[0])
        for item in range(tbl_size[1]):
            tbl.append(list(struct.unpack(cf[4], f.read(tbl_size[0]))))
        el_tbl.append(tbl)

class TodoModel(QAbstractListModel):
    def __init__(self, _todos):
        super().__init__()
        self.todos = _todos

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.todos[index.row()]

    def rowCount(self, index):
        return len(self.todos)


class PandasModel(QAbstractTableModel):
    def __init__(self, data, header):
        super().__init__()
        self._data = data
        self.hdr = header

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                if type(value)==bytes:
                    return value.decode('utf-16le').rstrip(uSpace)
                else:
                    return value

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            if type(self._data[index.row()][index.column()])==bytes:
                self._data[index.row()][index.column()] = bytes(value, 'utf-16')
            else:
                self._data[index.row()][index.column()] = value
            return True
        return False
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # return self.hdr[section]
                if section<len(self.hdr):
                    return self.hdr[section]
                else:
                    return 'unk'

class Ui(QtWidgets.QMainWindow):
    global el_tbl
    data = el_tbl[3]
    data[0][1]=112
    hdr = cfg[3][2]
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        self.mnExport.triggered.connect(self.printButtonPressed)
        self.btnSave.clicked.connect(self.saveTbl)
        
        self.tblModel = TodoModel(list_tbl)
        self.lsName.setModel(self.tblModel)

        self.model = PandasModel(self.data, self.hdr)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

        self.show()
        
    def saveTbl(self):
        self.data = [
            [12, 'So 9', 2,4],
            [12, 'so 0', -1,6],
            [33, 'Five 5', 2,3],
            [31, 'ss 3', 2,5],
            [53, 'pt 8', 9,9]
        ]
        self.model = PandasModel(self.data, self.hdr)
        self.table.setModel(self.model)
        
    def printButtonPressed(self):
        # This is executed when the button is pressed
        print(self.data)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()