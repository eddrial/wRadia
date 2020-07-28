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
    
    ###wradObjThckPgn __init__ tests
    def test_wradObjThckPgn_exists(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[0,0,0])
        #rd.ObjThckPgn(0, 5, [[0,10],[0,10],[10,10],[0,0]],'x',origin)
        assert a.radobj == 1
        
        #assert wrd.wradObjThckPgn(0, mainmagthick, ([-5,-5],[-5,5],[5,5],[5,-5]),'x',origin).radobj == 1

    def test_wradObjThckPgn_corners(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[0,0,0])
        
        assert a.corners == [[0,10],[10,10],[10,0],[0,0]]
        
    def test_wradObjThckPgn_extrusion_direction(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[0,0,0])
        
        assert a.extrusion_direction == 'x'
        
    def test_wradObjThckPgn_thickness(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[0,0,0])
        
        assert a.lx == 5
        
    def test_wradObjThckPgn_vertices_x_extrusion(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[0,0,0])
        
        comparison = a.vertices == np.array([[-2.5,  0. , 10. ],[-2.5, 10. , 10. ],[-2.5, 10. ,  0. ],[-2.5,  0. ,  0. ],[ 2.5,  0. , 10. ],[ 2.5, 10. , 10. ],[ 2.5, 10. ,  0. ],[ 2.5,  0. ,  0. ]])

        assert comparison.all()
        
    def test_wradObjThckPgn_vertices_y_extrusion(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'y',[0,0,0])
        
        comparison = a.vertices == np.array([[10. , -2.5,  0. ], [10. , -2.5, 10. ], [ 0. , -2.5, 10. ], [ 0. , -2.5,  0. ], [10. ,  2.5,  0. ], [10. ,  2.5, 10. ], [ 0. ,  2.5, 10. ], [ 0. ,  2.5,  0. ]])

        assert comparison.all()
        
    def test_wradObjThckPgn_vertices_z_extrusion(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'z',[0,0,0])
        
        comparison = a.vertices == np.array([[ 0. , 10. , -2.5], [10. , 10. , -2.5], [10. ,  0. , -2.5], [ 0. ,  0. , -2.5], [ 0. , 10. ,  2.5], [10. , 10. ,  2.5], [10. ,  0. ,  2.5], [ 0. ,  0. ,  2.5]])

        assert comparison.all()
        
    def test_wradObjThckPgn_magnetisation(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
        
        assert a.magnetisation == [1,2,3]
        
    def test_wradObjThckPgn_extrusion_centre_of_mass(self):
        rd.UtiDelAll()
        a = wrd.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
        
        assert a.x == 0
        
    #
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_wradObjThckPgn_exists']
    unittest.main()
    
