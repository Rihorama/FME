#!/usr/bin/python
import random

class Chromosome:
    
    dim_cnt = 0
    length = 0
    maximum = 0
    minimum = 0
    #isSet = False
    mapSeeds = []  #seed for mapping the binary value to the given interval
                   #that is: float(maximum - minimum) / float(pow(2,Chromosome.length))
    
    def __init__(self,dim,l,mi,ma):
        
        self.fitness = False
        
        #first chromosome sets class variables
        
        #if not Chromosome.isSet:
        Chromosome.dim_cnt = dim
        Chromosome.length = l
        Chromosome.minimum = mi #list of minima for resp dimensions
        Chromosome.maximum = ma #list of maxima for resp dimensions
        Chromosome.isSet = True
            
        self.decimal = []  #list of integers
        self.binary = []   #list of lists representing binary number
        
        for i in range(0,Chromosome.dim_cnt):
            
            #creates mapping seed for this dimension
            d = float(Chromosome.maximum[i] - Chromosome.minimum[i])
            seed = d / float(pow(2,Chromosome.length))
            Chromosome.mapSeeds.append(seed)
            
            self.createDimension(i)
                
        
    #creates one dimension and appends its dec and bin represetnation
    #to the respective lists
    def createDimension(self,i):

        dim_min = Chromosome.minimum[i]
        dim_max = Chromosome.maximum[i]
        
        #generates an integer within the bit array range
        binRangeNum = random.randint(0,pow(2,Chromosome.length))
        
        #overflow control
        if binRangeNum == pow(2,Chromosome.length):
            binRangeNum = binRangeNum -1
        
        #now maps the number from binary range to the dimension interval
        mapped = self.mapToInterval(binRangeNum,i)
        
        self.decimal.append(mapped)
        self.binary.append(self.makeBinary(mapped,i))
        
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
    
    
    #takes a positive integer and maps it on given interval
    def mapToInterval(self,number,dim_i):
        
        #print "toInterval: I get: " + str(number)
        
        #what particular number does our binary number stand for in the interval
        #we multiply it with the mapping seed for this dimension
        mapped = Chromosome.minimum[dim_i] + (number * Chromosome.mapSeeds[dim_i])
        
        #print "toInterval: I map: " + str(mapped)
        return mapped
    
    
    #reverse process, mapped float -> positive integer
    def mapToBinRange(self,number,dim_i):
        
        #print "toBinRange: I get: " + str(number)
        
        #we get back the positive integer coming from binary range
        demapped = (number - Chromosome.minimum[dim_i]) / Chromosome.mapSeeds[dim_i]
        
        #print "toBinRange: I map: " + str(demapped)
        
        return int(demapped)
    
    
    
    #takes interval-mapped decimal, maps it back to range, then makes binary of it
    def makeMapBinary(self,number, dim_i):
        
        i = self.mapToBinRange(number,dim_i)
        return self.makeBinary(i)
    
    
    
    #takes already back-mapped decimal, returns list of 0 and 1 representing its binary
    #back-mapped form
    def makeBinary(self,number,dim_i):
        
        #first maps the number back to binary range
        i = self.mapToBinRange(number,dim_i)

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
    
    
    #gets binary, returns its mapped decimal value
    def makeMapDecimal(self,b,dim_i):
        
        decimal = 0
        
        for i in range(0, len(b)):
            decimal = decimal + b[i]*pow(2,i)
            
        mapped = self.mapToInterval(decimal,dim_i)
            
            
        return mapped
    
    #gets a list representing binary number - returns its unmapped decimal value
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
            
            temp_decimal = self.makeMapDecimal(binary[x],x)
            
            #if the decimal is out of range, it becomes the limit
            #binary must be updated
            if temp_decimal < self.minimum[x]:
                temp_decimal = float(self.minimum[x])
                binary[x] = self.makeBinary(temp_decimal,x)
                
            elif temp_decimal > self.maximum[x]:
                temp_decimal = float(self.maximum[x])
                binary[x] = self.makeBinary(temp_decimal,x)
                
            new_decimal.append(temp_decimal) #adds to list of decimals
            
        self.binary = binary
        self.decimal = new_decimal
    
    
        