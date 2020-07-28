'''
Created on 28 Jul 2020

@author: oqb
'''
import unittest
import radia as rd
from wRadia import wradObj as wrd
from wRadia import wradMat
import numpy as np



class Test(unittest.TestCase):
    def test_wradMat_ksi(self):
        rd.UtiDelAll()
        ksi = [.019, .06]
        M = [0,0,1.5]
        a = wradMat.wradMatLin(ksi,M)
        
        assert a.ksi == [.019, .06]
        
    def test_wradMat_M(self):
        rd.UtiDelAll()
        ksi = [.019, .06]
        M = [0,0,1.5]
        a = wradMat.wradMatLin(ksi,M)
        
        assert a.M ==  [0,0,1.5]
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_wradObjThckPgn_exists']
    unittest.main()