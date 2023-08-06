# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:22:00 2019

@author: THO1NR
"""

import pandas as pd
import sys
import os
import random

# Get path of current directory and convert it to lisp
directory_path = os.path.join(os.path.dirname(__file__))

def convertPath(path):
     #sep = os.path.sep
     #print('separator: ' + sep)
     return path.replace(os.path.sep, ';') 
 
directory_path_lisp = convertPath(directory_path)[1:]


sys.path.append(directory_path)
sys.path


import actr
import actcv as cv
import actms as ms



# LOAD ACT-R MODELS
def loadmodels():
    actr.load_act_r_model(directory_path_lisp + ";EF-metamodel.lisp")
    actr.load_act_r_model(directory_path_lisp + ";EF-submodel-left.lisp")
    actr.load_act_r_model(directory_path_lisp + ";EF-submodel-middle.lisp")
    actr.load_act_r_model(directory_path_lisp + ";EF-submodel-right.lisp")

loadmodels()
actr.set_current_model("main-model")          

ms.getutility()
ms.saveutility()


## ----- -----
# loop over all datasets
timesRun = 1
session = [2,7]

printer = pd.DataFrame(columns=[], index = range(0))

for tr in range(timesRun):
    random.shuffle(session)


    print("-"*40 + "-----------------------------")
    print("-"*40 + '   Run: ' + str(tr) )
    print("-"*40 + "-----------------------------")
    print("-"*40 + '  List: ' + str(session) )
    print("-"*40 + "-----------------------------")

  # ms.setsaveutility()

    for ses in session:
        print('Looping Participant: {0}'.format(ses))

        
        # LOOP AND SCHEDULE EVENT 4
        print('Looping Scenario: 2 | Event: 3')
        data = pd.read_csv(directory_path + '/Data/Session_{0}_scenario_2.csv'.format(ses),
                            sep = ';', dtype = {'ALTITUDE' : float, 'SPEED' : float, 'AOI' : object, 'AlarmActive' : float, 'AOIpT' : str})
            
        header = list(data)
        data = data.where((pd.notnull(data)), None)
               
        cv.setCVsettings()
        cv.schedule_Visicon(data, header, header[-2], header[1], header[0], 3000, 3, 0, 0, 0.01)
                
        #ms.end_scenario()

        ms.init_actms()
        ms.writeToProtocol("Session", ses)
        ms.writeToProtocol("timesRun", tr)

        actr.run_until_condition("end-program", True)       

        tmpresult = ms.getProtocol()
        printer = pd.concat([printer, tmpresult])

        
       # ms.resetutility()
       # ms.getutility()

        actr.reset()
        loadmodels()
  
        print("-"*30 + " Models Reloaded " + "-"*30)         

        ms.setutility()
        
        ms.deleteProtocol()

        # reload act-r
        actr.set_current_model("main-model")
        actr.delete_all_visicon_features()

    print("-"*30 + " " + "-"*22 + " " + "-"*30)
    print("-"*30 + "    END SIMULATION     " + "-"*30)         
    print("-"*30 + " " + "-"*22 + " " + "-"*30)

printer.to_csv('simulation_results.csv')

