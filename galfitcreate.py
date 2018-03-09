#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 12:14:06 2018

@author: matt
"""

import re
import sys
        
def processDecomp(galaxy):
    decomp = open("/home/matt/Thesis/Files From Kevin/decompositionValues.txt",'r')
    for line in decomp:
        if re.match(galaxy+"((?!plus|minus).*)", line):
            decompVals = line
            
    decompVals = decompVals.split(" ")
    for i, j in enumerate(decompVals):
        if j[0].isdigit():
            decompVals[i] = float(j)
            
    decompDict = {'galaxy': decompVals[0], 'mu_e1': decompVals[1],
                  'r_e1': decompVals[4], 'n1': decompVals[7],
                  'mu_e2': decompVals[10], 'r_e2': decompVals[13],
                  'mu_e3': decompVals[16], 'r_e3': decompVals[19],
                  'n3': decompVals[22]}
    return decompDict
    
def processProf(galaxy):
    path = "/home/matt/Thesis/Working Sources/SHIVIR/"+galaxy+"/"+galaxy+"-I-Image_mag_cut3.prof"
    for line in open(path, 'r'):
        line = line.split(" ")
        newline=[]
        for i in line:
            if i != "":
                newline.append(i)
                newline[-1].replace("\n",'')
                try:
                    newline = [float(i) for i in newline]
                except ValueError:
                    pass
            try:
                if int(newline[0]) == 5: #take PA at ~5 arcsec for bulge
                    PA5 = newline[4]
                    ellip5 = newline[3]
            except (IndexError, ValueError):
                pass
    
    profDict = {'radius': newline[0], 'ellip': newline[3],
                'PAFinal': newline[4], 'PA5': PA5,
                'xpos': newline[8], 'ypos': newline[9],
                'ellip5': ellip5}

    return profDict
    
def main(input1):
    galaxy = input1
    buildHalo = False
    inclMask = False
    #change this to sersic
    expString = "# Object number: 3\n0) expdisk\n1) $EXP1POS 1 1\n3) $EXP1MAG 1\n"+\
            "4) $EXP1RE 1\n9) 0 1\n10) 0 1\nZ) 0"+\
            "\n\n# Object number: 4"
            
    noExpString = "# Object number:3"
    
    
    decompDict = processDecomp(galaxy)
    profDict = processProf(galaxy)
    #print("decomp:", decompDict, "\n")
    #print("profile:", profDict)
    
    center = str(int(profDict['xpos'])) + ' ' + str(int(profDict['ypos']))
    conbox = "400 400"
    addMoreRegion = 75
    fitregion = str(int(profDict['xpos']-profDict['radius'])-addMoreRegion) + ' ' +\
                str(int(profDict['xpos']+profDict['radius'])+addMoreRegion) + ' ' +\
                str(int(profDict['ypos']-profDict['radius'])-addMoreRegion) + ' ' +\
                str(int(profDict['ypos']+profDict['radius'])+addMoreRegion)
    
    
    with open("GALFITTEMPLATE", 'r') as file :
        filedata = file.read()
    
    if inclMask:
        filedata = filedata.replace("$PIXELMASK", galaxy+"-I-Flag-Invert.fits")
    else:
        filedata = filedata.replace("$PIXELMASK", "none")
    
    filedata = filedata.replace("$PIXELMASK", "none")
    filedata = filedata.replace("$INPUTFILE", galaxy+"-I-Image.fits")
    filedata = filedata.replace("$OUTPUTFILE", galaxy+"-Output.fits")
    filedata = filedata.replace("$SIGMAFILE", galaxy+"-I-Sigma.fits")
    filedata = filedata.replace("$FITREGION", fitregion)
    filedata = filedata.replace("$CONBOX", conbox)
    
    filedata = filedata.replace("$SERSIC1POS", center)
    filedata = filedata.replace("$SERSIC1MAG", str(decompDict['mu_e1']))
    filedata = filedata.replace("$SERSIC1RE", str(int(decompDict['r_e1']/0.187)))
    filedata = filedata.replace("$SERSIC1IND", str(decompDict['n1']))
    filedata = filedata.replace("$SERSIC1PA", str(-profDict['PA5']))
    filedata = filedata.replace("$SERSIC1ELLIP", str(-profDict['ellip5']+1))
    #add axis ratio at 5 arcsec
    
    filedata = filedata.replace("$EXPD1POS", center)
    filedata = filedata.replace("$EXPD1MAG", str(decompDict['mu_e2']))
    filedata = filedata.replace("$EXPD1RE", str(int(decompDict['r_e2']/0.187)))
    filedata = filedata.replace("$EXPD1PA", str(-profDict['PAFinal']))
    filedata = filedata.replace("$EXPD1ELLIP", str(-profDict['ellip']+1))
    #add axis ratio at end
    
    if buildHalo: #change this to sersic
        expString = expString.replace("$EXP1POS", center)
        expString = expString.replace("$EXP1MAG", str(decompDict['mu_e3']))
        expString = expString.replace("$EXP1RE", str(decompDict['r_e3']/0.187))
        filedata = filedata.replace("$EXPBOOL", expString)
    else:
        filedata = filedata.replace("$EXPBOOL", noExpString)
    
    filedata = filedata.replace("$SKYEST", "1")
    
    with open(galaxy+".galfit", 'w') as file:
        file.write(filedata)
    
#main(sys.argv[1])
main("VCC0355")

