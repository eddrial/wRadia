'''
Created on 26 Feb 2020

@author: oqb
'''
import unittest
from wRadia import firstradia as wr


class Test(unittest.TestCase):


    def testsimple(self):
        cl = wr.wradClaExtr()
        assert cl.a == 1


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testsimpe']
    unittest.main()