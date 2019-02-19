# -*- coding: utf-8 -*-
import numpy as np  

class FeatureGenerator():
    def __init__(self):
        self.feature_blob=None
        self.__log_table=np.log1p(np.arange(256))        

    def Generate(self,vldpc):
        z=vldpc.valid_z
        rows=vldpc.rows
        cols=vldpc.cols
        grids=rows*cols
        intensity=vldpc.valid_intensity
        map_idx=vldpc.idx_row*cols+vldpc.idx_col
        uidx,counts=np.unique(map_idx,return_counts=True)
        max_height_data=np.zeros(grids)
        mean_height_data=np.zeros(grids)
        grid_count=np.zeros(grids)
        top_intensity_data=np.zeros(grids)
        mean_intensity_data=np.zeros(grids)
        none_empty=np.zeros(grids)
        for idx,count in zip(uidx,counts):
            max_height_data[idx]=np.max(z[idx==map_idx])
            mean_height_data[idx]=np.mean(z[idx==map_idx])
            top_intensity_data[idx]=np.max(intensity[idx==map_idx])/255
            mean_intensity_data[idx]=np.mean(intensity[idx==map_idx])/255
            grid_count[idx]=self.__LogCount(count.astype(np.int))
        none_empty[grid_count>0]=1
        grid_col,grid_row=np.meshgrid(range(cols),range(rows))
        center_x=self.Pix2Pc(grid_row,rows,vldpc.lrange)
        center_y=self.Pix2Pc(grid_col,cols,vldpc.lrange)
        direction_data=np.arctan2(center_y,center_x)/(2*np.pi) # Normalized
        distance_data=np.hypot(center_x,center_y)/60-0.5
        self.feature_blob=np.concatenate([max_height_data.reshape((1,1,rows,cols)),
                                      mean_height_data.reshape((1,1,rows,cols)),
                                      grid_count.reshape((1,1,rows,cols)),
                                      direction_data.reshape((1,1,rows,cols)),
                                      top_intensity_data.reshape((1,1,rows,cols)),
                                      mean_intensity_data.reshape((1,1,rows,cols)),
                                      distance_data.reshape((1,1,rows,cols)),
                                      none_empty.reshape((1,1,rows,cols))],axis=1)
        return self.feature_blob

    def __LogCount(self,count_data):
        if count_data<256:
            return self.__log_table[count_data]
        return np.log(1+count_data)

    @staticmethod
    def F2I(x,rows,lrange):
        return np.floor(rows*(lrange-x)/(2*lrange)).astype(np.int32)
    @staticmethod
    def Pix2Pc(in_pixel,in_size,out_range):
        res=2.0*out_range/in_size
        return out_range-(in_pixel+0.5)*res

if __name__=='__main__':
    import pointcloud as pc 
    import validpoint as vp
    tst=pc.PointCloud()
    tst.ReadFromPcdFile('/home/reme/桌面/CNNSeg/data/test.pcd')
    vldpc=vp.ValidPoints(tst,640,640,5,-5,60)
    vldpc.GetValid()
    fg=FeatureGenerator()
    fg.Generate(vldpc)
    pass