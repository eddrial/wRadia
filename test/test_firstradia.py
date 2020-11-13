'''
Created on 26 Feb 2020

@author: oqb
'''
import unittest
from wradia import firstradia as wr
from wradia import wrad_obj as wrd
import radia as rd
import numpy as np


class Test(unittest.TestCase):



    def testsimple(self):
        rd.UtiDelAll()
        cl = wr.wradClaExtr()
        assert cl.cont1 == 1
            
    def testawradO(self):
        rd.UtiDelAll()
        c2 = wrd.wradObjThckPgn(0.0,5.0,[[-5.0,-5.0],[-5.0,5.0],[5.0,5.0],[5.0,-5.0]])
        assert c2.radobj == 1
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testsimpe']
    unittest.main()