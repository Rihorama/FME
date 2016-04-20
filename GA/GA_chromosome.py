#!/usr/bin/python
import random

class Chromosome:
    
    dim_cnt = 0
    length = 0
    maximum = 0
    minimum = 0
    isSet = False
    
    def __init__(self,dim,l,mi,ma):
        
        self.fitness = False
        
        #first chromosome sets class variables
        
        if not Chromosome.isSet:
            Chromosome.dim_cnt = dim
            Chromosome.length = l
            Chromosome.minimum = mi #list of minima for resp dimensions
            Chromosome.maximum = ma #list of maxima for resp dimensions
            Chromosome.isSet = True
            
        self.decimal = []  #list of integers
        self.binary = []   #list of lists representing binary number
        
        for i in range(0,Chromosome.dim_cnt):
            self.createDimension(i)
                
        
    #creates one dimension and appends its dec and bin represetnation
    #to the respective lists
    def createDimension(self,i):

        dim_min = Chromosome.minimum[i]
        dim_max = Chromosome.maximum[i]
        
        #generates an integer in the range
        myself = random.randint(dim_min,dim_max)
        
        self.decimal.append(myself)
        self.binary.append(self.makeBinary(myself))
        
        return
    
    
    #reverses gene value
    #if it would mean exceeding boundaries, nothing happens
    def swapGene(self,dim_i,gene_i):
        
        old_gene = self.binary[dim_i][gene_i]        
        new_gene = (old_gene + 1) % 2
                
        self.changeGene(dim_i,gene_i,new_gene,old_gene)
        
        return old_gene
    
    
    
    
    #if we change a gene somewhere
    #the dimension binary value might fall out of allowed range
    #this method checks the gene change and if ok
    #also executes the change to both binary and decimal representation
    #and returns true, else false
    def changeGene(self,dim_i,gene_i,new_gene,old_gene):
        
        dimension = self.decimal[dim_i] #decimal value of dimension
        
        #if the change is 1 -> 0, the value decreases
        #we subtract 2^index from the value to compute the change
        #then we compare it with the minimum, if less -> false
        if old_gene > new_gene:
            alt_decimal = dimension - pow(2,gene_i)
            
            if alt_decimal < Chromosome.minimum[dim_i]:
                return False
            else:
               self.decimal[dim_i] = alt_decimal
               self.binary[dim_i][gene_i] = new_gene
               return True
        
        #if the change is 0 -> 1, the value increases
        #we check for maximum
        else:
            alt_decimal = dimension + pow(2,gene_i)
            
            if alt_decimal > Chromosome.maximum[dim_i]:
                return False
            else:
               self.decimal[dim_i] = alt_decimal
               self.binary[dim_i][gene_i] = new_gene
               return True
        
    #takes integer, returns list of 0 and 1 representing its binary
    #form
    def makeBinary(self,i):

        i = str(bin(i))
        i = i[2:]         #cuts the "0b"

        binary = []
        
        for x in reversed(i):
            binary.append(int(x))
        
        #cuts msb if binary length exceeds limit
        if Chromosome.length < len(binary):
            return binary[:Chromosome.length]
        
        #else adds zeros to meet the limit
        for x in range(Chromosome.length - len(binary)):
            binary.append(0)
            
        return binary    
    
    
    #gets a list representing binary number - returns its decimal value
    def makeDecimal(self,b):
        
        decimal = 0
        
        for i in range(0, len(b)):
            decimal = decimal + b[i]*pow(2,i) 
            
            
        return decimal
    
    
    
    
    def printBinary(self):
        
        for i in range(0,Chromosome.dim_cnt):
            bin_num = bin(self.decimal[i])
            print "  Dimension " + str(i)
            print "    " + str(bin_num)[2:]
        
        return
    
    
    #receives and stores given fitness value
    def setFitness(self,fitness):
        
        self.fitness = fitness        
        return
    
    
    #returns fitness value
    def getFitness(self):
        
        return self.fitness
    
    #returns list of decimal values of the chromosome 
    def getDecimal(self):
        
        return self.decimal
    
    
    def getBinary(self):
        
        return self.binary
    
    
    #replaces current binary with newly given binary
    #also updates decimal counterpart
    #also controls the number being within the range
    def setBinary(self,binary):
        
        new_decimal = []
        
        #for that controls each element of binary for bounds
        for x in range(0,len(binary)):
            
            temp_decimal = self.makeDecimal(binary[x])
            
            #if the decimal is out of range, it becomes the limit
            #binary must be updated
            if temp_decimal < self.minimum[x]:
                temp_decimal = self.minimum[x]
                binary[x] = self.makeBinary(temp_decimal)
                
            elif temp_decimal > self.maximum[x]:
                temp_decimal = self.maximum[x]
                binary[x] = self.makeBinary(temp_decimal)
                
            new_decimal.append(temp_decimal) #adds to list of decimals
            
        self.binary = binary
        self.decimal = new_decimal
    
    
        