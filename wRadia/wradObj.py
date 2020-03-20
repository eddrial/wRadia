'''
Created on 3 Mar 2020

@author: oqb
'''

import radia as rd
import numpy as np

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
        
        self.vertices = []
        
        if self.extrusion_direction == 'x':
            for corner in corners:
                self.vertices.append([self.x - self.lx/2.0,corner[0],corner[1]])
                self.vertices.append([self.x + self.lx/2.0,corner[0],corner[1]])
        elif self.extrusion_direction == 'y':
            for corner in corners:
                self.vertices.append([corner[1],self.x - self.lx/2.0,corner[0]])
                self.vertices.append([corner[1],self.x + self.lx/2.0,corner[0]])
        elif self.extrusion_direction == 'z':
            for corner in corners:
                self.vertices.append([corner[0], corner[1],self.x - self.lx/2.0])
                self.vertices.append([corner[0], corner[1],self.x + self.lx/2.0])
        
        self.radobj = rd.ObjThckPgn(self.x, self.lx, self.corners,self.extrusion_direction, self.magnetisation)
        
    def wradMatAppl(self,material):
        self.material = material
        self.magnetisation = self.material.M
        rd.MatApl(self.radobj,material.radobj)
    
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