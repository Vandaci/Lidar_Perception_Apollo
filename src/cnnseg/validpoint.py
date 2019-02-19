# -*- coding:utf-8 -*-
import numpy as np 

class ValidPoints():
    def __init__(self,pcdata,rows,cols,
                 max_height,min_height,lrange):
        self.RawPoints=pcdata
        self.validindex=None
        self.valid_x=None
        self.valid_y=None
        self.valid_z=None
        self.valid_intensity=None
        self.rows=rows
        self.cols=cols
        self.max_height=max_height
        self.min_height=min_height
        self.lrange=lrange
        self.idx_col=None # 投射到map图中的列
        self.idx_row=None # 投射到map图中的行
        self.GetValid()

    def GetValid(self):
        idx_row=self.F2I(self.RawPoints.x,self.rows,self.lrange)
        idx_col=self.F2I(self.RawPoints.y,self.cols,self.lrange)
        valid_idx=np.all([idx_row>=0,idx_row<self.rows,
                          idx_col>=0,idx_col<self.cols,
                          self.RawPoints.z>=self.min_height,
                          self.RawPoints.z<=self.max_height],axis=0)
        self.valid_x=self.RawPoints.x[valid_idx]
        self.valid_y=self.RawPoints.y[valid_idx]
        self.valid_z=self.RawPoints.z[valid_idx]
        self.valid_intensity=self.RawPoints.intensity[valid_idx]
        self.validindex=np.where(valid_idx==True)[0]
        self.idx_row=idx_row[valid_idx]
        self.idx_col=idx_col[valid_idx]
        
    @staticmethod
    def F2I(x,rows,lrange):
        return np.floor(rows*(lrange-x)/(2*lrange)).astype(np.int32)

if __name__=='__main__':
    import pointcloud as pc 
    tst=pc.PointCloud()
    tst.ReadFromPcdFile('/home/reme/桌面/CNNSeg/data/test.pcd')
    vldpc=ValidPoints(tst,640,640,5,-5,60)
    pass