#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:34:41 2017

@author: matt

Inverts the pixel values in the NGVS pixel masks
"""

from astropy.io import fits
import sys

f = fits.open(sys.argv[1]) #sys.argv[1] = VCC????-I-Flag.fits
data = f[0].data
dims = data.shape
#print(dims)

for x in range(dims[1]):
    for y in range(dims[0]):
        if data[y, x] == 0:
            data[y, x] = 1
        else:
            data[y, x] = 0
        
f.writeto(sys.argv[2]) #sys.argv[2] = VCC???-I-Flag-Invert.fits

#print('done')






