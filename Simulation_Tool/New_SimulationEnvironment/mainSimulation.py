"""
=========================================
main file for simulation environment
=========================================
"""


"""
@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

02.11.2016
"""


"""
Description of the code 


HOW TO USE:
- Open the main_new_mauro.GH file in Grasshopper
- Set the location in the Grasshopper file to same Location as defined in geoLoaction in this script
- Set both red framed boolean toggles to true 
- Set all needed values for evaluation at the beginning of the main.py script

if LadyBug once has calculated all the radiation data, they will be stored in the folder with the corresponding DataName. 
Also the Data of the PV producation and radiation hitting the window will be saved and can be loaded again, with the same DataName.


VARIABLE DEFINITION

   geoLocation: set the location which should be evaluated, make sure the correspoding .epw file is saved in the WeatherData folder
   Save: decide weather you want to save (True) or not save (False) the results
   optimization_Types: Decide for which energy demand type, you want to do the optimisation for
   DataName: choose the name for the stored data
   XANGLES = set the X-Angles of the ASF = [0, 15, 30, 45, 60, 75, 90] , 0 = closed, 90 = open
   YANGLES = set the Y-Angles of the ASF = [-45, -30,-15,0, 15, 30, 45] 
   NoClusters = option for using different multiple clusters
   ActuationEnergy = choose weather you want to include the the needed actuation energy for the ASF adjustment
   room_width =     
   room_height =
   room_depth = 
   glazing_percentage_w = perecentage of glazing of the total room width
   glazing_percentage_h =  perecentage of glazing of the total room height


	
INPUT PARAMETER DEFINITION 

	Fenst_A: Area of the Glazed Surface  [m2]
	Room_Depth=7.0 Depth of the modeled room [m]
	Room_Width=4.9 Width of the modeled room [m]
	Room_Height=3.1 Height of the modeled room [m]
	glass_solar_transmitance: Fraction of Radiation transmitting through the window []
	glass_light_transmitance: Fraction of visible light (luminance) transmitting through the window []
	lighting_load: Lighting Load [W/m2] 
	lighting_control: Lux threshold at which the lights turn on [Lx]
	U_em: U value of opaque surfaces  [W/m2K]
	U_w: U value of glazed surfaces [W/m2K]
	ACH_vent: Air changes per hour through ventilation [Air Changes Per Hour]
	ACH_infl: Air changes per hour through infiltration [Air Changes Per Hour]
	ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat recovery []
	c_m_A_f: Thermal capacitance of the room per floor area [J/m2K] #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
	theta_int_h_set : Thermal heating set point [C]
	theta_int_c_set: Thermal cooling set point [C]
	phi_c_max_A_f: Maximum cooling load. Set to -np.inf for unresctricted cooling [C]
	phi_h_max_A_f: Maximum heating load. Set to no.inf for unrestricted heating [C]

"""



import os, sys
import numpy as np
import pandas as pd

optimization_Types = ['E_total', 'Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting']
DataName = 'ZH05_49comb'
geoLocation = 'Zuerich_Kloten_2005' 

# 'ZH13_49comb'
# 'Zuerich_Kloten_2013.epw'

#DefaultValues
#Set panel data
#panel_data={
#"XANGLES": [0, 15, 30, 45, 60, 75, 90],
#"YANGLES" : [-45, -30,-15,0, 15, 30, 45],
#"NoClusters":1,
#"numberHorizontal":6,
#"numberVertical":9,
#"panelOffset":400,
#"panelSize":400,
#"panelSpacing":500
#}

##Set Building Parameters
#building_data={
#"room_width": 4900,     
#"room_height":3100,
#"room_depth":7000,
#"glazing_percentage_w": 0.92,
#"glazing_percentage_h": 0.97
#    }


#BuildingProperties={
#            
#"glass_solar_transmitance" : 0.687 ,
#"glass_light_transmitance" : 0.744 ,
#"lighting_load" : 11.74 ,
#"lighting_control" : 300,
#"Lighting_Utilisation_Factor" :  0.45,
#"Lighting_MaintenanceFactor" : 0.9,
#"U_em" : 0.2, 
#"U_w" : 1.2,
#"ACH_vent" : 1.5,
#"ACH_infl" :0.5,
#"ventilation_efficiency" : 0.6 ,
#"c_m_A_f" : 165 * 10**3,
#"theta_int_h_set" : 20,
#"theta_int_c_set" : 26,
#"phi_c_max_A_f": -np.inf,
#"phi_h_max_A_f":np.inf
#}

#SimulationProperties= {
#setBackTemp = 4.,
#Occupancy = 'Occupancy_COM.csv')



#def __main__(geoLocation='Zuerich_Kloten_2005', optimization_Types = ['E_total', 'Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting'] , DataName = 'ZH05_49comb'):

def MainCalculateASF(geoLocation, optimization_Types, DataName):
    
    # add python_path to system path, so that all files are available:
    sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'python'))
    
    from simulationFunctions import initializeSimulation, initializeASF, setBuildingParameters, initializeBuildingSimulation, setPaths, CalculateVariables  
    from simulationFunctions import PrepareRadiationData, runRadiationCalculation, runBuildingSimulation, createAllPlots, SaveResults 
        
        
    geoLocation, Save, optimization_Types, FolderName = initializeSimulation(
                           geoLocation = geoLocation, 
                           Save = True, 
                           optimization_Types = optimization_Types,
                           DataName = DataName) #'ZH05_49comb',
                          
            
    panel_data = initializeASF(
                           XANGLES = [0, 15, 30, 45, 60, 75, 90], 
                           YANGLES = [-45, -30,-15,0, 15, 30, 45], 
                           NoClusters = 1, #not working yet
                           ActuationEnergy = False) #not working yet
    
    
    
    building_data, roomFloorArea = setBuildingParameters(
                            room_width = 4900,     
                            room_height = 3100,
                            room_depth = 7000,
                            glazing_percentage_w = 0.92,
                            glazing_percentage_h = 0.97) 
    
    BuildingProperties, setBackTemp, Occupancy = initializeBuildingSimulation(
                            building_data = building_data,    
                            glass_solar_transmitance = 0.687 ,
                            glass_light_transmitance = 0.744 ,
                            lighting_load = 11.74 ,
                            lighting_control = 300,
                            Lighting_Utilisation_Factor = 0.45,
                            Lighting_MaintenanceFactor = 0.9,
                            U_em = 0.2, 
                            U_w = 1.2,
                            ACH_vent = 1.5,
                            ACH_infl = 0.5,
                            ventilation_efficiency = 0.6,
                            c_m_A_f = 165 * 10**3, #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
                            theta_int_h_set = 20,
                            theta_int_c_set = 26,
                            phi_c_max_A_f = -np.inf, 
                            phi_h_max_A_f = np.inf,
                            setBackTemp = 4.,
                            Occupancy = 'Occupancy_COM.csv')
    
    ###########################################################################    
    
    paths, weatherData, SunTrackingData = setPaths(
                                geoLocation = geoLocation, 
                                Occupancy = Occupancy,
                                FolderName = FolderName)
    
    
    ANGLES, hour_in_month, NumberCombinations, combinationAngles, daysPerMonth, \
    hourRadiation, hourRadiation_calculated, sumHours = CalculateVariables(
                            SunTrackingData = SunTrackingData, 
                            building_data = building_data, 
                            XANGLES = panel_data['XANGLES'], 
                            YANGLES = panel_data['YANGLES'])
    
    PV_electricity_results, PV_detailed_results, \
    BuildingRadiationData_HOD, now = runRadiationCalculation(
                            paths = paths, 
                            XANGLES = panel_data['XANGLES'], 
                            YANGLES = panel_data['YANGLES'], 
                            daysPerMonth = daysPerMonth, 
                            hour_in_month = hour_in_month, 
                            FolderName = FolderName,
                            panel_data = panel_data, 
                            NumberCombinations = NumberCombinations, 
                            createPlots = False, 
                            simulationOption = {'timePeriod' : None})
     
     
    #rearrange the Radiation Data on PV and Window into HOY form
    PV, BuildingRadiationData_HOY = PrepareRadiationData(
                            hour_in_month = hour_in_month, 
                            daysPerMonth = daysPerMonth, 
                            BuildingRadiationData_HOD = BuildingRadiationData_HOD, 
                            PV_electricity_results = PV_electricity_results, 
                            NumberCombinations = NumberCombinations)
    
                 
    hourlyData, monthlyData, yearlyData, ResultsBuildingSimulation, \
    BestKey_df, x_angles, y_angles = runBuildingSimulation(
                            geoLocation = geoLocation, 
                            paths = paths, 
                            optimization_Types = optimization_Types, 
                            building_data =  building_data, 
                            weatherData = weatherData, 
                            hourRadiation = hourRadiation, 
                            BuildingRadiationData_HOY = BuildingRadiationData_HOY, 
                            PV = PV, 
                            NumberCombinations = NumberCombinations, 
                            combinationAngles = combinationAngles, 
                            BuildingProperties = BuildingProperties, 
                            setBackTemp = setBackTemp, 
                            daysPerMonth = daysPerMonth, 
                            ANGLES = ANGLES)
        
    fig = createAllPlots(
                            monthlyData = monthlyData, 
                            roomFloorArea = roomFloorArea, 
                            x_angles = x_angles, 
                            y_angles = y_angles, 
                            hour_in_month = hour_in_month, 
                            optimization_Types = optimization_Types)
       
      
        
    ResultsBuildingSimulation, monthlyData, yearlyData \
                            = SaveResults(
                            now = now, 
                            Save = Save, 
                            geoLocation = geoLocation, 
                            paths = paths, 
                            fig = fig, 
                            optimization_Types = optimization_Types,  
                            monthlyData = monthlyData, 
                            yearlyData = yearlyData, 
                            ResultsBuildingSimulation = ResultsBuildingSimulation, 
                            BuildingProperties = BuildingProperties,
                            x_angles = x_angles,
                            y_angles = y_angles)
                            
    return ResultsBuildingSimulation, monthlyData, yearlyData

ResultsBuildingSimulation, monthlyData, yearlyData = MainCalculateASF(geoLocation, optimization_Types, DataName)