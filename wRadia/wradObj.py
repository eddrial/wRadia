'''
Created on 3 Mar 2020

@author: oqb
'''

import radia as rd
import numpy as np
from astropy.wcs.docstrings import name

class wradObjThckPgn(object):
    '''
    classdocs
    
    Simply creates a container to hold all variables going in to radia calls
    '''


    def __init__(self, x, lx, corners, magnetisation = [0,0,0]):
        '''
        Constructor
        
        stores params in object.
        calls radia function and stores identifyin ID
        '''
        
        self.x = x
        self.lx = lx
        self.corners = corners
        self.magnetisation = magnetisation
        
        self.radobj = rd.ObjThckPgn(self.x, self.lx, self.corners, self.magnetisation)
    
if __name__ == '__main__':
    a = wradObjThckPgn(1,2,3)
    print(a.radobj)