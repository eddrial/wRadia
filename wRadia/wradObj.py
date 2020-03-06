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
        
        self.radobj = rd.ObjThckPgn(self.x, self.lx, self.corners,self.extrusion_direction, self.magnetisation)
        
    
class wradObjCnt(object):
    
    def __init__(self,objectlist = []):
        self.objectlist = objectlist
        
        self.radobj = rd.ObjCnt([])
        
        for i in range(len(objectlist)):
            rd.ObjAddToCnt(self.radobj, self.objectlist[i].radobj)
        
class wradObjAddToCnt(object):
    
    def __init__(self,existingobject, objectlist):
        self.objectlist = objectlist
        self.radobj = rd.ObjAddToCnt(existingobject,objectlist)
    
if __name__ == '__main__':
    a = wradObjThckPgn(2,2,[[-5,-5],[-5,5],[5,5],[5,-5]],'x',[4,3,2])
    print(a.radobj)