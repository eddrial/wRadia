'''
Created on 3 Mar 2020

@author: oqb
'''

import radia as rd
import numpy as np
import copy
from wradia import wrad_mat as wrdm
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class wradObjThckPgn(object):
    '''
    classdocs
    
    Simply creates a container to hold all variables going in to radia calls
    '''


    def __init__(self, x, lx, corners, extrusion_direction = 'x', magnetisation = [0,0,0]):
        '''
        Constructor
        
        stores params in object.
        calls radia function and stores identifyin ID
        '''
        
        self.x = x
        self.lx = lx
        self.corners = corners
        self.extrusion_direction = extrusion_direction
        self.magnetisation = magnetisation
        
        self.vertices = np.zeros((2*len(corners),3))
        self.polygons = [[] for _ in range (2 + len(corners))]
        
        if self.extrusion_direction == 'x':
            for i in range(len(corners)):
                self.vertices[i,:] = np.array([self.x - self.lx/2.0,corners[i][0],corners[i][1]])
                self.vertices[i+len(corners),:] = np.array([self.x + self.lx/2.0,corners[i][0],corners[i][1]])
            
            
        elif self.extrusion_direction == 'y':
            for i in range(len(corners)):
                self.vertices[i,:] = np.array([corners[i][1],self.x - self.lx/2.0,corners[i][0]])
                self.vertices[i+len(corners),:] = np.array([corners[i][1],self.x + self.lx/2.0,corners[i][0]])
        elif self.extrusion_direction == 'z':
            for i in range(len(corners)):
                self.vertices[i,:] = np.array([corners[i][0],corners[i][1],self.x - self.lx/2.0])
                self.vertices[i+len(corners),:] = np.array([corners[i][0],corners[i][1],self.x + self.lx/2.0])
        
        self.polygons[0] =  np.arange(len(corners))
        self.polygons[1] = np.arange(len(corners),2*len(corners))
        
        n = len(corners)
        for i in range(n):
            self.polygons[i+2] = np.array([i,n+i,n+((i+1)%n),(i+1)%n])
        
        self.radobj = rd.ObjThckPgn(self.x, self.lx, self.corners,self.extrusion_direction, self.magnetisation)
        
    def wradMatAppl(self,material):
        self.material = copy.deepcopy(material)
        self.magnetisation = copy.deepcopy(self.material.M)
        self.radobj = rd.MatApl(self.radobj,self.material.radobj)
        
        #Apply Colour
#        magcol = [(2 + y) / 4.0 for y in self.material.M]
#        self.wradObjDrwAtr(magcol)
        
    #Graphics Methods
    def wradObjDrwAtr(self, colour = 'default', linethickness = 2):
        
        if colour == 'default':
            self.set_default_colour = True
            colour = [(2 + y) / 4.0 for y in self.material.M]
        else: 
            self.set_default_colour = False
        
        
        self.colour = colour
        self.linethickness = linethickness
        
        rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        
    def wradSolve(self, prec_r, iter_r):
        self.solved = 1
        
        rd.Solve(self.radobj,prec_r,iter_r)
        #Spatial Transform Methods
    def wradRotate(self,pivot_origin, pivot_vector, rot_magnitude):
        '''trying to write a rotation function
            # u' = quq*
            #u is point
            #q is quaternion representation of rotation angle ( sin (th/2)i, sin(th/2)j, sin (th/2)k, cos (th/2))'''
        q = R.from_quat([pivot_vector[0] * np.sin(rot_magnitude/2.0), 
                             pivot_vector[1] * np.sin(rot_magnitude/2.0),
                             pivot_vector[2] * np.sin(rot_magnitude/2.0),
                             np.cos(rot_magnitude/2.0)])
        #rotate vertices
        for i in range (len(self.vertices)):
            u = self.vertices[i] - pivot_origin
            
        
            self.vertices[i] = q.apply(u)
        
        #rotate magnetisation vector
        self.magnetisation = (q.apply(self.magnetisation)).tolist()
        self.material.M = self.magnetisation
        
        
        # rotate colour
        q = R.from_quat([pivot_vector[0] * np.sin(rot_magnitude/2.0), 
             pivot_vector[1] * np.sin(rot_magnitude/2.0),
             pivot_vector[2] * np.sin(rot_magnitude/2.0),
             np.cos(rot_magnitude/2.0),])
        
        tmpcol = [(4*x - 2) for x in self.colour]
        
        tmpcol = q.apply(tmpcol)
        
        self.colour = [(2+x) / 4.0 for x in tmpcol]
        rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        
        
        #rotate radia object
        rota = rd.TrfRot(pivot_origin,pivot_vector,rot_magnitude)
        rd.TrfOrnt(self.radobj,rota)

    def wradReflect(self,reflection_origin, reflection_vector):
        '''trying to write a reflection function
            # u' = quq
            #u is point
            #q is quaternion representation of rotation angle ( sin (th/2)i, sin(th/2)j, sin (th/2)k, cos (th/2))'''
        
        r = reflection_vector / np.linalg.norm(reflection_vector)  #ai + bj + ck
        tmp = np.zeros(3)
        #reflect vertices
        for i in range (len(self.vertices)):
            u = self.vertices[i] - reflection_origin # xi + yj + zk
            #i x(-a^2 + b^2 + c^2) -2aby    -2acz
            #j y(-b^2 + a^2 + c^2)     -2abx    -2bcz
            #k z(-c^2 + a^2 + b^2)    -2acx    -2bcy

            tmp[0] = u[0] * (-r[0]**2 + r[1]**2 + r[2]**2) -2 * r[0] * (r[1] * u[1] + r[2] * u[2])
            tmp[1] = u[1] * (-r[1]**2 + r[0]**2 + r[2]**2) -2 * r[1] * (r[0] * u[0] + r[2] * u[2])
            tmp[2] = u[2] * (-r[2]**2 + r[0]**2 + r[1]**2) -2 * r[2] * (r[0] * u[0] + r[1] * u[1])
            
        
            self.vertices[i] = tmp
        
        #reflect magnetisation vector
        u = self.magnetisation
        tmp[0] = u[0] * (-r[0]**2 + r[1]**2 + r[2]**2) -2 * r[0] * (r[1] * u[1] + r[2] * u[2])
        tmp[1] = u[1] * (-r[1]**2 + r[0]**2 + r[2]**2) -2 * r[1] * (r[0] * u[0] + r[2] * u[2])
        tmp[2] = u[2] * (-r[2]**2 + r[0]**2 + r[1]**2) -2 * r[2] * (r[0] * u[0] + r[1] * u[1])
        
        self.magnetisation = tmp
        self.material.M = self.magnetisation
        
        #is colour applied at this level?
        
        #reflect the colour
        r = reflection_vector/np.linalg.norm(reflection_vector)  #ai + bj + ck
        tmp = np.zeros(3)
    #reflect colour
        tmpcol = [(4*x - 2) for x in self.colour]
        
        u = tmpcol # xi + yj + zk
        #i x(-a^2 + b^2 + c^2) -2aby    -2acz
        #j y(-b^2 + a^2 + c^2)     -2abx    -2bcz
        #k z(-c^2 + a^2 + b^2)    -2acx    -2bcy

        tmp[0] = u[0] * (-r[0]**2 + r[1]**2 + r[2]**2) -2 * r[0] * (r[1] * u[1] + r[2] * u[2])
        tmp[1] = u[1] * (-r[1]**2 + r[0]**2 + r[2]**2) -2 * r[1] * (r[0] * u[0] + r[2] * u[2])
        tmp[2] = u[2] * (-r[2]**2 + r[0]**2 + r[1]**2) -2 * r[2] * (r[0] * u[0] + r[1] * u[1])
        
    
        tmpcol = tmp
        
        self.colour = [(2+x) / 4.0 for x in tmpcol]
        rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        
        
        #reflect radia object
        refl = rd.TrfPlSym(reflection_origin,reflection_vector)
        rd.TrfOrnt(self.radobj,refl)
        
    def wradTranslate(self,translation_vector):
        '''trying to write a translation function'''

        #translate vertices
        for i in range (len(self.vertices)):
            self.vertices[i] = self.vertices[i] + translation_vector
        
        #translate radia object
        tran = rd.TrfTrsl(translation_vector)
        rd.TrfOrnt(self.radobj,tran)
        
    #Field Transform Methods
    def wradFieldInvert(self):
        '''trying to write a field inversion function'''
        for i in range(len(self.magnetisation)):
            u = -self.magnetisation [i]
            self.magnetisation[i] = u
        self.material.M = self.magnetisation
        
        fieldinvert = rd.TrfInv(self.radobj)
        rd.TrfOrnt(self.radobj,fieldinvert)    

        
        #invert the colour
        tmp = np.zeros(3)
    #reflect colour
        tmpcol = [(4*x - 2) for x in self.colour]
        
        tmpcol[0] = -tmpcol[0]
        tmpcol[1] = -tmpcol[1]
        tmpcol[2] = -tmpcol[2]
        
        self.colour = [(2+x) / 4.0 for x in tmpcol]
        rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        
        
#        self.radobj.TrfInv()
        
#        rd.TrfOrnt(self.radobj,fieldinvert)
            
    def wradFieldRotate(self,pivot_origin, pivot_vector, rot_magnitude):
        '''trying to write a rotation function
            # u' = quq*
            #u is point
            #q is quaternion representation of rotation angle ( sin (th/2)i, sin(th/2)j, sin (th/2)k, cos (th/2))'''
        q = R.from_quat([pivot_vector[0] * np.sin(rot_magnitude/2.0), 
                             pivot_vector[1] * np.sin(rot_magnitude/2.0),
                             pivot_vector[2] * np.sin(rot_magnitude/2.0),
                             np.cos(rot_magnitude/2.0)])
        
        #rotate magnetisation vector
        self.magnetisation = q.apply(self.magnetisation)
        self.material.M = self.magnetisation.tolist()
        
        self.material = wrdm.wradMatLin(self.material.ksi,self.material.M)
        rd.MatApl(self.radobj,self.material.radobj)
        
        
        # rotate colour
        q = R.from_quat([pivot_vector[0] * np.sin(rot_magnitude/2.0), 
             pivot_vector[1] * np.sin(rot_magnitude/2.0),
             pivot_vector[2] * np.sin(rot_magnitude/2.0),
             np.cos(rot_magnitude/2.0),])
        
        tmpcol = [(4*x - 2) for x in self.colour]
        
        tmpcol = q.apply(tmpcol)
        
        self.colour = [(2+x) / 4.0 for x in tmpcol]
        rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        
        

    
class wradObjCnt(object):
    
    #Container Methods
    def __init__(self,objectlist = []):
        self.objectlist = objectlist
        self.objectlistradobj = []
        
        for i in range(len(objectlist)):
            self.objectlistradobj.append(self.objectlist[i].radobj)
        
        self.radobj = rd.ObjCnt([])
        
        for i in range(len(objectlist)):
            rd.ObjAddToCnt(self.radobj, self.objectlist[i].radobj)
            
    def wradObjAddToCnt(self, objectlist = []):
        #self.objectlist = objectlist
        
        
        for i in range (len(objectlist)):
            self.objectlistradobj.append(objectlist[i].radobj)
            self.objectlist.append(objectlist[i])
        
        rd.ObjAddToCnt(self.radobj,self.objectlistradobj)
        
    
    #Subdivision Methods
    
    def wradObjDivMag(self,subdivision = [1,1,1]):
        '''subdivision is in x,y,z'''
        
        self.subdivision = subdivision
        rd.ObjDivMag(self.radobj, self.subdivision)
    
    #Spatial Transform Methods
    def wradRotate(self,pivot_origin, pivot_vector, rot_magnitude):
        '''trying to write a rotation function'''
        
        #recur down to overloaded function
        for obj in self.objectlist:
            obj.wradRotate(pivot_origin, pivot_vector, rot_magnitude)
        
    
    def wradTranslate(self, translation_vector):
        '''trying to write a translation function'''
        
        #recur down to overloaded function
        for obj in self.objectlist:
            obj.wradTranslate(translation_vector)#vertices

    
    def wradReflect(self, reflection_origin, reflection_vector):
        '''trying to write a reflection function'''

        #recur down to overloaded function
        for obj in self.objectlist:
            obj.wradReflect(reflection_origin, reflection_vector)
        

    
    # Magnetisation Transformations
    def wradFieldInvert(self):
        '''trying to write a field inversion function'''
        
        #recur down to overloaded function
        for obj in self.objectlist:
            obj.wradFieldInvert()#vertices
    
        #Spatial Transform Methods
    def wradFieldRotate(self,pivot_origin, pivot_vector, rot_magnitude):
        '''trying to write a rotation function'''
        
        #recur down to overloaded function
        for obj in self.objectlist:
            obj.wradFieldRotate(pivot_origin, pivot_vector, rot_magnitude)
    
#Material Methods
    def wradMatAppl(self, material):
        for obj in self.objectlist:
            obj.wradMatAppl(material)
        
        
#Graphics Methods
    def wradObjDrwAtr(self, colour = 'default', linethickness = 2):
        
        for obj in self.objectlist:
            obj.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
#solving methods
    def wradSolve(self, prec_r = 0.001, iter_r = 1000):
        
        rd.Solve(self.radobj,prec_r,iter_r)
        self.solved = 1
        


        
        
#if __name__ == '__main__':
#    tr = 5
#    ve = 3
#    
#    x = wradObjThckPgn(2,2,[[-tr,-ve],[-tr,ve],[tr,ve],[tr,-ve]],'x',[4,3,2])
#    print(x.vertices)
#    
#    y = wradObjThckPgn(2,2,[[-tr,-ve],[-tr,ve],[tr,ve],[tr,-ve]],'y',[4,3,2])
#    print(y.vertices)
#    
#    z = wradObjThckPgn(2,2,[[-tr,-ve],[-tr,ve],[tr,ve],[tr,-ve]],'z',[4,3,2])
#    print(z.vertices)
#    
#    rd.ObjDrwOpenGL(x.radobj)
#    rd.ObjDrwOpenGL(y.radobj)
#    rd.ObjDrwOpenGL(z.radobj)
#    
#    input("Press Enter to continue...")