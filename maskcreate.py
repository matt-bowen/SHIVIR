#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:09:56 2017

@author: matt

Creates a Circ FITS mask from a .circ text file
"""


from astropy.io import fits
import numpy as np
import sys

def read(filename):
    new = []
    with open(filename, 'r') as file:
        for line in file:
            line.strip()
            splitLine = line.split()
            if splitLine:
                new.append(line)
    file.close()
    for i, line in enumerate(new):
        newline = []
        line = line[1:]
        for possible_float in line.split(' '):
            possible_float.replace(' ','')
            if possible_float:
                possible_float.replace('\n','')
                newline.append(possible_float.rstrip())
        new[i] = newline
    for i, line in enumerate(new):
        newline = [float(line[0]), float(line[1]), float(line[2])]
        new[i] = newline
    return(new)
    
def makemask(radius):
    radius = int(radius)-1
    y,x = np.ogrid[-radius:radius+1,-radius:radius+1]
    mask =  x**2 + y**2 <= radius**2
    mask = 1*mask.astype(int)
    #print(mask)
    indices = []
    for (x,y), value in np.ndenumerate(mask):
        if value == 1:
            indices.append([x,y])
    return(indices)
    
    
    
f = fits.open(sys.argv[1]) #sys.argv[1] = VCC????-I-Flag.fits
data = f[0].data
dims = data.shape
f.close()
#print(dims)

#new array of zeros
data = np.ndarray(shape=dims)
data.fill(0)

new = read(sys.argv[2]) #sys.argv[2] = VCC????-I-Image.aedit.circ
for line in new:
    indices = makemask(line[2])

    for coords in indices:
        x = int(coords[0]+line[0]-int(line[2])+1)
        y = int(coords[1]+line[1]-int(line[2])+1)
        if x < dims[0] and y < dims[1]:
            data[x,y] = 1
    
hdu = fits.PrimaryHDU(data)
hdu.writeto(sys.argv[3]) #sys.argv[3] = VCC????-I-Flag-Circ.fits
    








