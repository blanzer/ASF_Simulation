
import math
import numpy as np

from sympy.solvers import solve
from sympy import Symbol

#http://math.stackexchange.com/questions/164700/how-to-transform-a-set-of-3d-vectors-into-a-2d-plane-from-a-view-point-of-anoth
room_height = 3100.
room_depth = 7000.
room_width = 4900.


#S1 = [-2500,0,0]
#S2 = [4000,10,0]
#S3 = [-2500,0,5000]




SunVec = np.array([-0.92, 0.35 ,-0.2])*10000
#SunVec = np.array([0.92, -35 ,2])*1000

PanelNum = 4

PanelSize = 1100. #mm

Hyp = np.sin(np.deg2rad((45)))*PanelSize
DistWindow = 500. # distance of panels from Window surface

xAngle = 0
yAngle = 0

xAngle = np.deg2rad(xAngle)
yAngle = np.deg2rad(yAngle)


xR = 0 + 20000
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

#ASF = [[xR + room_width/2-np.sqrt(2)/2*PanelSize, yR , zR + room_height/2],
#        [xR + room_width/2, yR, zR + room_height/2 + np.sqrt(2)/2*PanelSize],
#        [xR + room_width/2 + np.sqrt(2)/2*PanelSize,yR, zR + room_height/2],
#        [xR + room_width/2, yR, zR + room_height/2 - np.sqrt(2)/2*PanelSize]]

from scipy.optimize import fsolve

def ProjPlane(S1, n):
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
        F[2] = x-1
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

S1 = [1,0,0]

S2, S3 = ProjPlane(S1 = S1, n = SunVec)

#S4 = np.array(S2) - (np.array(S1)-np.array(S3))



ASF_dict = {}



for jj in range(PanelNum):
    
    xR1 = [-room_width/4 + xR, room_width * 1/4. + xR , -room_width/4. + xR, room_width * 1/4. + xR]
    yR1 = [DistWindow + yR]* 4 
    zR1 = [room_height/4. + zR ,room_height/4. + zR, -room_height/4. + zR, -room_height/4. + zR]
    
    # 2   
    #1 3   
    # 4   
    ASF_dict[jj] = [[xR1[jj] + room_width/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(yAngle)*Hyp),    yR1[jj] + np.sin(yAngle)* Hyp ,     zR1[jj] + room_height/2], #1
                    [xR1[jj] + room_width/2 ,                            yR1[jj] - np.sin(xAngle)*Hyp,                            zR1[jj] + room_height/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(xAngle)*Hyp)],#2
                    [xR1[jj] + room_width/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(yAngle)*Hyp),    yR1[jj] - np.sin(yAngle)* Hyp ,      zR1[jj] + room_height/2], #3
                    [xR1[jj] + room_width/2 ,                            yR1[jj] + np.sin(xAngle)*Hyp,                            zR1[jj] + room_height/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(xAngle)*Hyp)]] #4








def PointPro(S1, S2, S3, A, SunVec):
    
    
    
    #creates a Projection of A_prime for A on the plane S
    W = math.sqrt((S2[0]-S1[0])**2 + (S2[1]-S1[1])**2 + (S2[2]-S1[2])**2)
    H = math.sqrt((S3[0]-S1[0])**2 + (S3[1]-S1[1])**2 + (S3[2]-S1[2])**2)
    
    M = [(S2[0] + S3[0])/2.,(S2[1] + S3[1])/2. ,(S2[2] + S3[2])/2. ]
    
    
    a = np.array([[S1[0],S1[1],S1[2]], [S2[0],S2[1],S2[2]],[M[0],M[1],M[2]]])
    b = np.array([1,1,1])
    coef = np.linalg.solve(a, b)
    #print coef
    #
    #print np.allclose(np.dot(a, coef), b)
    
    N = [coef[0]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[1]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[2]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2)]
    #Camera Point    
    #C = [M[0]+ h*N[0], M[1]+ h*N[1] , M[2]+ h*N[2]]
    
    
    #find projection of A, Aprime
    k = Symbol('k')
    k = solve(coef[0]*(k*SunVec[0]+ A[0]) + coef[1]*(k*SunVec[1]+ A[1]) + coef[2]*(k*SunVec[2] + A[2]) -1, k)
    k = k[0]
        
    APrime = [round( (k*(SunVec[0])+ A[0]),2), round((k*(SunVec[1])+ A[1]),2), round((k*(SunVec[2])+ A[2]),2)] 
        
    
    
    #find projection of A, Aprime
#    k = Symbol('k')
#    k = solve(coef[0]*(k*(C[0]-A[0])+ A[0]) + coef[1]*(k*(C[1]-A[1])+ A[1]) + coef[2]*(k*(C[2]-A[2])+ A[2]) -1, k)
#    k = k[0]
#    print k
#    
#    APrime = [(k*(C[0]-A[0])+ A[0]), (k*(C[1]-A[1])+ A[1]), (k*(C[2]-A[2])+ A[2])] 
    
    
   
    
    n2 = (W* np.sqrt( int((APrime[0]-S1[0])**2 + (APrime[1]-S1[1])**2 + (APrime[2]-S1[2])**2)))
    
    #cos(u)
    n3 = ((S2[0]-S1[0])*(APrime[0]-S1[0]) + (S2[1]-S1[1])*(APrime[1]-S1[1])+ (S2[2]-S1[2])*(APrime[2]-S1[2]))/n2
    
    u = np.arccos(round(n3,4))
    
    m = np.sqrt(round((APrime[0]-S1[0])**2 + (APrime[1]-S1[1])**2 + (APrime[2]-S1[2])**2, 4)) * n3
    
    n = np.sqrt(round((APrime[0]-S1[0])**2 + (APrime[1]-S1[1])**2 + (APrime[2]-S1[2])**2, 4)) * np.sin(u)
    
    #APrime = ((k*(C[0]-A[0])+ A[0]), (k*(C[1]-A[1])+ A[1]), (k*(C[2]-A[2])+ A[2]))
    
    
    return APrime
    
    


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

#for ii in ASF:
#    Prime, C = PointPro(S1 = S1, S2 = S2, S3= S3, A = ii, h = h)
#    ASFPrime.append(Prime)
#    ASFX.append(Prime[0])
#    ASFY.append(Prime[1])
#    ASFZ.append(Prime[2])


ASF_dict_prime = {}

count = 0    
for ii in range(len(ASF_dict)):
    ASFPrime = []
    
    for jj in range(PanelNum):
        Prime = PointPro(S1 = S1, S2 = S2, S3= S3, A = ASF_dict[ii][jj], SunVec = SunVec)
        ASFPrime.append(Prime)
        
        ASFX.append(Prime[0])
        ASFX.append(ASF_dict[ii][jj][0])

        ASFY.append(Prime[1])
        ASFY.append(ASF_dict[ii][jj][1])

        ASFZ.append(Prime[2])
        ASFZ.append(ASF_dict[ii][jj][2])        
        count += 1
        
    ASF_dict_prime[ii] = ASFPrime

        
        




from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D



fig = pylab.figure()
ax = Axes3D(fig)



x_vals = ASFX + ListX + [SunVec[0]] #[S1[0], S2[0], S3[0], S4[0],
y_vals = ASFY + ListY + [SunVec[1]] #S1[1], S2[1], S3[1], S4[1], 
z_vals = ASFZ + ListZ + [SunVec[2]] #S1[2], S2[2], S3[2], S4[2], 

for nn in range(len(room)):
    x_vals.append(room[nn][0])
    y_vals.append(room[nn][1])
    z_vals.append(room[nn][2])
    
#for nn in range(len(ASF)):
#    x_vals.append(ASF[nn][0])
#    y_vals.append(ASF[nn][1])
#    z_vals.append(ASF[nn][2])    
    

#x_vals = np.append(roomX[0], np.array(ListX, dtype = np.float64), np.array([S1[0], S2[0], S3[0], S4[0], C[0]]))
#y_vals = np.append(roomY[0], np.array(ListY, dtype = np.float64), np.array([S1[1], S2[1], S3[1], S4[1], C[1]]))
#z_vals = np.append(roomZ[0], np.array(ListZ, dtype = np.float64), np.array([S1[2], S2[2], S3[2], S4[2], C[2]]))


ax.scatter(x_vals, y_vals, z_vals, s=3)
#ax.scatter(ListX, ListY, ListZ)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
#ax.view_init(45,60)
ax.view_init(0,90)
#ax.view_init(45,60)
pyplot.show()


def AreaCalc(poly):
    #calculate area of 3D polygon
    #determinant of matrix a
    def det(a):
        return a[0][0]*a[1][1]*a[2][2] + a[0][1]*a[1][2]*a[2][0] + a[0][2]*a[1][0]*a[2][1] - a[0][2]*a[1][1]*a[2][0] - a[0][1]*a[1][0]*a[2][2] - a[0][0]*a[1][2]*a[2][1]
    
    #unit normal vector of plane defined by points a, b, and c
    def unit_normal(a, b, c):
        x = det([[1,a[1],a[2]],
                 [1,b[1],b[2]],
                 [1,c[1],c[2]]])
        y = det([[a[0],1,a[2]],
                 [b[0],1,b[2]],
                 [c[0],1,c[2]]])
        z = det([[a[0],a[1],1],
                 [b[0],b[1],1],
                 [c[0],c[1],1]])
        magnitude = (x**2 + y**2 + z**2)**.5
        return (x/magnitude, y/magnitude, z/magnitude)
    
    #dot product of vectors a and b
    def dot(a, b):
        return np.dot(a,b)
    
    #cross product of vectors a and b
    def cross(a, b):

        return np.cross(a,b)
    
    #area of polygon poly
    def area(poly):
        if len(poly) < 3: # not a plane - no area
            return 0
    
        total = [0, 0, 0]
        for i in range(len(poly)):
            vi1 = poly[i]
            if i is len(poly)-1:
                vi2 = poly[0]
            else:
                vi2 = poly[i+1]
            prod = cross(vi1, vi2)
            total[0] += prod[0]
            total[1] += prod[1]
            total[2] += prod[2]
        result = dot(total, unit_normal(poly[0], poly[1], poly[2]))
        return result
        
    result = area(poly)
    
    return abs(result/2) * 10**(-6) #m2

for tt in range(len(ASF_dict)):
    result1 = AreaCalc(poly = ASF_dict[tt])
    print "ASF", result1    
    result2 = AreaCalc(poly = ASF_dict_prime[tt])
    print "Prime", result2



def createPlane(P1, P2, P3):
    # P1 + lambda* r1 + mü * r2, parameterform
    R1 = []
    R2 = []
    
    R1 = [P2[0]-P3[0], P2[1]-P3[1], P2[2]-P3[2]]
     
    R2 = [P2[0]-P1[0], P2[1]-P1[1], P2[2]-P1[2]]
    
    
    #coordinates of plane
    n = np.cross(R1,R2)
    
    #value of plane
    a = np.dot(n,P1)
#    print n
#    print a
    return n, a



def Intersect(n, a, vec, vecSt):
    #intersection between plane and vector
    #plane normal vector n, a = result of plane equation
    #vecSt = startpoint, vec = vector

    lamb = Symbol('lamb')
    lamb = solve((vecSt[0] + lamb *vec[0])*n[0] + (vecSt[1] + lamb*vec[1])*n[1] + (vecSt[2] + lamb*vec[2])*n[2] - a, lamb)
    lamb = lamb[0]
    IntPoint = [vecSt[0] + lamb* vec[0], vecSt[1] + lamb* vec[1], vecSt[2] + lamb* vec[2]]
    #print IntPoint
    return IntPoint

vecSt = [1000,1000,1000]
vecSt2 = [100,100,100]
n, a = createPlane(S1,S2,S3)

IntPoint =  Intersect(n = n ,a = a, vec = SunVec, vecSt = vecSt)


def DisPoints (P1,P2):
    distance = np.sqrt( (P1[0]-P2[0])**2 + (P1[1]-P2[1])**2 + (P1[2]-P2[2])**2)
    #print distance    
    return distance
    
distan = DisPoints(P1 = vecSt, P2 = vecSt2)



def Area2D(P1, P2, P3):
    from numpy import linalg as LA
    # calculate area of 3 dots, use for window surface, input mm output m2
    vec1 = [P1[0]-P2[0], P1[1]-P2[1], P1[2]-P2[2]]
    vec2 = [P1[0]-P3[0], P1[1]-P3[1], P1[2]-P3[2]]    
    
    n = np.cross(vec1, vec2)
    Len_N = LA.norm(n) * 10**(-6) #m2
    
    return Len_N
    
    
areaReal = Area2D(P1 = room[0], P2 = room[1], P3 = room[2])
print "Area Real: ", areaReal    

areaPro = Area2D(P1 = RoomPrime[0], P2 = RoomPrime[1], P3 = RoomPrime[2])
print "Area Projection: ", areaPro



test = [[1,0,1], [2,0,1.5], [1,0,2], [0.75,0,0.75], [0.5,0,1.5], [0.75, 0, 0.25]]    

result1 = AreaCalc(poly = test)
print "ASF", result1 *10**6    



def PointInPlane(P, n, a):
    #Test if Point is placed on Plane
    result = n[0]*P[0] + n[1]*P[1] + n[2]*P[2]
    if a == result:
        return True
    else:
        return False


print PointInPlane(P = S1, n = n, a= a)

def LineInter(C1,C2,C3,C4):
    #create lines from two points c1 and c2 / c3 and c4
    #find intersection of lines
    R1 = [C2[0]- C1[0], C2[1]- C1[1], C2[2]- C1[2]] # C1 + lambda * R1
    R2 = [C4[0]- C3[0], C4[1]- C3[1], C4[2]- C3[2]] # C3 + lambda * R2
    
    print R1
    print R2
    
#    if R1[0]/R2[0] != R1[1]/R2[1]:
#        
#        InterPoint = None
#        return InterPoint
#
#    else:
    
    def SolveLine(w):
        t = w[0]
        s = w[1]
                       
        F = np.empty((2))
        F[0] = C1[0]+ t* R1[0] - C3[0] + s * R2[0]
        F[1] = C1[1]+ t* R1[1] - C3[1] + s * R2[1]
        
        return F

    zGuess = np.array([1,1])
    w = fsolve(SolveLine, zGuess)
    InterPoint = [C1[0] + w[0] * R1[0], C1[1] + w[0] * R1[1], C1[2] + w[0] * R1[2]]
    
    
    return InterPoint

    



S1 = [-2500,1,2]
S2 = [4000,1,2]
S3 = [-2500,1,5000]
S4 = [4000,1,5000]

IP = LineInter(S1,S3,S2,S4)

print IP    