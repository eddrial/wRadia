'''
Created on 3 Mar 2020

@author: oqb
'''
import unittest
import radia as rd
from wRadia import wradObj as wrd
import numpy as np



class Test(unittest.TestCase):
    #parameters
    
    def test_wradObjThckPgn_exists(self,mainmagthick = 5, origin = [0,0,0]):
        a = rd.ObjThckPgn(0, 5, [[-5,-5],[-5,5],[5,5],[5,-5]],'x',origin)
        assert a == 1
        
        #assert wrd.wradObjThckPgn(0, mainmagthick, ([-5,-5],[-5,5],[5,5],[5,-5]),'x',origin).radobj == 1


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_wradObjThckPgn_exists']
    unittest.main()
    
