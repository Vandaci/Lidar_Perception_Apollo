# -*- coding:utf-8 -*-

import pcl.io as pio 
import numpy as np 

class PointCloud():
    def __init__(self):
        self.x=None
        self.y=None
        self.z=None
        self.intensity=None
        self.counts=None

    def ReadFromPcdFile(self,pcd_file_path):
        reader=pio.PCDReader()
        pcdata=reader.read(pcd_file_path)
        self.x=pcdata[0].data['x']
        self.y=pcdata[0].data['y']
        self.z=pcdata[0].data['z']
        self.intensity=pcdata[0].data['intensity']
        self.counts=self.x.size

    def ReadFromBinFile(self,bin_file_path):
        pc=np.fromfile(bin_file_path,dtype=np.float32)
        pc=pc.reshape((pc.size//4,4))
        self.x=pc[:,0]
        self.y=pc[:,1]
        self.z=pc[:,2]
        self.intensity=pc[:,3]
        self.counts=self.x.size        

    def findROIdata(self,xlimits,ylimits,zlimits):
        vldpc=PointCloud()
        idx=np.all([self.x>xlimits[0],self.x<=xlimits[1],
                    self.y>ylimits[0],self.y<=ylimits[1],
                    self.z>zlimits[0],self.z<=zlimits[1]],axis=0)
        vldpc.x=self.x[idx]
        vldpc.y=self.y[idx]
        vldpc.z=self.z[idx]
        vldpc.intensity=self.intensity[idx]
        vldpc.counts=vldpc.x.size
        return vldpc    

    def project2map(self,xlimits,ylimits,zlimits,rows,cols):
        vldpc=self.findROIdata(xlimits,ylimits,zlimits)
        vldpc.roi=np.vstack((xlimits,ylimits,zlimits))
        vldpc.maprow=self.F2I(vldpc.x,rows,xlimits[1])
        vldpc.mapcol=self.F2I(vldpc.y,cols,ylimits[1])
        return vldpc

    @staticmethod
    def F2I(x,rows,lrange):
        return np.floor(rows*(lrange-x)/(2*lrange)).astype(np.int32)


if __name__=="__main__":
    pc=PointCloud()
    pc.ReadFromBinFile('/home/reme/桌面/Lidar_Perception_Apollo/data/51.bin')
    roipc=pc.findROIdata([-60,60],[-60,60],[-5,5])
    vldpc=pc.project2map([-60,60],[-60,60],[-5,5],640,640)
    import sys 
    sys.path.append('/home/reme/桌面/Lidar_Perception_Apollo/src/Visualization')
    import visualize as vlz 
    import mayavi.mlab as mlab  
    vlz.display(vldpc)
    vlz.display(pc)
    mlab.show()
    pass