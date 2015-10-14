#!/usr/bin/python

class Node:
    
    def __init__(self,data):
        self.data = data
        self.prev = None
        self.nxt = None        
        
    def setNext(self,node):
        node.prev = self        #prev  -> self
        self.nxt = node        #prev <-> self        
        
    def setPrev(self,node):
        node.nxt = self        #self <-  next
        self.prev = node        #self <-> next        
        
    def clearNext(self):
        self.nxt = None        
        
    def clearPrev(self):
        self.prev = None
        
    def getPrev(self):
        return self.prev
    
    def getNext(self):
        return self.nxt
    
    def getData(self):
        return self.data
    
    def setData(self,data):
        self.data = data






class Circular:
    
    def __init__(self):
        self.head = None
        self.size = 0
        self.active = None
        
        
    #new node added as predecessor of head node (effectively at "the end")   
    #for mass filling
    def addNode(self,data):
        
        node = Node(data)               #creates a new node
        
        if self.head == None:           #list is empty
            self.head = node
            self.head.setNext(node)
            self.head.setPrev(node)
            
        else:
            prev = self.head.getPrev()  #current last node
            prev.setNext(node)          #its new successor is the new node
            self.head.setPrev(node)     #new head's predecessor is the new node
            
            node.setNext(self.head)     #updating new node
            node.setPrev(prev)
        
        self.size += 1
        
        
    #removes the active node if it's set (activity is moved forward)
    #returns removed node data
    def popNode(self):
        
        if self.active and self.size == 1:   #deleting the only node
            node = self.active
            self.head = None
            self.active = None
        
        elif self.active:        
            node = self.active
            prev = node.getPrev()
            nxt = node.getNext()
            
            prev.setNext(nxt)       #removing connections with the deleted node
            nxt.setPrev(prev)
            self.active = nxt       #updating list info
            
            if self.head == node:
                self.head = nxt     #if its head we're deleting, nxt is the new head
                
        self.size -= 1              #decreasing size
        return node.getData()
        
        
    #inserts node as a successor of the active node
    #for modifications
    def insertNode(self,data):
        
        if not self.active:
            print "Insertion failure, active node is not set."
            return
        
        node = Node(data)               #creates a new node
        
        active = self.active
        nxt = active.getNext()
        
        active.setNext(node)   #new successor of active is node
        nxt.setPrev(node)      #prev's new predecessor is node
        
        node.setPrev(active)
        node.setNext(nxt)
        
        self.size += 1
        
    
    #sets activity to head node if there is a head node, returns data
    def resetActive(self):        
        if self.head:            
            self.active = self.head
            
    
    #returns active node data, None if not set
    def getActive(self):
        if not self.active:
            print "getActive: Active node not set, None returned."
            return None
        return self.active.getData()
    
    
    #updates data of the active node it its set
    def updateActive(self,data):        
        if self.active:
            self.active.setData(data)
            
    
    #moves activity to the next node, returns its data, None if not set
    def getNext(self):
        if not self.active:
            print "getNext: Active node not set, None returned."
            return None
        self.active = self.active.getNext()
        return self.active.getData()
    
    
    #moves activity to the previous node, returns its data, None if not set
    def getPrev(self):
        if not self.active:
            print "getPrev: Active node not set, None returned."
            return None
        self.active = self.active.getPrev()
        return self.active.getData()
    
    
    def getSize(self):
        return self.size
    
    
    def printList(self):
        self.resetActive()
        data = self.getActive()
        for i in range(self.size):
            print data
            data = self.getNext()
            
    
    #starts with head node's previous node
    def printListReverse(self):
        self.resetActive()
        data = self.getPrev()
        for i in range(self.size):
            print data
            data = self.getPrev()
            
    
    #finds the first node to the right that has value equal to data
    #true if successful, leaves the node active
    def findFirst(self,data):
        self.resetActive()
        compare = self.getActive()
        for i in range(self.size):
            if compare == data:
                return True
            else:
                compare = self.getNext()
                
                
    #for each value appearing in the list prints how many times it's there
    #returns a dictionary value : count
    def getCounts(self):
        counts = {}
        self.resetActive()
        for i in range(self.size):
            active = self.getActive()
            if active in counts:
                counts[active] += 1
            else:
                counts[active] = 1
            self.getNext()
        return counts
            
            
    def clearList():
        self.head = None
        self.size = 0
  
  
  
            
###MAIN###
import math

circular = Circular()


for i in range (20):
    data = pow(2,i)
    circular.addNode(data)

print "List of first 20 powers of two:" 
circular.printList()



print "\nLets duplicate the odd nodes!"

circular.resetActive()
for i in range(circular.getSize()):
    if not (i % 2 == 0):
        data = circular.getActive()     #gets data
        circular.insertNode(data)       #inserts node with the same data
        circular.getNext()        #extra skip for the new node
    circular.getNext()            #skip to the next node
        
print "\nNew size is " + str(circular.getSize()) + "."
print "The list now looks like this:"
circular.printList()

print"\nLet's print backwards because we can~"
circular.printListReverse()

print "\nI feel an urge to replace the 1024 node with something actual..."
if circular.findFirst(1024):
    circular.updateActive("Soaz xpeked the Nexus in Paris.")
    circular.printList()
    
print "\nNow we shall test the requested counting function, yeehao!"
counted = circular.getCounts()
#lets make it pretty for printing
for i in counted:
    print str(i) + " : " + str(counted[i])



        
        
        
            
            