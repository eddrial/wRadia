'''
Created on 3 Mar 2020

@author: oqb
'''
import unittest
import radia as rd
import wradia as wrd
import numpy as np
import copy
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
    
    def test_wradMatAppl_material_ksi(self):
        assert self.a.material.ksi == self.material.ksi
        
    def test_wradMatAppl_magnetisation(self):
        assert self.material.M == self.M
        
    
    def test_wradMatAppl_magnetisation_overwrite(self):
        assert self.material.M == self.a.magnetisation
        
class Test_wradObjDrwAtr(unittest.TestCase):
    #wradObjDrwAtr. Drawing Attributes and Testing
    def setUp(self):
        self.ksi = [.019, .06]
        self.M = [0,0,1.5]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
        self.a.wradMatAppl(self.material)
        
    def test_wradObjDrwAtr_set_default_colour(self):
        self.a.wradObjDrwAtr()
        
        np.testing.assert_equal(self.a.set_default_colour, True)
        
    def test_wradObjDrwAtr_default_colour(self):
        self.a.wradObjDrwAtr()
        
        np.testing.assert_equal(self.a.colour, [0.5, 0.5, 0.875])
        
    def test_wradObjDrwAtr_set_non_default_colour(self):
        self.a.wradObjDrwAtr(colour = [0.1,0.1,0.1])
        
        np.testing.assert_equal(self.a.set_default_colour, False)
        
    def test_wradObjDrwAtr_non_default_colour(self):
        self.a.wradObjDrwAtr(colour = [0.1,0.1,0.1])
        
        np.testing.assert_equal(self.a.colour, [0.1, 0.1, 0.1])
        
        
    def test_wradObjDrwAtr_default_line_thickness(self):
        self.a.wradObjDrwAtr()
        
        np.testing.assert_equal(self.a.linethickness, 2)
    
    def test_wradObjDrwAtr_non_default_line_thickness(self):
        self.a.wradObjDrwAtr(linethickness= 5)
        
        np.testing.assert_equal(self.a.linethickness, 5)
    
        
class Test_wradSolve(unittest.TestCase):
    

    def setUp(self):
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [0,0,1.5]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        self.a = wrd.wrad_obj.wradObjThckPgn(0, 5, [[0,10],[10,10],[10,0],[0,0]],'x',[1,2,3])
        self.a.wradMatAppl(self.material)
    
    
    def wradSolve_not_solved(self):
        assert hasattr(self, 'solved') == False, 'attribute set before solution solved'
    
    def test_wradSolve_solved(self):
        self.a.wradSolve(0.001, 1000)
        
        assert self.a.solved == 1, 'solver has not run'
        
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
        self.a.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        #self.a.wradRotate([0,0,0], [1,0,0], np.pi)
        
        #self.a.wradSolve(0.001, 10000)
        
    ##X Axis Rotation ##
    
    # BField #
        
    def test_rotate_cube_x_axis_Z_bfield1(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,i*6.0,0])
                np.testing.assert_almost_equal(b,[0,-0.3544116293114718,0])

    def test_rotate_cube_x_axis_Z_bfield2(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,-0.3544116293114718])
                
    def test_rotate_cube_x_axis_Z_bfield3(self):
        self.a.wradRotate([0,0,0], [1,0,0], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,i*6.0,0])
                np.testing.assert_almost_equal(b,[0,0.3544116293114718,0])
                
    def test_rotate_cube_x_axis_Z_bfield4(self):
        self.a.wradRotate([0,0,0], [1,0,0], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
                
                
    # Magnetisation #
    
    def test_rotate_cube_x_axis_Z_magnetisation1(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,-1.,0.])

    def test_rotate_cube_x_axis_Z_magnetisation2(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,-1.])

    def test_rotate_cube_x_axis_Z_magnetisation3(self):
        self.a.wradRotate([0,0,0], [1,0,0], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,1.,0.])
                
    def test_rotate_cube_x_axis_Z_magnetisation4(self):
        self.a.wradRotate([0,0,0], [1,0,0], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])
        
    # Colour #
    
    def test_rotate_cube_x_axis_Z_colour1(self):
        self.a.wradRotate([0,0,0], [1,0,0], np.pi/2.0)
        
        Mrotated = [0.,-1.,0.]
        loc_material = wrd.wrad_mat.wradMatLin(self.ksi,Mrotated)
        
        b = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        b.wradMatAppl(loc_material)
        b.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        np.testing.assert_almost_equal(self.a.colour, b.colour, 2, 'The Colour is Wrong') 
        
        
    
    ##Y Axis Rotation ##
    
    # BField #
    def test_rotate_cube_y_axis_Z_bfield1(self):
        self.a.wradRotate([0,0,0], [0,1,0], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[i*6.0,0,0])
                np.testing.assert_almost_equal(b,[0.3544116293114718,0,0])

    def test_rotate_cube_y_axis_Z_bfield2(self):
        self.a.wradRotate([0,0,0], [0,1,0], np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,-0.3544116293114718])
                
    def test_rotate_cube_y_axis_Z_bfield3(self):
        self.a.wradRotate([0,0,0], [0,1,0], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[i*6.0,0,0])
                np.testing.assert_almost_equal(b,[-0.3544116293114718,0,0])
                
    def test_rotate_cube_y_axis_Z_bfield4(self):
        self.a.wradRotate([0,0,0], [0,1,0], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
                
    # Magnetisation #
                
    def test_rotate_cube_y_axis_Z_magnetisation1(self):
        self.a.wradRotate([0,0,0], [0,1,0], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [1.,0.,0.])

    def test_rotate_cube_y_axis_Z_magnetisation2(self):
        self.a.wradRotate([0,0,0], [0,1,0], np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,-1.])

    def test_rotate_cube_y_axis_Z_magnetisation3(self):
        self.a.wradRotate([0,0,0], [0,1,0], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [-1.,0.,0.])
                
    def test_rotate_cube_y_axis_Z_magnetisation4(self):
        self.a.wradRotate([0,0,0], [0,1,0], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])
        
    ##Z Axis Rotation ##
    
    # BField #
        
    def test_rotate_cube_z_axis_Z_bfield1(self):
        self.a.wradRotate([0,0,0], [0,0,1], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])

    def test_rotate_cube_z_axis_Z_bfield2(self):
        self.a.wradRotate([0,0,0], [0,0,1], np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
                
    def test_rotate_cube_z_axis_Z_bfield3(self):
        self.a.wradRotate([0,0,0], [0,0,1], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
                
    def test_rotate_cube_z_axis_Z_bfield4(self):
        self.a.wradRotate([0,0,0], [0,0,1], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        for i in range(-1,2,2):
            with self.subTest(i = i):
                b = rd.Fld(self.a.radobj,'bxbybz',[0,0,i*6.0])
                np.testing.assert_almost_equal(b,[0,0,0.3544116293114718])
                
                
    # Magnetisation #
    
    def test_rotate_cube_z_axis_Z_magnetisation1(self):
        self.a.wradRotate([0,0,0], [0,0,1], np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])

    def test_rotate_cube_z_axis_Z_magnetisation2(self):
        self.a.wradRotate([0,0,0], [0,0,1], np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])

    def test_rotate_cube_z_axis_Z_magnetisation3(self):
        self.a.wradRotate([0,0,0], [0,0,1], 3*np.pi/2.0)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])
                
    def test_rotate_cube_z_axis_Z_magnetisation4(self):
        self.a.wradRotate([0,0,0], [0,0,1], 2*np.pi)
        self.a.wradSolve(0.001, 10000)
        np.testing.assert_almost_equal(self.a.magnetisation, [0.,0.,1.])

    def test_wradRotate_thickpolygon_colour(self):
        #test the colour has rotated correctly
        a = 2
        
        assert a == 2, 'this test has not been written yet'
        
class Test_wradReflect_thickpolygon(unittest.TestCase):    
    #wradRotate. Testing for thick polygons being rotated
    def setUp(self):
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [1,0,0]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        Mxp = [1,0,0]
        Mxn = [-1,0,0]
        Myp = [0,1,0]
        Myn = [0,-1,0]
        Mzp = [0,0,1]
        Mzn = [0,0,-1]
        
        materialxp = wrd.wrad_mat.wradMatLin(self.ksi,Mxp)
        materialxn = wrd.wrad_mat.wradMatLin(self.ksi,Mxn)
        materialyp = wrd.wrad_mat.wradMatLin(self.ksi,Myp)
        materialyn = wrd.wrad_mat.wradMatLin(self.ksi,Myn)
        materialzp = wrd.wrad_mat.wradMatLin(self.ksi,Mzp)
        materialzn = wrd.wrad_mat.wradMatLin(self.ksi,Mzn)
        
        self.blockxp = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockxp.wradMatAppl(materialxp)
        self.blockxp.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockxn = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockxn.wradMatAppl(materialxn)
        self.blockxn.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockyp = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockyp.wradMatAppl(materialyp)
        self.blockyp.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockyn = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockyn.wradMatAppl(materialyn)
        self.blockyn.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockzp = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockzp.wradMatAppl(materialzp)
        self.blockzp.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockzn = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockzn.wradMatAppl(materialzn)
        self.blockzn.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
    def test_reflect_cube_x_plane_X_magnetisation(self):
        
        self.blockxp.wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.blockxp.magnetisation, self.blockxn.magnetisation)
        
    def test_reflect_cube_y_plane_X_magnetisation(self):
        
        originalMagnetisation = self.blockxp.magnetisation
        self.blockxp.wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.blockxp.magnetisation, originalMagnetisation)
        
    def test_reflect_cube_z_plane_X_magnetisation(self):
        
        originalMagnetisation = self.blockxp.magnetisation
        self.blockxp.wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.blockxp.magnetisation, originalMagnetisation)
    
    
    def test_reflect_cube_x_plane_Y_magnetisation(self):
        
        originalMagnetisation = self.blockyp.magnetisation
        self.blockyp.wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.blockyp.magnetisation, originalMagnetisation)
        
    def test_reflect_cube_y_plane_Y_magnetisation(self):
        
        self.blockyp.wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.blockyp.magnetisation, self.blockyn.magnetisation)
        
    def test_reflect_cube_z_plane_Y_magnetisation(self):
        
        originalMagnetisation = self.blockyp.magnetisation
        self.blockyp.wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.blockyp.magnetisation, originalMagnetisation)
        
    
    def test_reflect_cube_x_plane_Z_magnetisation(self):
        
        originalMagnetisation = self.blockzp.magnetisation
        self.blockzp.wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.blockzp.magnetisation, originalMagnetisation)
        
    def test_reflect_cube_y_plane_Z_magnetisation(self):
        
        originalMagnetisation = self.blockzp.magnetisation
        self.blockzp.wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.blockzp.magnetisation, originalMagnetisation)
        
    def test_reflect_cube_z_plane_Z_magnetisation(self):
        
        self.blockzp.wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.blockzp.magnetisation, self.blockzn.magnetisation)
        
    def test_reflect_cube_x_plane_X_colour(self):
        
        self.blockxp.wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.blockxp.colour, self.blockxn.colour)
        
    def test_reflect_cube_y_plane_X_colour(self):
        
        originalcolour = self.blockxp.colour
        self.blockxp.wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.blockxp.colour, originalcolour)
        
    def test_reflect_cube_z_plane_X_colour(self):
        
        originalcolour = self.blockxp.colour
        self.blockxp.wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.blockxp.colour, originalcolour)
    
    
    def test_reflect_cube_x_plane_Y_colour(self):
        
        originalcolour = self.blockyp.colour
        self.blockyp.wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.blockyp.colour, originalcolour)
        
    def test_reflect_cube_y_plane_Y_colour(self):
        
        self.blockyp.wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.blockyp.colour, self.blockyn.colour)
        
    def test_reflect_cube_z_plane_Y_colour(self):
        
        originalcolour = self.blockyp.colour
        self.blockyp.wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.blockyp.colour, originalcolour)
        
    
    def test_reflect_cube_x_plane_Z_colour(self):
        
        originalcolour = self.blockzp.colour
        self.blockzp.wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.blockzp.colour, originalcolour)
        
    def test_reflect_cube_y_plane_Z_colour(self):
        
        originalcolour = self.blockzp.colour
        self.blockzp.wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.blockzp.colour, originalcolour)
        
    def test_reflect_cube_z_plane_Z_colour(self):
        
        self.blockzp.wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.blockzp.colour, self.blockzn.colour)

class Test_wradTranslate_thickpolygon(unittest.TestCase):
    #wradTranslate. Testing for vertices being correctly translated
    def setUp(self):
        rd.UtiDelAll()
        
        self.test_blockx = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[1,0,0])
        self.test_blocky = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'y',[1,0,0])
        self.test_blockz = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'z',[1,0,0])
        
        
    def test_vertex_motion_correct_x(self):
        testagainst = copy.deepcopy(self.test_blockx.vertices[:,0])
        self.test_blockx.wradTranslate([1,0,0])
        np.testing.assert_equal(self.test_blockx.vertices[:,0],1+testagainst)
        
    def test_vertex_motion_correct_y(self):
        testagainst = copy.deepcopy(self.test_blocky.vertices[:,0])
        self.test_blocky.wradTranslate([1,0,0])
        np.testing.assert_equal(self.test_blocky.vertices[:,0],1+testagainst)
        
    def test_vertex_motion_correct_z(self):
        testagainst = copy.deepcopy(self.test_blockz.vertices[:,0])
        self.test_blockz.wradTranslate([1,0,0])
        np.testing.assert_equal(self.test_blockz.vertices[:,0],1+testagainst)

class Test_wradFieldInvert_thickpolygon(unittest.TestCase):    
    #wradRotate. Testing for thick polygons being rotated
    def setUp(self):
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        self.M = [1,0,0]
        self.material = wrd.wrad_mat.wradMatLin(self.ksi,self.M)
        
        Mxp = [1,0,0]
        Mxn = [-1,0,0]
        Myp = [0,1,0]
        Myn = [0,-1,0]
        Mzp = [0,0,1]
        Mzn = [0,0,-1]
        
        materialxp = wrd.wrad_mat.wradMatLin(self.ksi,Mxp)
        materialxn = wrd.wrad_mat.wradMatLin(self.ksi,Mxn)
        materialyp = wrd.wrad_mat.wradMatLin(self.ksi,Myp)
        materialyn = wrd.wrad_mat.wradMatLin(self.ksi,Myn)
        materialzp = wrd.wrad_mat.wradMatLin(self.ksi,Mzp)
        materialzn = wrd.wrad_mat.wradMatLin(self.ksi,Mzn)
        
        self.blockxp = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockxp.wradMatAppl(materialxp)
        self.blockxp.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockxn = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockxn.wradMatAppl(materialxn)
        self.blockxn.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockyp = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockyp.wradMatAppl(materialyp)
        self.blockyp.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockyn = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockyn.wradMatAppl(materialyn)
        self.blockyn.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockzp = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockzp.wradMatAppl(materialzp)
        self.blockzp.wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        self.blockzn = wrd.wrad_obj.wradObjThckPgn(10, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
        self.blockzn.wradMatAppl(materialzn)
        self.blockzn.wradObjDrwAtr(colour = 'default', linethickness = 2)
                
    def test_field_invert_X_magnetisation(self):
        
        self.blockxp.wradFieldInvert()
        np.testing.assert_almost_equal(self.blockxp.magnetisation, self.blockxn.magnetisation)
        
    def test_field_invert_Y_magnetisation(self):
        
        self.blockyp.wradFieldInvert()
        np.testing.assert_almost_equal(self.blockyp.magnetisation, self.blockyn.magnetisation)
        
    def test_field_invert_Z_magnetisation(self):
        
        self.blockzp.wradFieldInvert()
        np.testing.assert_almost_equal(self.blockzp.magnetisation, self.blockzn.magnetisation)
        
        
    def test_field_invert_X_colour(self):
        
        self.blockxp.wradFieldInvert()
        np.testing.assert_almost_equal(self.blockxp.colour, self.blockxn.colour)
        
    def test_field_invert_Y_colour(self):
        
        self.blockyp.wradFieldInvert()
        np.testing.assert_almost_equal(self.blockyp.colour, self.blockyn.colour)
        
    def test_field_invert_Z_colour(self):
        
        self.blockzp.wradFieldInvert()
        np.testing.assert_almost_equal(self.blockzp.colour, self.blockzn.colour)
        
class Test_wradContainerBasics(unittest.TestCase):
    
    def setUp(self):
        rd.UtiDelAll()
        self.emptycontainer = wrd.wrad_obj.wradObjCnt([])
        
        self.basicblock = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[1,0,0])
    
    def test_object_list_present(self):
        np.testing.assert_equal(hasattr(self.emptycontainer, 'objectlist'),True)
        
    def test_default_object_list_empty(self):
        np.testing.assert_equal(len(self.emptycontainer.objectlist), 0)
        
    def test_adding_to_container(self):
        self.emptycontainer.wradObjAddToCnt([self.basicblock])
        
        np.testing.assert_equal(self.emptycontainer.objectlist, [self.basicblock])
        
    def test_subdivision(self):
        self.emptycontainer.wradObjDivMag([2,2,2])
        
        np.testing.assert_equal(self.emptycontainer.subdivision,[2,2,2])
        
    def test_default_subdivision(self):
        np.testing.assert_equal(hasattr(self.emptycontainer,'subdivision'),False)
    
class Test_wradRotate_container(unittest.TestCase):
    def setUp(self):
        
        #Test suite to see if reflecting a container of two thick polygons correctly reflects magnetisation vector, colour, and calls the correct Radia function
        # Need 4 blocks 
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        
        #defince an array of magnetisatins [x+, x-, y+, y-, z+, z-]
        self.magnetisations = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        
        #define array of materials to apply to the blocks
        self.materials = [[] for _ in range(6)]
        for i in range(6):
            self.materials[i] = wrd.wrad_mat.wradMatLin(self.ksi, self.magnetisations[i])
        #create an array of magnet blocks for manipulation
        self.test_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.test_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.test_blocks[i].wradMatAppl(self.materials[i])
            self.test_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2) 
        
        #create an array of magnet blocks as comparators
        self.comparator_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.comparator_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.comparator_blocks[i].wradMatAppl(self.materials[i])
            self.comparator_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        #create containers for X, Y Z blocks
        self.test_containers = [[] for _ in range(3)]
        for i in range(3):
            self.test_containers[i] = wrd.wrad_obj.wradObjCnt([self.test_blocks[2*i],self.test_blocks[2*i + 1]])
        
    def test_Rotate_container_no_colour(self):
        self.test_containers[0].wradRotate([0,0,0],[0,0,1],4)
        
        np.testing.assert_equal(hasattr(self.test_containers[0],'colour'),False)
        
class Test_wradReflect_container(unittest.TestCase):    
    #wradRotate. Testing for thick polygons being rotated
    def setUp(self):
        
        #Test suite to see if reflecting a container of two thick polygons correctly reflects magnetisation vector, colour, and calls the correct Radia function
        # Need 4 blocks 
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        
        #defince an array of magnetisatins [x+, x-, y+, y-, z+, z-]
        self.magnetisations = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        
        #define array of materials to apply to the blocks
        self.materials = [[] for _ in range(6)]
        for i in range(6):
            self.materials[i] = wrd.wrad_mat.wradMatLin(self.ksi, self.magnetisations[i])
        #create an array of magnet blocks for manipulation
        self.test_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.test_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.test_blocks[i].wradMatAppl(self.materials[i])
            self.test_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2) 
        
        #create an array of magnet blocks as comparators
        self.comparator_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.comparator_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.comparator_blocks[i].wradMatAppl(self.materials[i])
            self.comparator_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        #create containers for X, Y Z blocks
        self.test_containers = [[] for _ in range(3)]
        for i in range(3):
            self.test_containers[i] = wrd.wrad_obj.wradObjCnt([self.test_blocks[2*i],self.test_blocks[2*i + 1]])
        
        
    def test_reflect_container_x_plane_X_magnetisation(self):
        
        self.test_containers[0].wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].magnetisation, np.array(self.comparator_blocks[1].magnetisation))
        
    def test_reflect_container_y_plane_X_magnetisation(self):
        
        self.test_containers[0].wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].magnetisation, self.comparator_blocks[0].magnetisation)
        
    def test_reflect_container_z_plane_X_magnetisation(self):
        
        self.test_containers[0].wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].magnetisation, self.comparator_blocks[0].magnetisation)
    
    
    def test_reflect_container_x_plane_Y_magnetisation(self):
        
        self.test_containers[1].wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].magnetisation, self.comparator_blocks[2].magnetisation)
        
    def test_reflect_container_y_plane_Y_magnetisation(self):
        
        self.test_containers[1].wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].magnetisation, self.comparator_blocks[3].magnetisation)
        
    def test_reflect_container_z_plane_Y_magnetisation(self):
        
        self.test_containers[1].wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].magnetisation, self.comparator_blocks[2].magnetisation)
        
    
    def test_reflect_container_x_plane_Z_magnetisation(self):
        
        self.test_containers[2].wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].magnetisation, self.comparator_blocks[4].magnetisation)
        
    def test_reflect_container_y_plane_Z_magnetisation(self):
        
        self.test_containers[2].wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].magnetisation, self.comparator_blocks[4].magnetisation)
        
    def test_reflect_container_z_plane_Z_magnetisation(self):
        
        self.test_containers[2].wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].magnetisation, self.comparator_blocks[5].magnetisation)
        
    def test_reflect_container_x_plane_X_colour(self):
        
        self.test_containers[0].wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].colour, self.comparator_blocks[1].colour)
        
    def test_reflect_container_y_plane_X_colour(self):
        
        self.test_containers[0].wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].colour, self.comparator_blocks[0].colour)
        
    def test_reflect_container_z_plane_X_colour(self):
        
        self.test_containers[0].wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].colour, self.comparator_blocks[0].colour)
    
    
    def test_reflect_container_x_plane_Y_colour(self):
        
        self.test_containers[1].wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].colour, self.comparator_blocks[2].colour)
        
    def test_reflect_container_y_plane_Y_colour(self):
        
        self.test_containers[1].wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].colour, self.comparator_blocks[3].colour)
        
    def test_reflect_container_z_plane_Y_colour(self):
        
        self.test_containers[1].wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].colour, self.comparator_blocks[2].colour)
        
    
    def test_reflect_container_x_plane_Z_colour(self):
        
        self.test_containers[2].wradReflect([0,0,0], [1,0,0])
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].colour, self.comparator_blocks[4].colour)
        
    def test_reflect_container_y_plane_Z_colour(self):
        
        self.test_containers[2].wradReflect([0,0,0], [0,1,0])
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].colour, self.comparator_blocks[4].colour)
        
    def test_reflect_container_z_plane_Z_colour(self):
        
        self.test_containers[2].wradReflect([0,0,0], [0,0,1])
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].colour, self.comparator_blocks[5].colour)

class Test_wradTranslate_container(unittest.TestCase):
    #wradTranslate. Testing for vertices being correctly translated
    def setUp(self):
        
        #Test suite to see if reflecting a container of two thick polygons correctly reflects magnetisation vector, colour, and calls the correct Radia function
        # Need 4 blocks 
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        
        #defince an array of magnetisatins [x+, x-, y+, y-, z+, z-]
        self.magnetisations = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        
        #define array of materials to apply to the blocks
        self.materials = [[] for _ in range(6)]
        for i in range(6):
            self.materials[i] = wrd.wrad_mat.wradMatLin(self.ksi, self.magnetisations[i])
        #create an array of magnet blocks for manipulation
        self.test_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.test_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.test_blocks[i].wradMatAppl(self.materials[i])
            self.test_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2) 
        
        #create an array of magnet blocks as comparators
        self.comparator_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.comparator_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.comparator_blocks[i].wradMatAppl(self.materials[i])
            self.comparator_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        #create containers for X, Y Z blocks
        self.test_containers = [[] for _ in range(3)]
        for i in range(3):
            self.test_containers[i] = wrd.wrad_obj.wradObjCnt([self.test_blocks[2*i],self.test_blocks[2*i + 1]])
        
        


class Test_wradFieldInvert_container(unittest.TestCase):    
    #wradRotate. Testing for thick polygons being rotated
    def setUp(self):
        
        #Test suite to see if reflecting a container of two thick polygons correctly reflects magnetisation vector, colour, and calls the correct Radia function
        # Need 4 blocks 
        
        rd.UtiDelAll()
        self.ksi = [.019, .06]
        
        #defince an array of magnetisatins [x+, x-, y+, y-, z+, z-]
        magnetisations = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        
        #define array of materials to apply to the blocks
        materials = [[] for _ in range(6)]
        for i in range(6):
            materials[i] = wrd.wrad_mat.wradMatLin(self.ksi, magnetisations[i])
        #create an array of magnet blocks for manipulation
        self.test_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.test_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.test_blocks[i].wradMatAppl(materials[i]) 
            self.test_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        #create an array of magnet blocks as comparators
        self.comparator_blocks = [[] for _ in range(6)]
        for i in range(6):
            self.comparator_blocks[i] = wrd.wrad_obj.wradObjThckPgn(0, 10, [[-5,5],[5,5],[5,-5],[-5,-5]],'x',[0,0,0])
            self.comparator_blocks[i].wradMatAppl(materials[i]) 
            self.comparator_blocks[i].wradObjDrwAtr(colour = 'default', linethickness = 2)
        
        #create containers for X, Y Z blocks
        self.test_containers = [[] for _ in range(3)]
        for i in range(3):
            self.test_containers[i] = wrd.wrad_obj.wradObjCnt([self.test_blocks[2*i],self.test_blocks[2*i + 1]])
            #self.test_containers[i] = wrd.wrad_obj.wradObjCnt([self.test_blocks[2*i]])
        
        
        
            
    def test_field_invert_container_X_magnetisation(self):
        self.test_containers[0].wradFieldInvert()
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].magnetisation, self.comparator_blocks[1].magnetisation)
        
    def test_field_invert_container_Y_magnetisation(self):
        
        self.test_containers[1].wradFieldInvert()
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].magnetisation, self.comparator_blocks[3].magnetisation)
        
    def test_field_invert_container_Z_magnetisation(self):
        
        self.test_containers[2].objectlist[0].wradFieldInvert()
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].magnetisation, self.comparator_blocks[5].magnetisation)
        
        
    def test_field_invert_container_X_colour(self):
        self.test_containers[0].wradFieldInvert()
        np.testing.assert_almost_equal(self.test_containers[0].objectlist[0].colour, self.comparator_blocks[1].colour)
        
    def test_field_invert_container_Y_colour(self):
        
        self.test_containers[1].wradFieldInvert()
        np.testing.assert_almost_equal(self.test_containers[1].objectlist[0].colour, self.comparator_blocks[3].colour)
        
    def test_field_invert_container_Z_colour(self):
        
        self.test_containers[2].objectlist[0].wradFieldInvert()
        np.testing.assert_almost_equal(self.test_containers[2].objectlist[0].colour, self.comparator_blocks[5].colour)
      
    def test_field_invert_container_X_Bfield(self):
        self.test_containers[0].wradFieldInvert()
        self.test_containers[0].objectlist[0].wradSolve(0.001,1000)
        b = rd.Fld(self.test_containers[0].objectlist[0].radobj,'bxbybz',[6.0,0,0])
        print(b)
        self.assertLess(b[0], -0.01, 'field did not invert')
        
    def test_field_invert_container_Y_Bfield(self):
        
        self.test_containers[1].wradFieldInvert()
        self.test_containers[1].objectlist[0].wradSolve(0.001,1000)
        b = rd.Fld(self.test_containers[1].objectlist[0].radobj,'bxbybz',[0.0,6.0,0.0])
        print(b)
        self.assertLess(b[1], -0.01, 'field did not invert')
        
    def test_field_invert_container_Z_Bfield(self):
        
        self.test_containers[2].wradFieldInvert()
        self.test_containers[2].objectlist[0].wradSolve(0.001,1000)
        b = rd.Fld(self.test_containers[2].objectlist[0].radobj,'bxbybz',[0,0.0,6.0])
        print(b)
        self.assertLess(b[2], -0.01, 'field did not invert')
      
      


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_wradObjThckPgn_exists']
    unittest.main()
    
