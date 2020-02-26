'''
Created on 17 Dec 2019

@author: oqb
'''

#import radia as rad
import numpy as np

class wradClaExtr():
    def __init__(self):
        self.a = 1

    '''def __init__(self, extrusioncentroid = 0, extrusionlength = 10, 
                 extrusionprofile = [[-5,-5],[-5,5],[5,5],[5,-5]],
                  Mvector = [0,0,0], Mcolour = [1,1,1], Morientation = 'x'):
    
        
        self.centroid = extrusioncentroid
        self.extrusionlength = extrusionlength
        self.extrusionprofile = extrusionprofile
        self.orientation = Morientation
        
        self.magvector = Mvector
        
        self.colour = Mcolour
        
        self.radiacontID = rad.ObjCnt([])
#        self.radiaID = rad.ObjThckPgn(self.centroid,self.extrusionlength,self.extrusionprofile,self.orientation,self.magvector)
        self.radiablockID = rad.ObjThckPgn(0,10,[[-5,-5],[5,-5],[5,5],[-5,5]])
        rad.ObjAddToCnt(self.radiacontID, self.radiablockID)
        
#        ObjThckPgn(x,lx,[[y1,z1],[y2,z2],...],a:'x',[mx,my,mz]:[0,0,0])
    
    
    def colourfromM(self):
        bmax = np.sqrt(self.magvector*self.magvector)
        self.colour = self.magvector/[2*max(bmax), 2*max(bmax), 2*max(bmax)]+[0.5,0.5,0.5]
        rad.ObjDrwAtr(self.radiablockID, self.colour)'''
    
    
    

'''if __name__ == '__main__':
    
    #make block
    #make block colour dependent on magnetisation
    #display block
    help(rad.ObjDrwOpenGL)
    magcentre = np.array([0,0,0])
    
    print(magcentre)
    
    magnetisation = np.array([4,-3,10])
    
    print(magnetisation)
    
    appleMainMagnet = wradClaExtr(extrusionprofile = [[-5,-5],[-5,5],[5,5],[5,-5]], Mvector=magnetisation) 
    appleMainMagnet.colourfromM()
    print(appleMainMagnet.colour)
    
    print(appleMainMagnet.radiacontID)
    print(appleMainMagnet.magvector)
    
    rad.ObjDrwOpenGL(appleMainMagnet.radiablockID)
    #uti_plot_show()
    
    a = 1
    
    print(a)'''
if __name__ == '__main__':
    cl = wradClaExtr()
    print (cl.a)
    
    
