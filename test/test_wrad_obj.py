'''
Created on 3 Mar 2020

@author: oqb
'''
import unittest
import radia as rd
import wradia as wrd
import numpy as np
from _pytest.outcomes import fail



class Test_wradObjThckPgn(unittest.TestCase):
    #test wrad object initialisation
    def setUp(self):
        rd.UtiDelAll()
        self.ax = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
        self.ay = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'y',[1,2,3])
        self.az = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'z',[1,2,3])
    ###wradObjThckPgn athenaii tests
    def test_wradObjThckPgn_exists(self):
        assert self.ax.radobj == 1
        

    def test_wradObjThckPgn_corners(self):
        assert self.ax.corners == [[0,10],[10,10],[10,0],[0,0]]
        
    def test_wradObjThckPgn_extrusion_direction(self):

        assert self.ax.extrusion_direction == 'x'
        
    def test_wradObjThckPgn_thickness(self):

        assert self.ax.lx == 5
        
    def test_wradObjThckPgn_vertices_x_extrusion(self):

        comparison = self.ax.vertices == np.array([[-2.5,  0. , 10. ],[-2.5, 10. , 10. ],[-2.5, 10. ,  0. ],[-2.5,  0. ,  0. ],[ 2.5,  0. , 10. ],[ 2.5, 10. , 10. ],[ 2.5, 10. ,  0. ],[ 2.5,  0. ,  0. ]])

        assert comparison.all()
        
    def test_wradObjThckPgn_vertices_y_extrusion(self):

        comparison = self.ay.vertices == np.array([[10. , -2.5,  0. ], [10. , -2.5, 10. ], [ 0. , -2.5, 10. ], [ 0. , -2.5,  0. ], [10. ,  2.5,  0. ], [10. ,  2.5, 10. ], [ 0. ,  2.5, 10. ], [ 0. ,  2.5,  0. ]])

        assert comparison.all()
        
    def test_wradObjThckPgn_vertices_z_extrusion(self):

        comparison = self.az.vertices == np.array([[ 0. , 10. , -2.5], [10. , 10. , -2.5], [10. ,  0. , -2.5], [ 0. ,  0. , -2.5], [ 0. , 10. ,  2.5], [10. , 10. ,  2.5], [10. ,  0. ,  2.5], [ 0. ,  0. ,  2.5]])

        assert comparison.all()
        
    def test_wradObjThckPgn_magnetisation(self):
        assert self.ax.magnetisation == [1,2,3]
        
    def test_wradObjThckPgn_extrusion_centre_of_mass(self):
        assert self.ax.x == 0
        
class Test_wradMatAppl(unittest.TestCase):
    #wradMatAppl. Material tests and application
    def setUp(self):
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [0,0,1.5]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
        self.a.wradMatAppl(self.material)
    
    def test_wradMatAppl_material(self):
        assert self.a.material == self.material
        
    def test_wradMatAppl_magnetisation(self):
        assert self.material.M == self.M
        
    
    def test_wradMatAppl_magnetisation_overwrite(self):
        assert self.material.M == self.a.magnetisation
        
class Test_wradObjThckPgn_resulting_fields_x(unittest.TestCase):
    #check effect of magnetisation being written in each of three dimensions
    def setUp(self):
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [1,0,0]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.a.wradMatAppl(self.material)
        
        self.a.wradSolve(0.001, 10000)
    
    def test_cube_X_magnetisation(self):
        b = rd.Fld(self.a.radobj,'bxbybz',[6.0,0,0])
        self.assertAlmostEqual(b[0], 0.3544116293114718)
    
    def test_cube_X_magnetisation1(self):
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[i*6.0,0,0])
                #self.assertAlmostEqual(b, [0.3544116293114718,0,0])
                np.testing.assert_almost_equal(b,[0.3544116293114718,0,0])
        
class Test_wradObjThckPgn_resulting_fields_y(unittest.TestCase):
    #check effect of magnetisation being written in each of three dimensions
    def setUp(self):
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [0,1,0]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.a.wradMatAppl(self.material)
        
        self.a.wradSolve(0.001, 10000)
    
    def test_cube_Y_magnetisation(self):
        b = rd.Fld(self.a.radobj,'bxbybz',[0,6.0,0])
        self.assertAlmostEqual(b[1], 0.3544116293114718)
    
    def test_cube_Y_magnetisation1(self):
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,i*6.0,0])
                np.testing.assert_almost_equal(b,[0,0.3544116293114718,0])

        
class Test_wradObjThckPgn_resulting_fields_z(unittest.TestCase):
    #check effect of magnetisation being written in each of three dimensions
    def setUp(self):
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [0,0,1]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.a.wradMatAppl(self.material)
        
        self.a.wradSolve(0.001, 10000)
    
    def test_cube_Z_magnetisation(self):
        b = rd.Fld(self.a.radobj,'bxbybz',[0,0,6.0])
        self.assertAlmostEqual(b[2], 0.3544116293114718)
    
    def test_cube_Z_magnetisation1(self):
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
    
class Test_wradRotate_thickpolygon(unittest.TestCase):    
    #wradRotate. Testing for thick polygons being rotated
    def setUp(self):
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [0,0,1]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.a.wradMatAppl(self.material)
        
        #self.a.wradRotate([0,0,0], [1,0,0], np.pi)
        
        #self.a.wradSolve(0.001, 10000)
        
    def test_rotate_cube_Z_bfield1(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,i*6.0,0])
                np.testing.assert_almost_equal(b,[0,-0.3544116293114718,0])

    def test_rotate_cube_Z_bfield2(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,-0.3544116293114718])

                
    def test_rotate_cube_Z_bfield3(self):
        self.a.wradRotate([0,0,0], [1,0,0], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,i*6.0,0])
                np.testing.assert_almost_equal(b,[0,0.3544116293114718,0])
                
    def test_rotate_cube_Z_bfield4(self):
        self.a.wradRotate([0,0,0], [1,0,0], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
                
    def test_rotate_cube_Z_magnetisation1(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,-1.,0.])

    def test_rotate_cube_Z_magnetisation2(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,-1.])

    def test_rotate_cube_Z_magnetisation3(self):
        self.a.wradRotate([0,0,0], [1,0,0], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,1.,0.])
                
    def test_rotate_cube_Z_magnetisation4(self):
        self.a.wradRotate([0,0,0], [1,0,0], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])
    

    def test_wradRotate_thickpolygon_colour(self):
        #test the colour has rotated correctly
        a = 1
        
        assert a == 2, 'this test has not been written yet'
        
    
        
    
    
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_wradObjThckPgn_exists']
    unittest.main()
    
