#!/usr/bin/python
import sys
from PyQt4 import QtGui, QtCore

count = 1  
 
class Gui(QtGui.QWidget):
    
    def __init__(self):
        super(Gui, self).__init__()
        
        self.initUI()
        

 
    def initUI(self):
        
        
        #------------- LAYOUTS --------------
                
        
        self.row0_formula_options_layout = QtGui.QHBoxLayout()
        
        self.row1_dimension_layout = QtGui.QGridLayout()
        
        row1_dim_options = QtGui.QHBoxLayout() #unimportant, partial -> local
                
        row2_vbox1 = QtGui.QVBoxLayout()        
        row2_vbox2 = QtGui.QVBoxLayout()
        
        self.row2_options_layout = QtGui.QHBoxLayout()
        
        self.mainLayout = QtGui.QVBoxLayout()
       
        
        #------------FORMULA OPTIONS----------
        
        formula_lab = QtGui.QLabel()
        formula_lab.setText("Fitness func.")
        
        self.options=QtGui.QButtonGroup() # Number group
        
        r0=QtGui.QRadioButton("1")
        r0.setChecked(True)
        r1=QtGui.QRadioButton("2")
        r2=QtGui.QRadioButton("3")
        r3=QtGui.QRadioButton("4")
        
        self.options.addButton(r0)
        self.options.setId(r0,1)
        self.options.addButton(r1)
        self.options.setId(r1,2)
        self.options.addButton(r2)
        self.options.setId(r2,3)
        self.options.addButton(r3)
        self.options.setId(r3,4)
        
        self.row0_formula_options_layout.addWidget(formula_lab)
        self.row0_formula_options_layout.addWidget(r0)
        self.row0_formula_options_layout.addWidget(r1)
        self.row0_formula_options_layout.addWidget(r2)
        self.row0_formula_options_layout.addWidget(r3)

        #-----------DIMENSION OPTIONS ---------------
        add_button = QtGui.QPushButton("Add Dimension")
        add_button.clicked.connect(self.add)
        
        dim_no1 = QtGui.QLabel()
        dim_no1.setText("1:  ") #string with dimension cnt
        
        dim_min1 = QtGui.QLineEdit(self)
        
        print dim_min1
        dim_max1 = QtGui.QLineEdit(self)
        
        dim_min_lab1 = QtGui.QLabel()
        dim_min_lab1.setText("Min:")
        
        dim_max_lab1 = QtGui.QLabel()
        dim_max_lab1.setText("Max:")
        
        
        
        #------------TEXT FIELDS -----------  
        
        self.box1 = QtGui.QLineEdit(self)        
        self.box2 = QtGui.QLineEdit(self)
        self.box3 = QtGui.QLineEdit(self)
        self.box4 = QtGui.QLineEdit(self)
        
        
        lab1 = QtGui.QLabel()
        lab1.setText("Iteration count:")
        
        lab2 = QtGui.QLabel()
        lab2.setText("Population size:")
        
        lab3 = QtGui.QLabel()
        lab3.setText("Mutation probability:")
        
        lab4 = QtGui.QLabel()
        lab4.setText("Bit array length:")

        
        #----------START BUTTON-------------
        
        start_button = QtGui.QPushButton("START")
        start_button.clicked.connect(self.start)
        
        
        #----------FILLING LAYOUTS --------------
        
        row1_dim_options.addWidget(dim_no1)
        row1_dim_options.addWidget(dim_min_lab1)
        row1_dim_options.addWidget(dim_min1)
        row1_dim_options.addWidget(dim_max_lab1)
        row1_dim_options.addWidget(dim_max1)
        
        self.row1_dimension_layout.addWidget(add_button,0,0)
        self.row1_dimension_layout.addLayout(row1_dim_options,0,1)
        
        
                
        row2_vbox1.addWidget(lab1)
        row2_vbox1.addWidget(lab2)
        row2_vbox1.addWidget(lab3)
        row2_vbox1.addWidget(lab4)
        
        row2_vbox2.addWidget(self.box1)
        row2_vbox2.addWidget(self.box2)
        row2_vbox2.addWidget(self.box3)
        row2_vbox2.addWidget(self.box4)
        row2_vbox2.addWidget(start_button)
        
        self.row2_options_layout.addLayout(row2_vbox1)
        self.row2_options_layout.addLayout(row2_vbox2)
        
        self.mainLayout.addLayout(self.row0_formula_options_layout)
        self.mainLayout.addLayout(self.row1_dimension_layout)
        self.mainLayout.addLayout(self.row2_options_layout)
        
        self.setLayout(self.mainLayout)
 
    #---------Window settings --------------------------------
         
        self.setGeometry(300,300,280,170)
        self.setWindowTitle("")
        self.setWindowIcon(QtGui.QIcon(""))
        self.setStyleSheet("background-color:")
        self.show()
        
    def add(self):
        global count
        
        #text fields
        dim_min = QtGui.QLineEdit(self) 
        dim_max = QtGui.QLineEdit(self)
        
        #labels to text fields
        dim_no = QtGui.QLabel()
        dim_no.setText(str(count) + ":  ") #string with dimension cnt
        dim_min_lab = QtGui.QLabel()
        dim_min_lab.setText("Min:")        
        dim_max_lab = QtGui.QLabel()
        dim_max_lab.setText("Max:")        
        
        #adds min and max labels & text fields
        row1_dim_options = QtGui.QHBoxLayout()
        row1_dim_options.addWidget(dim_no)
        row1_dim_options.addWidget(dim_min_lab)
        row1_dim_options.addWidget(dim_min)
        row1_dim_options.addWidget(dim_max_lab)
        row1_dim_options.addWidget(dim_max)
        
        self.row1_dimension_layout.addLayout(row1_dim_options,count,1)
    
        count += 1
        
        
    def getAttributes(self):
        global count
        
        attr_dict = {}
        
        #FITNESS FUNC ID
        attr_dict["fitness"] = self.options.checkedId()
        
        #DIMENSION CNT
        attr_dict["dim_cnt"] = count  #removing last increment
        
        #ATTRIBUTES OF DIMENSIONS
        dim_attr_list = []
        
        for i in range(0, count):
            #gets layout with respective dimension
            box = self.row1_dimension_layout.itemAtPosition(i, 1)
            
            print self.row1_dimension_layout.rowCount()
            
            #lineEdit with minimum 2nd element of layout
            minimum = box.itemAt(2).widget().text()
            minimum = str(minimum)

            #lineEdit with maximum 4rd element of layout
            maximum = box.itemAt(4) .widget().text()
            maximum = str(maximum)
            
            #TODO: overit, ze je vstup spravny vcetne prazdnosti
            
            dim_attr_list.append([minimum,maximum])
            
        attr_dict["dim_attr_list"] = dim_attr_list
        
        
        #ITERATION CNT
        txt = str(self.box1.text())
        attr_dict["iteration_cnt"] = txt
        
        #POPULATION SIZE
        txt = str(self.box2.text())
        attr_dict["population_size"] = txt
        
        #MUTATION PROBABILITY
        txt = str(self.box3.text())
        attr_dict["mutation probability"] = txt
        
        #BIT ARRAY LENGTH
        txt = str(self.box4.text())
        attr_dict["bit_array_length"] = txt

        
        return attr_dict
    
    def start(self):
        attr_dict = self.getAttributes()
        print attr_dict

