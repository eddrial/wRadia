'''
Created on 10 Nov 2021

@author: oqb
'''
import radia as rd
import numpy as np
import copy
from wradia import wrad_mat as wrdm
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class wradPlot(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    #streamplotting
    def wradStreamPlot(self,corner1 = np.array([-10,0,-10]), corner2 = np.array([10,0,10]), fields = 'bxbz'):
        
        #region of V magnets
        Zv, Xv = np.mgrid[20:40:41j, -10:10:41j]
        Bxv = Xv.copy()
        Bzv = Zv.copy()
        
        for i in range(len(Xv)):
            for j in range(len(Zv)):
                #print ('coords are {}'.format([Xv[i,j],Zv[i,j]]))
                Bxv[i,j],Bzv[i,j] = rd.Fld(self.radobj,'bxbz',[Xv[i,j],0,Zv[i,j]]) 
                #print ('the field at those coords are Bx: {} Bz: {}'.format(Bxv[i,j],Bzv[i,j]))
        
        fig = plt.figure(figsize=(7, 9))
        gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 2])
        
        #  Varying density along a streamline
        ax0 = fig.add_subplot(gs[0, 0])
        ax0.streamplot(Xv, Zv, Bxv, Bzv, density=[0.5, 1])
        for i in range(2):
            for j in range(4,7,2):
                ax0.plot(self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                         self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
        ax0.set_title('Vertical Comp Magnets')
        
        ax0.set_aspect('equal')
        
        # Varying color along a streamline
        ax1 = fig.add_subplot(gs[0, 1])
        strm = ax1.streamplot(Xv, Zv, Bxv, Bzv, color=Bzv, linewidth=2, cmap='autumn')
        fig.colorbar(strm.lines)
        for i in range(2):
            for j in range(4,7,2):
                ax1.plot(self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                         self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
        ax1.set_title('Vertical Comp Magnets')
        
        #region of H magnets
        Zh, Xh = np.mgrid[-10:10:41j, 20:40:41j]
        BXh = Xh.copy()
        BZh = Zh.copy()
        
        for i in range(len(Xh)):
            for j in range(len(Zh)):
                #print ('coords are {}'.format([X[i,j],Y[i,j]]))
                BXh[i,j],BZh[i,j] = rd.Fld(self.radobj,'bxbz',[Xh[i,j],0,Zh[i,j]]) 
                #print ('the field at those coords are Bx: {} Bz: {}'.format(a,b))
        ax1.set_aspect('equal')
        
        #  Varying density along a streamline
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.streamplot(Xh, Zh, BXh, BZh, density=[0.5, 1])
        ax2.set_title('Horizontal Comp Magnets')
        
        for i in range(2):
            for j in range(7,12,4):
                ax2.plot(self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                         self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
        ax2.set_aspect('equal')
        
        # Varying color along a streamline
        ax3 = fig.add_subplot(gs[1, 1])
        strm = ax3.streamplot(Xh, Zh, BXh, BZh, color=BZh, linewidth=2, cmap='autumn')
        fig.colorbar(strm.lines)
        for i in range(2):
            for j in range(7,12,4):
                ax3.plot(self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                         self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
        ax3.set_title('Horizontal Comp Magnets')
        ax3.set_aspect('equal')
        
        #region of Functional magnets
        Zf, Xf = np.mgrid[-20:20:41j, -20:20:41j]
        BXf = Xf.copy()
        BZf = Zf.copy()
        
        for i in range(len(Xf)):
            for j in range(len(Zf)):
                #print ('coords are {}'.format([X[i,j],Y[i,j]]))
                BXf[i,j],BZf[i,j] = rd.Fld(self.radobj,'bxbz',[Xf[i,j],0,Zf[i,j]]) 
                #print ('the field at those coords are Bx: {} Bz: {}'.format(a,b))
        
        
        #  Varying density along a streamline
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.streamplot(Xf, Zf, BXf, BZf, density=[0.5, 1])
        ax4.set_title('Functional Magnets')
        for i in range(3):
            for j in range(4):
                ax4.plot(self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                         self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
        ax4.set_aspect('equal')
        
        # Varying color along a streamline
        ax5 = fig.add_subplot(gs[2, 1])
        strm = ax5.streamplot(Xf, Zf, BXf, BZf, color=BZf, linewidth=2, cmap='autumn')
        fig.colorbar(strm.lines)
        ax5.set_title('Functional Magnets')
        for i in range(3):
            for j in range(4):
                ax5.plot(self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,0],
                         self.objectlist[j].objectlist[0].objectlist[0].objectlist[i].vertices[:,2], color = 'k')
        ax5.set_aspect('equal')