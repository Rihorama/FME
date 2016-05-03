#!/usr/bin/python
import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import KM_kmeans

count = 1  
 
class Gui(QtGui.QWidget):
    
    def __init__(self):
        super(Gui, self).__init__()
        
        self.initUI()
        

 
    def initUI(self):
        
        
        #------------- LAYOUTS --------------
                
        
        self.row0_formula_options_layout = QtGui.QHBoxLayout()
        
        self.row1_cluster_layout = QtGui.QGridLayout()
        
        row1_cl_options = QtGui.QHBoxLayout() #unimportant, partial -> local
                
        
        self.results_layout = QtGui.QHBoxLayout()
        
        self.row2_file_layout = QtGui.QHBoxLayout()
        
        self.row3_start_layout = QtGui.QHBoxLayout()
        
        self.mainLayout = QtGui.QVBoxLayout()
       
        
        #------------STEPS OPTIONS----------
        
        #formula_lab = QtGui.QLabel()
        #formula_lab.setText("Fitness func.")
        
        #self.options=QtGui.QButtonGroup() # Number group
        
        #r0=QtGui.QRadioButton("1")
        #r0.setChecked(True)
        #r1=QtGui.QRadioButton("2")
        #r2=QtGui.QRadioButton("3")
        #r3=QtGui.QRadioButton("4")
        
        #self.options.addButton(r0)
        #self.options.setId(r0,1)
        #self.options.addButton(r1)
        #self.options.setId(r1,2)
        #self.options.addButton(r2)
        #self.options.setId(r2,3)
        #self.options.addButton(r3)
        #self.options.setId(r3,4)
        
        #self.row0_formula_options_layout.addWidget(formula_lab)
        #self.row0_formula_options_layout.addWidget(r0)
        #self.row0_formula_options_layout.addWidget(r1)
        #self.row0_formula_options_layout.addWidget(r2)
        #self.row0_formula_options_layout.addWidget(r3)

        #-----------CLUSTER OPTIONS ---------------
        add_button = QtGui.QPushButton("Add Cluster")
        add_button.clicked.connect(self.add)
        
        cl_no1 = QtGui.QLabel()
        cl_no1.setText("1:  ") #string with cluster cnt
        
        cl_x = QtGui.QLineEdit(self)        
        cl_y = QtGui.QLineEdit(self)
        cl_z = QtGui.QLineEdit(self)
        
        cl_x_lab = QtGui.QLabel()
        cl_x_lab.setText("x:")
        
        cl_y_lab = QtGui.QLabel()
        cl_y_lab.setText("y:")
        
        cl_z_lab = QtGui.QLabel()
        cl_z_lab.setText("z:")
        
        
        
        #------------LOAD FILE -----------  
        
        self.file_box = QtGui.QLineEdit(self) 
        file_button = QtGui.QPushButton("File")
        file_button.clicked.connect(self.openFile)
        
        
        #lab1 = QtGui.QLabel()
        #lab1.setText("Iteration count:")

        
        lab_empty = QtGui.QLabel()
        lab_empty.setText(" ")

        
        #----------START BUTTON-------------
        
        start_button = QtGui.QPushButton("START")
        start_button.clicked.connect(self.start)
        
        

        
        #----------FILLING LAYOUTS --------------
        
        row1_cl_options.addWidget(cl_no1)
        row1_cl_options.addWidget(cl_x_lab)
        row1_cl_options.addWidget(cl_x)
        row1_cl_options.addWidget(cl_y_lab)
        row1_cl_options.addWidget(cl_y)
        row1_cl_options.addWidget(cl_z_lab)
        row1_cl_options.addWidget(cl_z)
        
        self.row1_cluster_layout.addWidget(add_button,0,0)
        self.row1_cluster_layout.addLayout(row1_cl_options,0,1)  
        
        #self.results_layout.addWidget(self.final_result)
                
        #row2_vbox1.addWidget(lab1)
        #row2_vbox1.addWidget(lab2)
        #row2_vbox1.addWidget(lab3)
        #row2_vbox1.addWidget(lab4)
        #row2_vbox1.addWidget(lab_empty)
        
        #row2_vbox2.addWidget(self.box1)
        #row2_vbox2.addWidget(self.box2)
        #row2_vbox2.addWidget(self.box3)
        #row2_vbox2.addWidget(self.box4)
        #row2_vbox2.addWidget(start_button)
        
        self.row2_file_layout.addWidget(file_button)
        self.row2_file_layout.addWidget(self.file_box)
        
        self.row3_start_layout.addWidget(lab_empty)
        self.row3_start_layout.addWidget(start_button)
        
        
        self.mainLayout.addLayout(self.row0_formula_options_layout)
        self.mainLayout.addLayout(self.row1_cluster_layout)
        self.mainLayout.addLayout(self.row2_file_layout)
        self.mainLayout.addLayout(self.row3_start_layout)
        
        self.setLayout(self.mainLayout)
 
    #---------Window settings --------------------------------
         
        self.setGeometry(400,400,280,100)
        self.setWindowTitle("")
        self.setWindowIcon(QtGui.QIcon(""))
        self.setStyleSheet("background-color:")
        self.show()
    
    
    
    def openFile(self):
        
        self.file_box.setText(QtGui.QFileDialog.getOpenFileName())
    
    
    
    def add(self):
        global count
        
        #text fields
        new_cl_x = QtGui.QLineEdit(self) 
        new_cl_y = QtGui.QLineEdit(self)
        new_cl_z = QtGui.QLineEdit(self)
        
        #labels to text fields
        cl_no = QtGui.QLabel()
        cl_no.setText(str(count+1) + ":  ") #string with dimension cnt
        
        new_cl_x_lab = QtGui.QLabel()
        new_cl_x_lab.setText("x:")
        
        new_cl_y_lab = QtGui.QLabel()
        new_cl_y_lab.setText("y:")
        
        new_cl_z_lab = QtGui.QLabel()
        new_cl_z_lab.setText("z:")      
        
        #adds min and max labels & text fields
        row1_add_clusters = QtGui.QHBoxLayout()
        row1_add_clusters.addWidget(cl_no)
        
        row1_add_clusters.addWidget(new_cl_x_lab)
        row1_add_clusters.addWidget(new_cl_x)
        row1_add_clusters.addWidget(new_cl_y_lab)
        row1_add_clusters.addWidget(new_cl_y)
        row1_add_clusters.addWidget(new_cl_z_lab)
        row1_add_clusters.addWidget(new_cl_z)
        
        
        self.row1_cluster_layout.addLayout(row1_add_clusters,count,1)
    
        count += 1
        
        
    def getAttributes(self):
        global count
        empty = False
        
        self.attr_dict = {}
        
        #CLUSTERS
        cord_x = []
        cord_y = []
        cord_z = []
        
        for i in range(0, count):
            #gets layout with respective cluster
            box = self.row1_cluster_layout.itemAtPosition(i, 1)
            
            #lineEdit with x cord = 2nd element of layout
            x = box.itemAt(2).widget().text()
            x = str(x)
            if x == "":
                empty = True

            #lineEdit with y cord = 4rd element of layout
            y = box.itemAt(4).widget().text()
            y = str(y)
            if y == "":
                empty = True
            
            #lineEdit with z cord = 6th element of layout
            z = box.itemAt(4).widget().text()
            z = str(z)
            
            
            cord_x.append(x)
            cord_y.append(y)
            cord_z.append(z)
            
        self.attr_dict["cords_x"] = cord_x
        self.attr_dict["cords_y"] = cord_y
        self.attr_dict["cords_z"] = cord_z
        
        self.attr_dict["cl_cnt"] = count
        
        #empty centroids in gui means we generate them at random
        if empty:
            self.attr_dict["empty"] = True
        else:
            self.attr_dict["empty"] = False
        
        #FILE
        txt = str(self.file_box.text())
        self.attr_dict["file"] = txt
        
        

        
    #validates given attributes
    def checkAttributes(self):        
         
        try:
            f = open(self.attr_dict["file"], 'r')
            
        except IOError:
            print "Given file cannot be opened."
            return False
        
        points_x = []
        points_y = []
        points_z = []
        
        for line in f:
            cords = line.split(";")
            
            #appending x
            x = int(cords[0].replace("\n", ""))
            points_x.append(x) 
            
            #appending y
            y = int(cords[1].replace("\n", ""))
            points_y.append(y)            
            
            #appending z if given
            if len(cords) == 3:
                z = int(cords[2].replace("\n", ""))
                points_z.append(z)
                
        print points_x
        print points_y
        print points_z
        
        dimension = 3  #default
        
        
        #all x and y cords must be given
        if len(points_x) != len(points_y):
            print "X cord and Y cord count not the same in given file. 2D can't be processed."
            return False        
        
        #third dimension not given or given partly (=wrong)
        elif len(points_x) != len(points_z):
            #means we will be working in 2D
            points_z = []
            self.attr_dict["cords_z"] = [] #removing cluster z coordinates
            dimension = 2        
        
        elif len(points_z) == 0 and len(self.attr_dict["cords_z"]) != 0:
            #we work in 2D while clusters were given a third dimension
            #we remove the third dimension from cluster points
            self.attr_dict["cords_z"] = [] #removing cluster z coordinates
            
            
            
        self.attr_dict["points_x"] = points_x
        self.attr_dict["points_y"] = points_y
        self.attr_dict["points_z"] = points_z
        
        self.attr_dict["dim"] = dimension
        
        return True
    
    
    
    def start(self):
        
        self.getAttributes()
        print self.attr_dict
        
        if not self.checkAttributes():
            return
        
        KM = KM_kmeans.KMeans(self.attr_dict)
        
        
        #if not self.parseAttributes():
        #    print "Attribute failure."
        #    return
        
        #self.GA = GA_algorithm.GeneticAlgorithm(self.attr_dict)
        #data = self.GA.start()
        #pg.plot(data[1])
        
        #string = "Final fitness: " + str(data[1][-1]) + "\nBest fitness: " + str(data[0])
        
        #self.final_result.setText(string)
        #QtGui.QApplication.processEvents()
        

