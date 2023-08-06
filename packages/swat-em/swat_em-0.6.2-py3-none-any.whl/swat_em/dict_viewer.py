# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt5.QtWidgets import  QApplication, QTreeWidget, QTreeWidgetItem

from swat_em.datamodel import datamodel


# A more complex winding (overlapping full pitch winding with coil shortening)
wdg = datamodel()
Q = 12
P = 2
w = 5  # without shortening w would be 6 for this winding
wdg.genwdg(Q=Q, P=P, m=3, layers=2, w=w)
#  print(wdg)



"""
class ViewTree(QTreeWidget):
    def __init__(self, value):
        super().__init__()
        def fill_item(item, value):
            def new_item(parent, text, val=None):
                child = QTreeWidgetItem([text])
                fill_item(child, val)
                parent.addChild(child)
                child.setExpanded(True)
            if value is None: return
            elif isinstance(value, dict):
                for key, val in sorted(value.items()):
                    new_item(item, str(key), val)
            elif isinstance(value, (list, tuple)):
                for val in value:
                    text = (str(val) if not isinstance(val, (dict, list, tuple))
                            else '[%s]' % type(val).__name__)
                    #  new_item(item, text, val) 
                    new_item(item, str(val), None)
            else:
                new_item(item, str(value))

        fill_item(self.invisibleRootItem(), value)

if __name__ == '__main__':

    

    
    #  with open('test.txt', 'w') as f:
        #  f.write(str(wdg.results))

    app = QApplication([])
    window = ViewTree(wdg.results)
    window.show()
    app.exec_()
"""


# Dict-filter functions
def get_flat_keys(data):
    '''
    returns key list from dictionary (flattened)
    '''
    def dict_generator(indict, pre=None):
        # Code from http://stackoverflow.com/questions/12507206/python-recommended-way-to-walk-complex-dictionary-structures-imported-from-json
        pre = pre[:] if pre else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    for d in dict_generator(value, [key] + pre):
                        yield d
                else:
                    yield pre + [key, value]
        else:
            yield indict        
        
    tree = []
    for k in dict_generator(data):
        tree.append(k)
    return tree


def filter_flat_keys(tree, s, respect_cases=False):
    """
    filters the flattened tree with string s
    respect_cases == False --> upper/lower cases aren't respected
    """
    tree2 = []
    for l in tree:
        found = None
        for k in l[:-1]:
            if respect_cases:
                if s in k:
                    found = True
            else:
                if s.upper() in k.upper():
                    found = True
        if found:
            tree2.append(l)
    return tree2



def make_dict(lines):
    '''
    Creates a dictionary from a list of key-lists
    '''
    def add_line(d, line):
        tmp = d
        N = len(line)-1
        i = 0
        for l in line[:-1]:
            if not tmp.has_key(l):
                tmp[l] = {}
            if i < (N-1):
                tmp = tmp[l]
            i += 1
        tmp[l] = line[-1]
        return d
        
    d2 = {}
    for line in lines:
        d2 = add_line(d2, line)
    return d2


def fill_widget(widget, value):
    """
    fills an Qt-treewidget with an dictionary
    
    Parameters
    ----------
    widget : Qt-Widget
             Qt-Treewidget, for data visualisation
    value : dictionary
            data, that has to be displayed
    """
    widget.clear()
    fill_item(widget.invisibleRootItem(), value)





















from PyQt5 import QtGui,QtCore,QtWidgets
import sys

class MainFrame(QtWidgets.QWidget):
    def __init__(self, tree=None):
        QtWidgets.QWidget.__init__(self)

        if tree is None:
            tree = {'RootLevel':{
                        "Level1": {"Level1_item1":14, "Level1_item2":12, "Level1_item3":3.55},
                        "Level2": {
                            "Level2_SubLevel1": {"Level2_SubLevel1_item1":3.52, "Level2_SubLevel1_item2":2.55, "Level2_SubLevel1_item3":13},
                            "Level2_SubLevel2": {"Level2_SubLevel2_item1":2, "Level2_SubLevel2_item2":4, "Level2_SubLevel2_item3":3.11}
                            },
                        "Level3": {"Level3_item1":12, "Level3_item2":13.55, "Level3_item3":122}}
            }

        self.tree = QtWidgets.QTreeView(self)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.tree)

        root_model = QtGui.QStandardItemModel()
        self.tree.setModel(root_model)
        self.tree.model().setHorizontalHeaderLabels(['Level','Values'])
        
        

        txt = "" # str(txt)   # Filter for keys
        tree = get_flat_keys(tree)
        tree2 = filter_flat_keys(tree, txt)
        data = make_dict(tree2)        
        fill_widget(root_model.invisibleRootItem(), data)

        
        
        
        #  self.fill_model_from_json(root_model.invisibleRootItem(), tree)



    #  def fill_model_from_json(self, parent, d):
        #  if isinstance(d, dict):
            #  for key, value in d.items():
                #  it = QtGui.QStandardItem(str(key))
                #  if isinstance(value, dict):
                    #  parent.appendRow(it)
                    #  self.fill_model_from_json(it, value)
                #  else:
                    #  it2 = QtGui.QStandardItem(str(value))
                    #  parent.appendRow([it, it2])




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainFrame(wdg.results)
    main.show()
    sys.exit(app.exec_())
