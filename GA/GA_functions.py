#!/usr/bin/python

import math
import random

first = []
part = []
flag = False
cnt = 0


def solveSumOne(x):
    return x*x


def solveSumTwo(x):
    i = x*x
    j = 10 * math.cos(2 * math.pi * x)    
    return i - j


def solveSumThree(x):
    global flag
    global part
    
    i = math.sqrt(math.fabs(x))
    ret = x * math.sin(i)
    
    if not flag:
        part.append(x)
        part.append(ret)
    
    return ret


#---------------------
    
def functionOne(genomList):
    x = 0    
    for i in genomList:
        x = x + solveSumOne(i)    
    return x


def functionTwo(genomList):
    d = len(genomList)
    x = 0    
    for i in genomList:
        x = x + solveSumTwo(i)    
    return 10 * d + x


def functionThree(genomList):
    global first
    global flag
    global cnt
    global part
    
    constant = 418.9829
    d = len(genomList)
    x = 0    
    for i in genomList:
        x = x + solveSumThree(i) 
        
        
    
    ret = (d * constant) - x
    
    if not flag:
        part.append(ret)        
        cnt = cnt + 1
        first.append(part)
        part = []
        
        if not cnt < 100:
            flag = True
            for i in first:
                print i
    
    return ret




#--------------------
#func        - number of function to use
#genomList   - list of genom values for all dimension
#domain      - domain of valid coordinates

funcDict = {1 : functionOne, 2 : functionTwo, 3 : functionThree, 4 : functionThree}
        
def getFitness(func_no, genomList):
    
    
    func = funcDict[func_no]
    d = len(genomList)              #dimension   

    x = func(genomList)
       
    return x     #gets fitness

        
