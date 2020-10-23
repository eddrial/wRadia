'''
Created on 6 Mar 2020

@author: oqb

Just a collection of different classes, as each radMatLin is a different kind of object, and contains no methods
'''

import radia as rd
import numpy as np

class wradMatLin(object):
    '''
    classdocs
    '''


    def __init__(self, ksi, M=[0,0,0]):
        '''
        Constructor
        
        
        
        '''
        self.ksi = ksi
        self.M = M
        
        self.radobj = rd.MatLin(self.ksi,self.M)
        
if __name__ == '__main__':
    pass