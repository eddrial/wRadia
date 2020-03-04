'''
Created on 3 Mar 2020

@author: oqb
'''
import unittest
import wRadia.wradObj as wrdo
import numpy as np

class Test(unittest.TestCase):

#parameters
    origin = np.zeros(3)
    mainmagthick = 5
    mainmagdimension = 30
    clampcut = 5
    
    #instantiate test object
    basic_polygon_magnet = wrdo.wradObjThckPgn(0, mainmagthick, ([-5,-5],[-5,5],[5,5],[5,-5]),'x',origin)
    
    def test_wradObjThckPgn_exists(self):
        assert wrdo.wradObjThckPgn(0, mainmagthick, ([-5,-5],[-5,5],[5,5],[5,-5]),'x',origin).radobj == 1


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_wradObjThckPgn_exists']
    unittest.main()
