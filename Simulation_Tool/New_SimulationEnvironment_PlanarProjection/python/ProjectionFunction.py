# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 09:41:42 2017

@author: Assistenz
"""

from sympy import Point, Polygon
import numpy as np
import math
import time

def Theta2directions (sunAlt, sunAzi , panelAlt, panelAzi):

    sunAlt = np.deg2rad(sunAlt)
    panelAlt = np.deg2rad(panelAlt) # panelAlti
    sunAzi = np.deg2rad(sunAzi)
    panelAzi = np.deg2rad(panelAzi)
    
      
    theta2 = np.arccos(np.cos(sunAlt) * np.cos(sunAzi-panelAzi) * np.sin(panelAlt) + np.sin(sunAlt)* np.cos(panelAlt))
    
    if sunAzi >= np.deg2rad(90) or sunAzi <= np.deg2rad(-90):
        theta2 = np.nan
        print "Warning, sun position is behind the facade. Setting incident angle to nan"
    else:
        theta2 = np.rad2deg(theta2)
   
    return theta2 # deg



def RadTilt (I_dirnor, I_dif, ref, theta, panelAlt, sunAlt):
    #calculate radiation on tilt surface
    theta = np.deg2rad(theta)
    panelAlt = np.deg2rad(panelAlt)
    sunAlt = np.deg2rad(sunAlt)

    #Radiation on the horizontal surface: Used for reflectance calculation
    I_h = I_dif + I_dirnor * np.sin(sunAlt) # simplified, formula with view factor should be applied
    
    #If the sun is behind the context surface and there is diffuse radiation 
    if math.isnan(theta) and I_dif != 0:
        Rad_tilt = I_dif * ((1+np.cos(panelAlt))/2) + I_h * ref * ((1- np.cos(panelAlt))/2)
    #If there is no diffuse radiation and the sun is behind the context surface
    elif math.isnan(theta) and I_dif == 0:
        Rad_tilt=0
    #If the sun is in front of the context surface
    else:
        Rad_tilt = I_dirnor * np.cos(theta) + I_dif * ((1+np.cos(panelAlt))/2) + I_h * ref * ((1- np.cos(panelAlt))/2)

    if Rad_tilt < 0:
        
        #Rad_tilt = 0
        Rad_tilt = I_dif * ((1+np.cos(panelAlt))/2) + I_h * ref * ((1- np.cos(panelAlt))/2)
    
    
    return Rad_tilt # W/m2


  
def calcShadow(P0,sunAz,sunAlt,panelAz,panelAlt,h,d):
	

	#Calculate Centre of Shadow
	S0=[0,0] #initialise Centre of Shadow
	S0[0]=P0[0]+d*math.tan(sunAz)
	S0[1]=P0[1]-d*math.tan(sunAlt)


	#Calcuate the contraction or expansion of the shadow in the x and y directions due to the actuation
	#The difference is relative to the flat panel position
	y=(math.sin(sunAlt-panelAlt/2)/(math.sin(math.pi/2-sunAlt)))*h*math.sin(panelAlt/2) 
	#print y
	x=(math.sin(sunAz-panelAz/2)/(math.sin(math.pi/2-sunAz)))*h*math.sin(panelAz/2)
	#print x
     
#	     S2
#	    /\
#	   /S0\
#	S1 \' / S3
#	    \/
#	    S4  
	
	S2=[S0[0], S0[1]+h+y] # changed not dividing through 2
	S3=[S0[0]+h+x,S0[1]]
	S4=[S0[0], S0[1]-h-y]
	S1=[S0[0]-h-x,S0[1]]


	return S0,S1,S2,S3,S4,y,x
      
def Distance (P1,P2):
    #Distance between two points
    p1, p2 = Point(P1[0], P1[1]), Point(P2[0], P2[1])
    Dis = p1.distance(p2)
    return abs(Dis)

    
def Area(Dict):
    #calcualte area of polygon
    ListASF = Dict
    p1, p2, p3, p4 = map(Point, [(ListASF[0][0], ListASF[0][1]), (ListASF[1][0], ListASF[1][1]), 
                             (ListASF[2][0], ListASF[2][1]), (ListASF[3][0], ListASF[3][1])])
    poly1 = Polygon(p1, p2, p3, p4)
    
    resultASF = abs(round(float(poly1.area),2)) #mm2
    
    return resultASF
    

def CaseA(ind, SunAngles, ASF_dict_prime, PanelNum, row2, col, Case):
    
   
    #SunAngles['Azimuth'][ind] >= 180
    Case_tic=time.time()
                                
    print 'Altitude', SunAngles['Altitude'][ind]
    print 'Azimuth', SunAngles['Azimuth'][ind]
    

    Shadow = {}
    ASFArea = {}
    ShadowLong = {}
    ShadowLat = {}
    IntersectionPoints = {}

    
    for zz in range(PanelNum): 
           
        Shadow[zz] = 0
        ShadowLong[zz] = 0
        ShadowLat[zz] = 0
        
        
        p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[zz][0][0], ASF_dict_prime[zz][0][1]), (ASF_dict_prime[zz][1][0], ASF_dict_prime[zz][1][1]), 
                                 (ASF_dict_prime[zz][2][0], ASF_dict_prime[zz][2][1]), (ASF_dict_prime[zz][3][0], ASF_dict_prime[zz][3][1])])
                               
        ASFArea[zz] = abs(Polygon(p1, p2, p3, p4).area)
    
    
    if '1' in Case:
        print '\nCase A1: horizontal shading'
        
        
     
        for ii in range(1,PanelNum):
            IntersectionPoints[ii] = []
            
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
                
                Shadow[ii]= float(resultShadow)
                
                Dis1 = Distance(P1 = ASF_dict_prime[ii][0], P2 =  SP2) # latitudinal shading length
                Dis2 = Distance(P1 = ASF_dict_prime[ii][0] , P2 =  ASF_dict_prime[ii][3]) # latitudinal panel length
                ShadowLat[ii] = float(Dis1 / Dis2) # percentage latitudinal shading
                
                
                Dis3 = Distance(P1 = ASF_dict_prime[ii][0], P2 = SP1 )
                Dis4 = Distance(P1 = ASF_dict_prime[ii][0] , P2 =  ASF_dict_prime[ii][1])
                ShadowLong[ii] = float(Dis3 / Dis4)            
                
      
                print "Panel: ", ii 
                print "Intersection with panel to the left: Yes"    
                
            else:
                pass
#                print "Panel: ", ii
#                print "Intersection with panel to the left: No"
                
    print 'time after Case 1', time.time()-Case_tic   

            
    if '2' in Case:
            
        print '\nCase A2: diagonal shading'
        for ii in range(1,row2): 
            #case: check if the lowest edge of  a panel is intersection with panel below
            for colNum in range(col): 
            
                                
                if (colNum + ii *col) < PanelNum: #skip the last panels 
                
                    p = Polygon((ASF_dict_prime[colNum + ii *col][0][0],ASF_dict_prime[colNum + ii *col][0][1]),
                                (ASF_dict_prime[colNum + ii *col][1][0],ASF_dict_prime[colNum + ii *col][1][1]),
                                (ASF_dict_prime[colNum + ii *col][2][0],ASF_dict_prime[colNum + ii *col][2][1]),
                                (ASF_dict_prime[colNum + ii *col][3][0],ASF_dict_prime[colNum + ii *col][3][1]))
        
                
                    if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                        #if Point is in polygon p, than true will be returned
                    
        
                        #Calculate Intersection               
                        p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[colNum + ii *col][0][0], ASF_dict_prime[colNum + ii *col][0][1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), 
                                             (ASF_dict_prime[colNum + ii *col][2][0], ASF_dict_prime[colNum + ii *col][2][1]), (ASF_dict_prime[colNum + ii *col][3][0], ASF_dict_prime[colNum + ii *col][3][1])])
                
                
                        p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][1]),
                                             (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])])
                
                        poly1 = Polygon(p1, p2, p3, p4)
                        poly2 = Polygon(p5, p6, p7, p8)
                
                        a =  poly1.intersection(poly2)
                        SP3 = a[0]
                        SP4 = a[1]
                                               
    
                        
                        resultShadow2 = abs(Polygon((SP4[0],SP4[1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), (SP3[0],SP3[1]),
                                                 (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
                
                                
                        Shadow[colNum + ii *col] += float(resultShadow2)
                        
                        Dis1 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1], P2 =  SP4) # latitudinal shading length
                        Dis2 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1], P2 =  ASF_dict_prime[colNum + ii *col][2]) # latitudinal panel length
                        ShadowLat[colNum + ii *col] += float(Dis1/Dis2) # percentage latitudinal shading
                
                        Dis3 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1], P2 =  SP3)
                        Dis4 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1] ,P2 =  ASF_dict_prime[colNum + ii *col][0])
                        ShadowLong[colNum + ii *col] += float(Dis3/Dis4)      
                
                            
                        print "Panel: ", colNum + ii *col
                        print "Intersection with upper panel: Yes" 
                        
                    else:
                        pass
#                        print "Panel: ", colNum + ii *col
#                        print "Intersection with upper panel: No"
                        
                else:
                    pass
    print 'time after Case 2', time.time()-Case_tic 

    #10 seconds of computational time               
    if '3' in Case:                
        print '\nCase A3: vertical shading'              
                          
        for ii in range(2,row2): #row2 = yArray, col = xArray
        
                #case: check if the lowest edge of  a panel is intersection with panel below
            for colNum in range(col): 
            
                if (colNum + ii *col-1) < PanelNum: #skip the last panels 
                    
                    dot = colNum + ii *col -1
                
                    p = Polygon((ASF_dict_prime[dot][0][0],ASF_dict_prime[dot][0][1]),
                                (ASF_dict_prime[dot][1][0],ASF_dict_prime[dot][1][1]),
                                (ASF_dict_prime[dot][2][0],ASF_dict_prime[dot][2][1]),
                                (ASF_dict_prime[dot][3][0],ASF_dict_prime[dot][3][1]))
                    
                
                    if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])):
                        #if Point is in polygon p, than true will be returned
                    
        
                        #Calculate Intersection               
                        p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[dot][0][0], ASF_dict_prime[dot][0][1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), 
                                             (ASF_dict_prime[dot][2][0], ASF_dict_prime[dot][2][1]), (ASF_dict_prime[dot][3][0], ASF_dict_prime[dot][3][1])])
                
                
                        p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-2) *col)][0][0], ASF_dict_prime[(colNum + (ii-2) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][1][0], ASF_dict_prime[(colNum + (ii-2) *col)][1][1]),
                                             (ASF_dict_prime[(colNum + (ii-2) *col)][2][0], ASF_dict_prime[(colNum + (ii-2) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])])
                
                        poly1 = Polygon(p1, p2, p3, p4)
                        poly2 = Polygon(p5, p6, p7, p8)
                
                        a =  poly1.intersection(poly2)
                        SP5 = a[0]
                        SP6 = a[1]
                        
                        
       
                        
                        resultShadow2 = abs(Polygon((SP6[0],SP6[1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), (SP5[0],SP5[1]),
                                                 (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])).area)
                
                        
                        Shadow[dot] += float(resultShadow2)
                        
                        Dis1 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP6) # latitudinal shading length
                        Dis2 = Distance(P1 =  ASF_dict_prime[dot][1], P2 =  ASF_dict_prime[dot][2]) # latitudinal panel length
                        ShadowLat[dot] += float(Dis1 / Dis2) # percentage latitudinal shading
                
                        Dis3 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP5)
                        Dis4 = Distance(P1 = ASF_dict_prime[dot][1] , P2 =  ASF_dict_prime[dot][0])  
                        ShadowLong[dot] += float(Dis3 / Dis4)
                            
                        print "Panel: ", dot
                        print "Intersection with second upper panel: Yes" 

                    else:
                        pass
#                        print "Panel: ", dot
#                        print "Intersection with second upper panel: No"
                       
                else:
                    pass
    print 'time after Case 3', time.time()-Case_tic


    TotalArea = 0
    NonShadedArea = 0
    for ii in range(PanelNum):       
           #print "Panel: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
           NonShadedArea += ASFArea[ii]-Shadow[ii]
           TotalArea += ASFArea[ii]
           
    
    #Calculate Percentage of non overlapped area
    Percentage = NonShadedArea/(TotalArea)

    
    return Percentage, ShadowLat, ShadowLong 
    

def CaseB(ind, SunAngles, ASF_dict_prime, PanelNum, row2, col, Case):

    
    #SunAngles['Azimuth'][ind] < 90
    
                            
    print 'Altitude', SunAngles['Altitude'][ind]
    print 'Azimuth', SunAngles['Azimuth'][ind]
    Case_tic=time.time()
       
    Shadow = {}
    ASFArea = {}
    ShadowLong = {}
    ShadowLat = {}

    
    for zz in range(PanelNum):
        Shadow[zz] = 0
        ShadowLong[zz] = 0
        ShadowLat[zz] = 0
        
        p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[zz][0][0], ASF_dict_prime[zz][0][1]), (ASF_dict_prime[zz][1][0], ASF_dict_prime[zz][1][1]), 
                                 (ASF_dict_prime[zz][2][0], ASF_dict_prime[zz][2][1]), (ASF_dict_prime[zz][3][0], ASF_dict_prime[zz][3][1])])
                          
        ASFArea[zz] = abs(Polygon(p1, p2, p3, p4).area)
       

    
    if '1' in Case: 
        print '\nCase B1: horizontal shading'
               
        
        for ii in range(1,PanelNum):
            #case: if far left point of panel is within the panel to the left
            p = Polygon((ASF_dict_prime[ii-1][0][0],ASF_dict_prime[ii-1][0][1]),
                        (ASF_dict_prime[ii-1][1][0],ASF_dict_prime[ii-1][1][1]),
                        (ASF_dict_prime[ii-1][2][0],ASF_dict_prime[ii-1][2][1]),
                        (ASF_dict_prime[ii-1][3][0],ASF_dict_prime[ii-1][3][1]))
            
            if p.encloses_point(Point(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1])):
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
                
                
        
                Shadow[ii-1]= float(resultShadow)
                
                
                Dis1 = Distance(P1 = ASF_dict_prime[ii-1][2], P2 = SP2) # latitudinal shading length
                Dis2 = Distance(P1 = ASF_dict_prime[ii-1][2] ,P2 = ASF_dict_prime[ii-1][3]) # latitudinal panel length
                ShadowLat[ii-1] = float(Dis1/ Dis2) # percentage latitudinal shading
                
                Dis3 = Distance(P1 = ASF_dict_prime[ii-1][1], P2 = SP1)
                Dis4 = Distance(P1 = ASF_dict_prime[ii-1][1], P2 =  ASF_dict_prime[ii][2])
                ShadowLong[ii-1] = float(Dis3 / Dis4)      
                
                          
                print "Panel: ", ii-1
                print "Intersection with panel to the right: Yes"    
                
            else:            
                pass
#                print "Panel: ", ii-1 
#                print "Intersection with panel to the right: No"
                
    print 'time after Case 1', time.time()-Case_tic  

    #10 seconds of computational time           
    if '2' in Case:
        print '\nCase B2: diagonal shading'
        
        for ii in range(1,row2): #2
            #case: check if the lowest edge of  a panel is intersection with panel below
            for colNum in range(col): #4
            
                                
                if (colNum-1) + ii *col < PanelNum: #skip the last panels 
                    
                
                    p = Polygon((ASF_dict_prime[(colNum-1) + ii *col][0][0],ASF_dict_prime[(colNum-1) + ii *col][0][1]),
                                (ASF_dict_prime[(colNum-1) + ii *col][1][0],ASF_dict_prime[(colNum-1) + ii *col][1][1]),
                                (ASF_dict_prime[(colNum-1) + ii *col][2][0],ASF_dict_prime[(colNum-1) + ii *col][2][1]),
                                (ASF_dict_prime[(colNum-1) + ii *col][3][0],ASF_dict_prime[(colNum-1) + ii *col][3][1]))
    
                
                    if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                        #if Point is in polygon p, than true will be returned
                    
    
                        #Calculate Intersection               
                        p1, p2, p3, p4 = map(Point,[(ASF_dict_prime[(colNum-1) + ii *col][0][0], ASF_dict_prime[(colNum-1) + ii *col][0][1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][1]), 
                                             (ASF_dict_prime[(colNum-1) + ii *col][2][0], ASF_dict_prime[(colNum-1) + ii *col][2][1]), (ASF_dict_prime[(colNum-1) + ii *col][3][0], ASF_dict_prime[(colNum-1) + ii *col][3][1])])
                
                
                        p5, p6, p7, p8 = map(Point,[(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][1]),
                                             (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])])
                
                        poly1 = Polygon(p1, p2, p3, p4)
                        poly2 = Polygon(p5, p6, p7, p8)
                
                        a =  poly1.intersection(poly2)
                        SP1 = a[0]
                        SP2 = a[1]
                        
                               
                        
                        resultShadow2 = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][1]), (SP1[0],SP1[1]),
                                                 (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
                
                                
                        Shadow[(colNum-1) + ii *col] += float(resultShadow2)
                        
                        Dis1 = Distance(P1 = ASF_dict_prime[(colNum-1) + ii *col][1], P2 =  SP2) # latitudinal shading length
                        Dis2 = Distance(P1 =  ASF_dict_prime[(colNum-1) + ii *col][1], P2 =  ASF_dict_prime[(colNum-1) + ii *col][2]) # latitudinal panel length
                        ShadowLat[(colNum-1) + ii *col] += float(Dis1 / Dis2) # percentage latitudinal shading
                
                        Dis3 = Distance(P1 = ASF_dict_prime[(colNum-1) + ii *col][1], P2 =  SP1)
                        Dis4 = Distance(P1 = ASF_dict_prime[(colNum-1) + ii *col][1] , P2 =  ASF_dict_prime[(colNum-1) + ii *col][0])
                        ShadowLong[(colNum-1) + ii *col] += float(Dis3 / Dis4)   
                
                            
                        print "Panel: ", (colNum-1) + ii *col
                        print "Intersection with upper panel: Yes"    
                    else:
                        pass
#                        print "Panel: ", (colNum-1) + ii *col
#                        print "Intersection with upper panel: No"
                        
                else:
                    pass
    print 'time after Case 2', time.time()-Case_tic 

    #10 seconds of computational time
    if '3' in Case:        
        print '\nCase B3: vertical shading'              
                          
        for ii in range(2,row2): #row2 = yArray, col = xArray
        
                #case: check if the lowest edge of  a panel is intersection with panel below
            for colNum in range(col): 
            
                if (colNum + ii *col-1) < PanelNum: #skip the last panels 
                    
                    dot = colNum + ii *col -1
                
                    p = Polygon((ASF_dict_prime[dot][0][0],ASF_dict_prime[dot][0][1]),
                                (ASF_dict_prime[dot][1][0],ASF_dict_prime[dot][1][1]),
                                (ASF_dict_prime[dot][2][0],ASF_dict_prime[dot][2][1]),
                                (ASF_dict_prime[dot][3][0],ASF_dict_prime[dot][3][1]))
                    
                
                    if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])):
                        #if Point is in polygon p, than true will be returned
                    
        
                        #Calculate Intersection               
                        p1, p2, p3, p4 = map(Point,[(ASF_dict_prime[dot][0][0], ASF_dict_prime[dot][0][1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), 
                                             (ASF_dict_prime[dot][2][0], ASF_dict_prime[dot][2][1]), (ASF_dict_prime[dot][3][0], ASF_dict_prime[dot][3][1])])
                
                
                        p5, p6, p7, p8 = map(Point,[(ASF_dict_prime[(colNum + (ii-2) *col)][0][0], ASF_dict_prime[(colNum + (ii-2) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][1][0], ASF_dict_prime[(colNum + (ii-2) *col)][1][1]),
                                             (ASF_dict_prime[(colNum + (ii-2) *col)][2][0], ASF_dict_prime[(colNum + (ii-2) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])])
                
                        poly1 = Polygon(p1, p2, p3, p4)
                        poly2 = Polygon(p5, p6, p7, p8)
                
                        a =  poly1.intersection(poly2)
                        SP1 = a[0]
                        SP2 = a[1]
                        
    
                        
                        resultShadow2 = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), (SP1[0],SP1[1]),
                                                 (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])).area)
                
                        
                        Shadow[dot] += float(resultShadow2)
                        
                        Dis1 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP2) # latitudinal shading length
                        Dis2 = Distance(P1 =  ASF_dict_prime[dot][1], P2 =  ASF_dict_prime[dot][2]) # latitudinal panel length
                        ShadowLat[dot] += float(Dis1 / Dis2) # percentage latitudinal shading
                
                        Dis3 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP1)
                        Dis4 = Distance(P1 = ASF_dict_prime[dot][1] , P2 =  ASF_dict_prime[dot][0])  
                        ShadowLong[dot] += float(Dis3/ Dis4) 
                
                        print "Panel: ", dot
                        print "Intersection with second upper panel: Yes" 
                        
                    else:
                        pass
#                        print "Panel: ", dot
#                        print "Intersection with second upper panel: No"
                        
                else:
                    pass
    print 'time after Case 3', time.time()-Case_tic 
                  
    TotalArea = 0
    NonShadedArea = 0
    for ii in range(PanelNum):       
           #print "Panel: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
           NonShadedArea += ASFArea[ii]-Shadow[ii]
           TotalArea += ASFArea[ii]
           
    
    #Calculate Percentage of non overlapped area
    Percentage = NonShadedArea/(TotalArea)
    
    return Percentage, ShadowLat, ShadowLong                                  