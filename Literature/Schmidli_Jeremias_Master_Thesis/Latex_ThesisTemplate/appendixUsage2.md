%!TEX root = thesis.tex

#Usage of Simulation Environment

##Get ASF_Simulation Folder
	
	In order to use the ASF simulation framework, you can either download the .zip file and unpack the folder or you can use the following commands within git:

	\subsection{Git Setup}

	In Your working directory type

	`git init`

	Then Checkout the repository

	`git clone https://github.com/architecture-building-systems/ASF_Simulation.git`

	To download the files type

	`git pull`

	More information on using git can be found in the section [[Using Git]]

		
##Installation Guides

	###Rhino

		https://www.rhino3d.com/download
		You will need at least Rhino5
		Talk to Daren about licences

	###Grasshopper

		Open Source
		http://www.grasshopper3d.com/page/download-1

	####Grasshopper AddOns

		* GHPython: Grasshopper Python http://www.food4rhino.com/project/ghpython?etx
		* DIVA/VIPER: http://diva4rhino.com/
		 + You will need to add the Zuerich-Kloten weather file to C:/DIVA/WeatherData
		* Hoopsnake: For looping grasshopper scripts http://www.food4rhino.com/project/hoopsnake?etx
		* Ladybug/Honeybee: Thermal and radiation simulations, follow the instructions given within the following link: https://github.com/mostaphaRoudsari/ladybug/blob/master/resources/Installation_Instructions.md
		* Human: some additional functions for GH http://www.food4rhino.com/project/human?etx
		* Mesh Tools: http://www.food4rhino.com/project/meshedittools


	###Python

		Anaconda is recommended as it is easier to create virtual environments and manage python
		https://www.continuum.io/downloads

		If you do the installation manually (like how PJ did), follow this guide:
		http://www.lowindata.com/2013/installing-scientific-python-on-mac-os-x/

		You will need numpy, scipy, matplotlib, ipython


##Grasshopper Simulations

	##Installation

	You will need to download all Rhino and Grasshopper plugins found here [[Installation Guides]]

	Open an empty rhino file, type `grasshopper` in the command line to open grasshopper. Open `main.gh` from the folder Simulation_Environment in grasshopper.



	##How it works
	GHpython scripts generate the geometry of the ASF of every possible configuration. We then loop through every configuration and run an energy plus simulation and a ladybug simulation on every geometry for each hourly time step. The results are then post-processed to acquire the best configuration for each timestep.
	Special attention has to be given to the sections in the script which have a red frame, these sections should be checked before every simulation, to make sure that it is running correctly. Furthermore, one has to be aware of the places the results are stored, and the instructions given [here](https://github.com/architecture-building-systems/ASF_Simulation/wiki/Grasshopper-Simulation#save-data) and [here](https://github.com/architecture-building-systems/ASF_Simulation/wiki/Grasshopper-Simulation#save-radiation-results) on how to save the data should be closely followed. 



	##Set Geometry
	User Interaction on general geometry and simulation inputs

	###ASF Simulation Inputs
	Angles, number of clusters and the desired grid point size that will be used for the simulation are set in this section. The desired grid point size is only relevant for the ladybug analysis.

	### Geometry Inputs
	General inputs for the room and the asf geometry. 

	##Geometry Calculations
	Processing of the geometry inputs, creates the geometry and saves inputs.
	###Save Inputs
	Python script that saves asf geometry and simulation inputs.

	###Render the Building
	GHpython script `Render_Room` creates the building geometry for simulation. The room width, height, depth and glazing fractions of the front facade can be selected

	###Render the ASF
	Generate Diamond Array: Produces a matrix of coordinates of where a PV panel should exist
	Combination Maker: Determines the combination of PV panels. When running a simulation, **it must always be made sure that the right combination is connected** (either EplusComb or RadiationComb, framed in red)
	Render Diamond Array: Generates the geometry based off the chosen combination and array

	##E+ Simulation

		###DIVA Interface Conversion
			* Converts ASF panels into DIVA shading elements 
			* Converts all interior walls into adiabatic surfaces
			* Converts the front wall to a facade element
			* Converts the glazed section into a window element

	###Run the Simulation
	Run through the Viper interface. **It is important that the right settings are used.** Especially the weather file is subject to change. For the DIVA analysis, this can only be done in the Viper settings. 
	* Lx set point: 300
	* Heating COP=variable (usually 4 or 5)
	* Cooling COP=3
	* Lighting Load: Default is 11.74 W/m2

	###Save Data
	Python script that saves the DIVA data for post processing. The folder where it will be saved is set automatically in the script 'set DIVA data path' to 'Simulation_Environment/data/grasshopper/DIVA/DIVA_results'. **After a simulation finishes, the acquired data has to be moved to a separate folder with a unique name, which will be used for post processing.** Alternatively, the folder 'DIVA_results' can simply be renamed. It is good practice to also save a backup of the current main.gh file to this folder ([Ctr+Alt+s] saves a backup, this should then also be moved to the corresponding data folder. 

	##Loop E+
	Uses hoopsnake to iterate through all possible configurations
	 - Note that sometimes the hoopsnake algorithm is not connected correctly



	##Set Weather File
	The weather file used for the ladybug radiation analysis is set in this section. The desired .epw file must already be in the WeatherData folder and the full name of the weather file has to be input to the python weatherPath python script. 



	##Save details of weather file
	The weather file that was specified is read and relevant information is on the sun position and the temperature is saved to the folder 'Simulation_Environment\data\geographical_location'. If a new weather file is used, the main.py file has to be run in 'initialize' mode to prepare the data for further use with grasshopper. Make sure that the component 'Ladybug_SunPath' is enabled when a new weather-file is introduced. 


	##Loop LadyBug
	In this section ladybug is looped according to the specified angle combinations and for relevant hours (see 'Set Evaluation Period')


	##Set Evaluation Period
	Analysis period is set according to the loop number and the auxiliary data on the sun positions. 

	##Ladybug Solar Analysis
	First of all, you have to let ladybug fly. For this the ladybug_ladybug component has to be put onto the GH screen. This component has to run first, if there still are warnings that you first have to let ladybug fly, click on the component and press CTRL+B, then disable and enable again components that show the warning. This ensures, that the ladybug_ladybug component runs first. 

	###Create Mesh for Radiation Analysis
	Creates a mesh of the asf for the radiation analysis according to the desired grid point size. The normals of the ASF geometry are flipped so that they face away from the building. 

	###Create Sky Matrix
	In the selectSkyMtx component, it is possible to either choose a specific hour of the year or a period of time, which can be chosen with the Analysis Period component. **WARNING: This component is not working correctly in the current version of ladybug.** The bug has been found, fixed, and reported to the developers [here](https://github.com/mostaphaRoudsari/ladybug/issues/233). 

	###Calculate Radiance on Panels
	Calculates the radiance on a specified geometry. The simulation is done for the chosen settings given by the SelectSkyMtx component. **Toggle runIt to start the evaluation**, this can take up to 20 seconds on a fast computer. 

	###Sky Dome for reference
	This component creates sky domes, that show where the radiation is coming from. 



	##Save Radiation Results
	The detailed radiation results are saved to a .csv file with a C# script. The results are saved to the folder Simulation_Environment/data/grasshopper/LadyBug/radiation_results. It should be made sure that this folder is empty before starting a simulation, because otherwise there might be 'leftover' data, which will fill up space without being used. The 'copyLayoutAndComb' component copies the file generated in the 'Geometry Calculations' section and also saves it to the radiation_results folder for convenience. **After a simulation finishes, the acquired data has to be moved to a separate folder with a unique name, which will be used for post processing.** Alternatively the 'radiation_results' folder can be renamed. It is good practice to also save a backup of the current main.gh file to this folder ([Ctr+Alt+s] saves a backup, which should then also be moved to the corresponding data folder). 


##Python Evaluation

	###How it works
	The data that was previously generated by the main.gh script is read in and post processed to output several graphs and a summary.csv file. 

	###main.py
	This is the main file for the python evaluation. There are two modes: 'initialize' and 'post_processing'. If an evaluation is done for the first time for a specific location, it must first run in 'initialize' mode, otherwise it can be run directly in 'post_processing' mode (see also Installation Guides). 
	At the beginning of the script, there is a user interaction section. When starting an evaluation, a user must go through this section to make sure everything is set as wished. All variables are described in detail right before they are defined. 

##Set Up

	All the files that are necessary to perform simulations of the ASF are in the folder Simulation_Environment. There are two main simulation files, one for grasshopper, the other one for the python part of the simulation (main.gh, main.py). In order to get started with simulations, the following steps have to be taken to generate the auxiliary files that are needed:

	1. Open the main.gh file.  

	2. Assign the desired weather file that will be used for the radiation simulation in the section "Set Weather File". 

	3. Make sure that the component 'Ladybug_SunPath' is enabled in the section 'Save details of weather file'. A new folder in "Simulation_Environment\data\geographical_location" with the name of the location and information on temperature and the sun position will now be created. 

	4. Open the main.py file.

	5. In the "user interaction" section, the mainMode must be set to 'initialize' and the geoLocation must be set to the folder that was generated in grasshopper (for the zurich-kloten epw file, the corresponding folder is called 'Zuerich-Kloten'). The other options do not yet require any change, as they are only important for the post-processing mode.

	6. Run the main.py script. Be aware that the first time the file is run, it will take some time, as the lookup-table for the pv-electricity-generation needs to be generated first.

	7. Once the main.py script has finished without errors, the 'Ladybug_SunPath' component in the sectioin 'Save details of weather file' of the main.gh script can be disabled again, as it is no longer needed. This will speed up the initialization of grasshopper when restarting it. 

	Now, simulations can be performed using grasshopper. See [[Run Grasshopper]]

##Run Grasshopper

	After carefully following the instructions given in [[Installation Guides]] and [[Set-Up]], simulations can now be done using grasshopper as follows:

	#General Set-Up

	1. Open main.gh

	2. Make sure the 'run' switch in the 'E+ Simulation' section as well as the '_runIt' switch in the 'Ladybug Solar Analysis' section are set to False 

	3. Set the building geometry and the facade geometry for the simulation in the section 'Set Geometry'

	#LadyBug Radiation Simulation

	1. Set the weather file in the section 'Set Weather File' (If you want to use a new weather file, follow the instruction given in [[Set-Up]])

	2. Reset HoopSnake in the section 'Loop Lady Bug'

	3. Go to the folder 'ASF_Simulation\Simulation_Environment\data\grasshopper\LadyBug\radiation_results' and make sure it is empty. 

	4. Connect 'RadiationComb' to the 'combination' input of the 'Combination Maker V2' in the Section Geometry Calculations

	5. Test loop hoopsnake and make sure the combinations are run as desired. It can be stopped by right clicking on hoopsnake and selecting 'stop'. 

	6. Reset hoopsnake again. 

	7. Toggle the '_runIt' input in the 'Ladybug Solar Analysis' section to true. 

	8. Go again to the radiation_results folder and see if the .csv file for the first iteration was created. Also look at the graphical output from Ladybug in the rhino scene, make sure everything is evaluated as desired. 

	9. If everything looks fine, start to loop hoopsnake again. 

	10. Check that the 'LayoutAndCombinations.txt' file was created in the 'radiation_results' folder and look at the csv files to see if the results are reasonable. 

	11. Wait until the simulation is done. This step will generally take sever hours, so it is a good idea to let it run over night. 

	12. When the simulation is over, the folder 'radiation_results' has to be renamed to have a unique name, typical for the simulation, such as 'Radiation_Kloten_5x_1y_2clust_SE'. 

	13. Turn off the radiation analysis (set '_runIt' to False). This will automatically create a new and empty 'radiation_results' folder.  

	15. Save a backup of the main.gh file [CTR + ALT + S] and move it to the folder where the results are saved. 

	# E+ Building Simulation

	1. Set the desired weather file and other options in the Viper component settings in the section 'E+ Simulation'

	2. Set all other options in this section. 

	3. Connect 'EplusComb' to the 'combination' input of the 'Combination Maker V2' component in the 'Geometry Calculations' section.  

	3. Loop hoopsnake in the 'Loop E+' section while looking at the rhino scene to make sure the desired combinations will be evaluated. 

	4. Reset hoopsnake in the 'Loop E+' section. 

	4. Turn the run input toggle in the 'E+ Simulation' section to true. 

	5. Go to the folder 'ASF_Simulation\Simulation_Environment\data\grasshopper\DIVA\DIVA_results' and check the 'LayoutAndCombinations.txt' file as well as the first iteration. 

	6. Check the output of the VIPER component in the 'E+ Simulation' section, there should be no erros and no warnings. 

	7. When everything looks fine, loop hoopsnake in the 'Loop E+' section. 

	8. Check the rhino scene and the result files to make sure everything is working correctly while looping. 

	9. Rename the 'DIVA_results' folder to a unique name, such as 'DIVA_Kloten_5x_1y_2clust_SE'. 

	10. Turn the 'run' input of VIPER to False. This will create a new, empty 'DIVA_results' folder. 

	11. Save a backup of the main.gh file [CTR + ALT + S] and move it to the folder where the results are saved. 

	# Next Steps

	The results can now be post-processed as described in [[Run Python]]

##Run Python

	Once the grasshopper simulations are finished (see [[Run Grasshopper]]), the results can be post-processed as follows:

	1. Open main.py

	2. Set all the post-processing options in the user interaction section (each variable is described before its definition)

	3. Run main.py (you can press F5)

	4. Done