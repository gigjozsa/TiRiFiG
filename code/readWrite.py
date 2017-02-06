# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:26:40 2016

@author: samuel
"""

#import statements
from matplotlib import pyplot as plt
import numpy as np

#fetch content of .def file and assign to variable data
with open('/home/samuel/software/TiRiFiC/tirific_2.3.4/tirific_example/eso121-g6_in_first_input.def') as f:
    data = f.readlines()
 
#fetch the value of VROT in .def file
for i in data:
    lineVals = i.split()
    for j in range(len(lineVals)):
        if lineVals[j]=="VROT=":
            VROTval = lineVals[j+1:]
            break
            break

#fetch the value of RADI in .def file
for i in data:
    lineVals = i.split()
    for j in range(len(lineVals)):
        if lineVals[j]=="RADI=":
            RADIvals = lineVals[j+1:]
            break
            break


#convert string values to int
for i in range(len(RADIvals)):
    RADIvals[i]=int(RADIvals[i])

for i in range(len(VROTval)):
    VROTval[i]=int(VROTval[i])

def moveGraph():
    a=int(input('Enter the move value for x: '))
    b=int(input('Enter the move value for y: '))
    return a,b
moveVals = moveGraph()

#define new data points from the user input
for i in range(len(RADIvals)):
    RADIvals[i] = RADIvals[i] + moveVals[0]
for i in range(len(VROTval)):
    VROTval[i] = VROTval[i] + moveVals[1]

plt.plot(RADIvals, VROTval*len(RADIvals))
