'''
Created on 3 Mar 2020

@author: oqb
'''

import radia as rd
import numpy as np
from scipy.spatial.transform import Rotation as R

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
        
        self.radobj = rd.ObjThckPgn(self.x, self.lx, self.corners,self.extrusion_direction, self.magnetisation)
        
    def wradMatAppl(self,material):
        self.material = material
        self.magnetisation = self.material.M
        rd.MatApl(self.radobj,material.radobj)
        
        #Spatial Transform Methods
    def wradRotate(self,pivot_origin, pivot_vector, rot_magnitude):
        '''trying to write a rotation function
            # u' = quq*
            #u is point
            #q is quaternion representation of rotation angle ( sin (th/2)i, sin(th/2)j, sin (th/2)k, cos (th/2))'''
        
        #rotate vertices
        for i in range (len(self.vertices)):
            u = self.vertices[i] - pivot_origin
            q = R.from_quat([pivot_vector[0] * np.sin(rot_magnitude/2.0), 
                             pivot_vector[1] * np.sin(rot_magnitude/2.0),
                             pivot_vector[2] * np.sin(rot_magnitude/2.0),
                             np.cos(rot_magnitude/2.0)])
        
            self.vertices[i] = q.apply(u)
        
        #rotate magnetisation vector
        self.magnetisation = q.apply(self.magnetisation)
        
        #rotate radia object
        rota = rd.TrfRot(pivot_origin,pivot_vector,rot_magnitude)
        rd.TrfOrnt(self.radobj,rota)
            
  

    
class wradObjCnt(object):
    
    #Container Methods
    def __init__(self,objectlist = []):
        self.objectlist = objectlist
        
        self.radobj = rd.ObjCnt([])
        
        for i in range(len(objectlist)):
            rd.ObjAddToCnt(self.radobj, self.objectlist[i].radobj)
            
    def wradObjAddToCnt(self, objectlist = []):
        #self.objectlist = objectlist
        
        if hasattr(self,'objectlist'):
            pass
        else:
            self.objectlist = objectlist
        
        if hasattr(self, 'objectlistradobj'):
            pass
        else:
            self.objectlistradobj = []
        
        for i in range (len(objectlist)):
            self.objectlistradobj.append(objectlist[i].radobj)
            self.objectlist.append(objectlist[i])
        
        
            
        rd.ObjAddToCnt(self.radobj,self.objectlistradobj)
        
    
    #Subdivision Methods
    
    def wradObjDivMag(self,subdivision = [3,3,3]):
        '''subdivision is in x,y,z'''
        
        self.subdivision = subdivision
        rd.ObjDivMag(self.radobj, self.subdivision)
    
    #Spatial Transform Methods
    def wradRotate(self,pivot_origin, pivot_vector, rot_magnitude):
        '''trying to write a rotation function'''
        
        #is this a container, or a primitive... check for object list
        try:
            self.objectlist
        except AttributeError:
            pass

        #is colour applied at this level?
        try:
            self.colour
            #if yes rotate colour
            q = R.from_quat([pivot_vector[0] * np.sin(rot_magnitude/2.0), 
                 pivot_vector[1] * np.sin(rot_magnitude/2.0),
                 pivot_vector[2] * np.sin(rot_magnitude/2.0),
                 np.cos(rot_magnitude/2.0),])
            
            tmpcol = [(4*x - 2) for x in self.colour]
            
            tmpcol = q.apply(tmpcol)
            
            self.colour = [(2+x) / 4.0 for x in tmpcol]
            rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        except:
            pass
        
        #recur down to overloaded function
        for obj in self.objectlist:
            obj.wradRotate(pivot_origin, pivot_vector, rot_magnitude)
        
    
    def wradTranslate(self):
        #vertices
        #magnetisation
        pass
    
    def wradReflect(self):
        #vertices
        #magnetisation
        pass
    
    
    
#Material Methods
    def wradMatAppl(self, material):
        try:
            self.objectlist
        except AttributeError:
            self.material = material
            rd.MatApl(self.radobj,material.radobj)
        
        for obj in self.objectlist:
            obj.wradMatAppl(material)
        
        
#Graphics Methods
    def wradObjDrwAtr(self, colour, linethickness):
        self.colour = colour
        self.linethickness = linethickness
        
        rd.ObjDrwAtr(self.radobj,self.colour, self.linethickness)
        
        
#solving methods
    def wradSolve(self, prec_r, iter_r):
        self.solved = 1
        
        rd.Solve(self.radobj,prec_r,iter_r)
    
        
        
        
        
if __name__ == '__main__':
    tr = 5
    ve = 3
    
    x = wradObjThckPgn(2,2,[[-tr,-ve],[-tr,ve],[tr,ve],[tr,-ve]],'x',[4,3,2])
    print(x.vertices)
    
    y = wradObjThckPgn(2,2,[[-tr,-ve],[-tr,ve],[tr,ve],[tr,-ve]],'y',[4,3,2])
    print(y.vertices)
    
    z = wradObjThckPgn(2,2,[[-tr,-ve],[-tr,ve],[tr,ve],[tr,-ve]],'z',[4,3,2])
    print(z.vertices)
    
    rd.ObjDrwOpenGL(x.radobj)
    rd.ObjDrwOpenGL(y.radobj)
    rd.ObjDrwOpenGL(z.radobj)
    
    input("Press Enter to continue...")