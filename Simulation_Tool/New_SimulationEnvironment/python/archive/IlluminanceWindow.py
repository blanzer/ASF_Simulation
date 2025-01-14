# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 17:06:28 2016

@author: Mauro

Methode 2: The total flux method
S. 105


"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import csv
import pandas as pd
import math
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib



# E = illuminance on work plane (lux)
# E_w = illuminance on face of window
# UF = utilisation factor
# M = maintenance factor
# G = glass factor
# B = framing factor
# A_f = area of floor


A_f = 7. * 4.9 # m2
A_w = 13.5 #m2
M = 0.9 #S.127
G = 0.85 # S.127
B = 1 # S.127
UF = 0.15
E_w = 10000 #lux


def illuminanceCalc(E_w, A_w, UF, M, G, B, A_f):
    
    E = E_w * A_w * UF * M * G * B * 1/(A_f) # lux
    
    factor = E/E_w
    
    return E, factor

E, factor = illuminanceCalc(E_w, A_w, UF, M, G, B, A_f)


print "E work plane: ", E

print "Factor", round(factor,3)


                    
                    

# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now

geoLocation = 'Zuerich_Kloten_2013'

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'



# define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])




#Set Building Parameters
building_data={"room_width":4900,     
"room_height":3100,
"room_depth":7000,
"glazing_percentage_w":0.92,
"glazing_percentage_h":0.97,
}

with open('building.json','w') as f:
    f.write(json.dumps(building_data))

paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults'

#set parmeters for evaluation



HOD = 12.0
Day = 15.0
monthi = 1.0
x_angle = 0
y_angle = 0

#gridSize = [50.]

combination = 0

tic = time.time()

resultsdetected=0
        
print '\nStart illuminance calculation with ladybug'

for x_angle in [0,90]:

    #Set panel data
    panel_data={"XANGLES": x_angle ,
    "YANGLES" : y_angle,
    "NoClusters":1,
    "numberHorizontal":6,
    "numberVertical":9,
    "panelOffset":400,
    "panelSize":400,
    "panelSpacing":500,
    }
    
    #Save parameters to be imported into grasshopper
    with open('panel.json','w') as f:
        f.write(json.dumps(panel_data))
    
    for monthi in range(1,13):
        for HOD in [8,10,12,14,16,18]:
            
            print "Combination number", combination
            print HOD, monthi, x_angle
            combination += 1
            
            
            comb_data={"x_angle": x_angle,
                       "y_angle":y_angle,
                       "HOD":HOD,
                       "Month":monthi,
                       "Day": Day
                        }
                        
             #create json file with the set combination of x-angle,y-angle and HOY
            with open('comb.json','w') as f:
                f.write(json.dumps(comb_data))
            
                                     
            
            
            #gridSize = [400.0, 200.0, 100.0, 50., 25., 12.5] #mm2
            gridSize = [400.0]
                               
            for size in gridSize:
                
                print 'size', size
                toc = time.time() - tic
                print 'time passed (min): ' + str(toc/60.)
                    
                with open('illuminance.json','w') as f:
                    f.write(json.dumps(size)) 
                            
                #Wait until the radiation_results were created    
                while not os.path.exists(paths['illuminance']+'\\IlluminanceWindow_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
                    time.sleep(3)
                       
                else:
                    print 'next step'
                    resultsdetected += 1
                                        
    
         
print 'illuminance calculation finished!'                            
