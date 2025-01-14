import sys, os
import math
import numpy as np
import pandas as pd
import time

from sympy.solvers import solve
from sympy import Point, Polygon, pi, Symbol
from scipy.optimize import fsolve

from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.pyplot as plt
#from sympy.abc import t


paths = {}

geoLocation = 'Zuerich_Kloten_2013.epw'

paths['weather'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData'
paths['scirpt'] =  r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\python'
paths['location'] = os.path.join(paths['weather'], geoLocation)
paths['SunData'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\SunPosition2.csv'
paths['PanelData'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\PanelPostion.csv'
paths['Save'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'

sys.path.insert(0, paths['scirpt'])
						
from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['location'])
radiation = weatherData[['year', 'month', 'day', 'hour','dirnorrad_Whm2', 'difhorrad_Whm2','glohorrad_Whm2']]





#Load LB-Files
SolarData = np.load(os.path.join(paths['Save'], 'SolarData.npy')).item()
SolarData_df = pd.DataFrame(SolarData)
SolarData2 = np.load(os.path.join(paths['Save'], 'SolarData2.npy')).item()
SolarData_df2 = pd.DataFrame(SolarData2)
SolarData3 = np.load(os.path.join(paths['Save'], 'SolarData3.npy')).item()
SolarData_df3 = pd.DataFrame(SolarData3)

SolarData_df = pd.concat([SolarData_df,SolarData_df2, SolarData_df3], axis=1)
LB = SolarData_df['00'] * 1000 / (50*0.4*0.4) # kWh in Wh divided through area of panels in m2


RadData_df = pd.concat([radiation, LB], axis=1)

start = 0
end = 8760
RadAnalysis = pd.concat([radiation['dirnorrad_Whm2']/LB, radiation['difhorrad_Whm2']/LB,radiation['glohorrad_Whm2']/LB, LB/LB], axis=1)
RadAnalysis.columns = ['direct', 'diffuse', 'global', 'LB']

#RadAnalysis[start:end].plot(kind='line', title = 'Radiation Analysis', grid = True) 




SunData = pd.read_csv(paths['SunData'])
PanelPoints = pd.read_csv(paths['PanelData'])

TotalHOY = SunData['HOY'].tolist()


#http://math.stackexchange.com/questions/164700/how-to-transform-a-set-of-3d-vectors-into-a-2d-plane-from-a-view-point-of-anoth
room_height = 3100.
room_depth = 7000.
room_width = 4900.


#S1 = [-2500,0,0]
#S2 = [4000,10,0]
#S3 = [-2500,0,5000]

ii = 2000


#
for ii in range(2000,2005):
    
    print 'HOY', TotalHOY[ii]
    print str(ii)
    
    #SunVec = np.array([-2000, 2000 ,2000])
    #SunVec = np.array([0.92, -35 ,2])*1000
    SunVec = np.array([SunData['xV'][TotalHOY[ii]], SunData['yV'][TotalHOY[ii]], SunData['zV'][TotalHOY[ii]]]) 
    SunPos = np.array([SunData['xP'][TotalHOY[ii]], SunData['yP'][TotalHOY[ii]], SunData['zP'][TotalHOY[ii]]])
    
    PanelNum = len(PanelPoints)/4
    PanelNum = 4
    
    
    
    
    if PanelNum == 4:
        row = 2
        col = 2
        
    elif PanelNum == 8:
        row = 2
        col = 4
    elif PanelNum == 10:
        row = 2
        col = 5
        
    elif PanelNum == 50:
        row = 9
        col = 6
    elif PanelNum == 22:
        row = 4
        col = 6
        
        
    PanelSize = 400. #mm
    
    Hyp = np.sin(np.deg2rad((45)))*PanelSize
    DistWindow = 100. # distance of panels from Window surface
    
    #XANGLES = range(5,15,5)
    #for xAngle in XANGLES:
    
    
            
            
    xR = 0 
    yR = 0 
    zR = 0
    room= [[xR, yR, zR],
            [xR + room_width, yR, zR],
            #[xR + room_width, yR- room_depth, zR],
            #[xR, yR - room_depth, zR],
            [xR, yR, zR + room_height],
            [xR + room_width, yR, zR + room_height],
            #[xR + room_width, yR- room_depth, zR + room_height],
            #[xR, yR - room_depth, zR + room_height],
            ]
            
            
    def ProjPlane(S1, n): #needed
        # S1 Start Point
        # n sun vector
    
        S = {1: np.array(S1), 2: np.array(n)}
        
        def FunctionSolv(w, S):
            x = w[0]
            y = w[1]
            z = w[2]
            
            size = 5000.
            
            S1 = S[1]
            n = S[2]
            
            F = np.empty((3))
            F[0] = np.sqrt(pow(x-S1[0],2)+pow(y-S1[1],2) + pow(z-S1[2],2))-size
            F[1] = n[0]*x + n[1]*y + n[2]*z - 0
            F[2] = z-1
            return F
        
        def FuSo2(w, S):
            x = w[0]
            y = w[1]
            z = w[2]
            
            size = 5000.
            
            S1 = S[1]
            n = S[2]
            
            F = np.empty((3))
            F[0] = np.sqrt(pow(x-S1[0],2)+pow(y-S1[1],2) + pow(z-S1[2],2))-size
            F[1] = n[0]*x + n[1]*y + n[2]*z - 0
            F[2] = y-1
            return F
    
    
        zGuess = np.array([1,1,1])
        w = fsolve(FunctionSolv, zGuess, S)
        q = fsolve(FuSo2, zGuess, S)
        
        return w, q
    
      
    def PointPro(S1, S2, S3, A, SunVec): #needed
        
        #creates a Projection of A_prime for A on the plane S
        
        #W = math.sqrt((S2[0]-S1[0])**2 + (S2[1]-S1[1])**2 + (S2[2]-S1[2])**2)
        #H = math.sqrt((S3[0]-S1[0])**2 + (S3[1]-S1[1])**2 + (S3[2]-S1[2])**2)
        
        M = [(S2[0] + S3[0])/2.,(S2[1] + S3[1])/2. ,(S2[2] + S3[2])/2. ]
        
        
        a = np.array([[S1[0],S1[1],S1[2]], [S2[0],S2[1],S2[2]],[M[0],M[1],M[2]]])
        b = np.array([1,1,1])
        coef = np.linalg.solve(a, b)
        
        #N = [coef[0]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[1]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[2]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2)]
        
        #find projection of A, Aprime
        k = Symbol('k')
        k = solve(coef[0]*(k*SunVec[0]+ A[0]) + coef[1]*(k*SunVec[1]+ A[1]) + coef[2]*(k*SunVec[2] + A[2]) -1, k)
        k = k[0]
            
        APrime = [round( (k*(SunVec[0])+ A[0]),2), round((k*(SunVec[1])+ A[1]),2), round((k*(SunVec[2])+ A[2]),2)] 
        
        return APrime
        
    
    def DisPoints (P1,P2):
        distance = np.sqrt( (P1[0]-P2[0])**2 + (P1[1]-P2[1])**2 + (P1[2]-P2[2])**2)
        #print distance    
        return distance
    
    
    def Area(Dict):
        #calcualte area of polygon
        ASF_dict = Dict
        p1, p2, p3, p4, p5 = map(Point, [(ASF_dict[0][0], ASF_dict[0][1]), (ASF_dict[1][0], ASF_dict[1][1]), 
                                 (ASF_dict[2][0], ASF_dict[2][1]), (ASF_dict[3][0], ASF_dict[3][1]), (ASF_dict[0][0], ASF_dict[0][1])])
        poly1 = Polygon(p1, p2, p3, p4, p5)
        
        resultASF = abs(round(float(poly1.area),2)) #mm2
        return resultASF
    
    
    
    xAngle = 0
    yAngle = 45
    
    XANGLES = [45]
    YANGLES = [45]
    
    TotalDict = {}
    
    for x_angle in XANGLES:
        for y_angle in YANGLES:
            
            print '\nStart Calculation'
            print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
            
            tic = time.time()
            
            print str(x_angle), str(y_angle)
            
            xAngle = np.deg2rad(-x_angle)
            yAngle = np.deg2rad(y_angle) 
            
            #old projection plane
            
    #        S1 = [10,-5000,10]
    #        S2 = [10,-5000,50010]
    #        S3, PointA = ProjPlane(S1 = S1, n = SunVec)
    #        S3 = [50010,-5000,10]
            
            #new projection plan
            
            S1 = [0,0,-10]
            S2 = [0,5000,-10]
            #3S3, PointA = ProjPlane(S1 = S1, n = SunVec)
            S3 = [5000,0,-10]
            
            
            RoomPrime = []
            ListX, ASFX = [], []
            ListY, ASFY = [], []
            ListZ, ASFZ = [], []
            
            for ii in room:
                Prime = PointPro(S1 = S1, S2 = S2, S3= S3, A = ii, SunVec = SunVec)
                RoomPrime.append(Prime)
                ListX.append(Prime[0])
                ListY.append(Prime[1])
                ListZ.append(Prime[2])
                
                
    
            ASF_dict = {}
            ASF_dict_prime = {}
            
            for dot in range(PanelNum):
                
                # 1   
                #0 2   
                # 3 
                
                #change order of dots
                ASF_dict[dot] = [[PanelPoints['x'][(dot*4) + 0] + (Hyp- np.cos(yAngle)*Hyp)     ,PanelPoints['y'][(dot*4) + 0] - np.sin(yAngle)* Hyp,   PanelPoints['z'][(dot*4) + 0]], 
                                 [PanelPoints['x'][(dot*4) + 1]                                 ,PanelPoints['y'][(dot*4) + 1] - np.sin(xAngle)* Hyp,   PanelPoints['z'][(dot*4) + 1] - (Hyp- np.cos(xAngle)*Hyp)],
                                 [PanelPoints['x'][(dot*4) + 3] - (Hyp- np.cos(yAngle)*Hyp)     ,PanelPoints['y'][(dot*4) + 3] + np.sin(yAngle)* Hyp,   PanelPoints['z'][(dot*4) + 3]],
                                 [PanelPoints['x'][(dot*4) + 2]                                 ,PanelPoints['y'][(dot*4) + 2] + np.sin(xAngle)* Hyp,   PanelPoints['z'][(dot*4) + 2] + (Hyp- np.cos(xAngle)*Hyp)]]
                
#                ASF_dict[dot] = [[PanelPoints['x'][(dot*4) + 0]  ,PanelPoints['y'][(dot*4) + 0], PanelPoints['z'][(dot*4) + 0]], 
#                                 [PanelPoints['x'][(dot*4) + 1]  ,PanelPoints['y'][(dot*4) + 1], PanelPoints['z'][(dot*4) + 1]],
#                                 [PanelPoints['x'][(dot*4) + 3]  ,PanelPoints['y'][(dot*4) + 3], PanelPoints['z'][(dot*4) + 3]],
#                                 [PanelPoints['x'][(dot*4) + 2]  ,PanelPoints['y'][(dot*4) + 2], PanelPoints['z'][(dot*4) + 2]]] 
        
            count = 0
            for ii in range(PanelNum):    
                ASFPrime = []
                
                for jj in range(4):
                    
                    Prime = PointPro(S1 = S1, S2 = S2, S3= S3, A = ASF_dict[ii][jj], SunVec = SunVec)
                    ASFPrime.append(Prime)
                    
                    ASFX.append(Prime[0])                            
                    ASFY.append(Prime[1])                            
                    ASFZ.append(Prime[2])
    
    #                ASFZ.append(ASF_dict[ii][jj][2])
    #                ASFY.append(ASF_dict[ii][jj][1])
    #                ASFX.append(ASF_dict[ii][jj][0])
    
                    count += 1
                    
                ASF_dict_prime[ii] = ASFPrime        
            
            
            print "\nStart Geometry Analysis"
            result1 = Area(Dict = ASF_dict_prime[0])
            print "\nASF_Point2:  0", "- Area: ", result1
            print "no"
            result2 = Area(Dict = ASF_dict[0])
            print result2
            
            Shadow = {}
            ASFArea = {}
            ASFRealArea = {}
            Shadow[0] = 0
            ASFArea[0] = result1
            
            SumArea = 0
            
            for ii in range(1,PanelNum):
                #case: if far right point of panel is within the panel to the right
                p = Polygon((ASF_dict_prime[ii][0][0],ASF_dict_prime[ii][0][1]),
                            (ASF_dict_prime[ii][1][0],ASF_dict_prime[ii][1][1]),
                            (ASF_dict_prime[ii][2][0],ASF_dict_prime[ii][2][1]),
                            (ASF_dict_prime[ii][3][0],ASF_dict_prime[ii][3][1]))
                
                if p.encloses_point(Point(ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1])):
                    #if Point is in polygon p, than true will be returned
                    #test if far right point of asf porjection lies in the panel right to the existing one
                    
                    #Calculate Intersection               
                    p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1]), (ASF_dict_prime[ii][1][0], ASF_dict_prime[ii][1][1]), 
                                         (ASF_dict_prime[ii][2][0], ASF_dict_prime[ii][2][1]), (ASF_dict_prime[ii][3][0], ASF_dict_prime[ii][3][1])])
            
            
                    p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[ii-1][0][0], ASF_dict_prime[ii-1][0][1]), (ASF_dict_prime[ii-1][1][0], ASF_dict_prime[ii-1][1][1]),
                                         (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1]), (ASF_dict_prime[ii-1][3][0], ASF_dict_prime[ii-1][3][1])])
            
                    poly1 = Polygon(p1, p2, p3, p4)
                    poly2 = Polygon(p5, p6, p7, p8)
            
                    a =  poly1.intersection(poly2)
                    SP1 = a[0]
                    SP2 = a[1]
                    
                    
                    resultShadow = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1]), (SP1[0],SP1[1]),
                                (ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1])).area)
                    
                    resultASF = abs(poly1.area)
                    
                    totalArea = resultASF - resultShadow
            
                    Shadow[ii]= resultShadow
                    ASFArea[ii] = resultASF
                    
                    SumArea += resultASF            
                    print "ASF_Point2: ", ii , "- Area: ", round(totalArea,3)
                    print "yes"    
                    
                else:
                    result = Area(Dict = ASF_dict_prime[ii])
                    print "ASF: ", ii , "- Area: ", round(result,3)
                    print "no"
                    
                    SumArea += result 
                
                    Shadow[ii]= 0 
                    ASFArea[ii] = result
                    
                
                print "ASFreal: ", ii    
                result2 = Area(Dict = ASF_dict[ii])
                ASFRealArea[ii] = result2
                print result2
                
            TotalDict[str(x_angle) + str(y_angle)] = SumArea 
               
         
            
            for ii in range(1,row): #2
                #case: check if the lowest edge of  a panel is intersection with panel below
                for colNum in range(col): #4
                
                                    
                    if (colNum + ii *col) < PanelNum: #skip the last panels 
                    
                        p = Polygon((ASF_dict_prime[colNum + ii *col][0][0],ASF_dict_prime[colNum + ii *col][0][1]),
                                    (ASF_dict_prime[colNum + ii *col][1][0],ASF_dict_prime[colNum + ii *col][1][1]),
                                    (ASF_dict_prime[colNum + ii *col][2][0],ASF_dict_prime[colNum + ii *col][2][1]),
                                    (ASF_dict_prime[colNum + ii *col][3][0],ASF_dict_prime[colNum + ii *col][3][1]))
        
                    
                        if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                            #if Point is in polygon p, than true will be returned
                            
                            #Calculate Intersection               
                            p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[col + ii *colNum][0][0], ASF_dict_prime[col + ii *colNum][0][1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), 
                                                 (ASF_dict_prime[colNum + ii *col][2][0], ASF_dict_prime[colNum + ii *col][2][1]), (ASF_dict_prime[colNum + ii *col][3][0], ASF_dict_prime[colNum + ii *col][3][1])])
                    
                    
                            p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][1]),
                                                 (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])])
                    
                            poly1 = Polygon(p1, p2, p3, p4)
                            poly2 = Polygon(p5, p6, p7, p8)
                    
                            a =  poly1.intersection(poly2)
                            SP1 = a[0]
                            SP2 = a[1]
                            
                                   
                            
                            resultShadow2 = abs(10**(-6)* Polygon((SP2[0],SP2[1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), (SP1[0],SP1[1]),
                                                     (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
                    
                                    
                            Shadow[colNum + ii *col] += resultShadow2
                    
                                
                            print "ASF_Point3: ", colNum + ii *col
                            print "yes"    
                            
    
                            
                        else:
                            result1 = Area(Dict = ASF_dict_prime[colNum + ii *col])
                            print "ASF: ", colNum + ii *col
                            print "no"
                            Shadow[colNum + ii *col]+= 0
                    else:
                        pass
            
            sumArea2 = 0
            for ii in range(PanelNum):       
                   print "ASF: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
                   sumArea2 += ASFArea[ii]-Shadow[ii]
                        
            
            print 'ASF Area Projection: ', round(sumArea2,3)    
           
            showFig = True
            if showFig == True:
                # figure 2
                fig = pylab.figure()
                ax = Axes3D(fig)
                
                x_vals = np.array(ASFX) 
                y_vals = np.array(ASFY) 
                z_vals = np.array(ASFZ) 
                
                import random
    
                print random.random()
                colors1 = cm.rainbow(np.linspace(0, 1, len(x_vals)/4))
                
                
                          
                
                
                for ii in range(len(x_vals)/4):
                    rand = random.random()
                    ax.scatter(x_vals[ii* 4 + 0: ii* 4 + 4], y_vals[ii* 4 + 0: ii* 4 +4], z_vals[ii* 4 + 0: ii* 4 +4], s=15, color=colors1[ii])
                
                
                #ax.scatter(ListX, ListY, ListZ)
                
                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')
                
                #ax.view_init(45,60)
                ax.view_init(0,90)
                #ax.view_init(45,60)
                pyplot.show()
            toc = time.time() - tic
            print 'time passed (min): ' + str(round(toc/60.,2))
            
            
            
          