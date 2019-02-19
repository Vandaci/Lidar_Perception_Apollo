# -*- coding:utf-8 -*-
import numpy as np 

class Node():
    def __init__(self,rows,cols):
        self.node_rank=np.zeros((rows,cols),dtype=np.int)
        self.traversed=np.zeros((rows,cols),dtype=np.int)
        self.is_center=np.zeros((rows,cols),dtype=np.bool)
        self.is_object=np.zeros((rows,cols),dtype=np.bool)
        self.point_num=np.zeros((rows,cols),dtype=np.int)
        self.obstacle_id=-np.ones((rows,cols),dtype=np.int)
        self.parent=np.empty((2,rows,cols),dtype=np.int)
        self.center_node=np.empty((2,rows,cols),dtype=np.int)
        # MakeSet
        grid_col,grid_row=np.meshgrid(np.arange(cols),np.arange(rows))
        self.parent[0]=grid_row
        self.parent[1]=grid_col

if __name__=='__main__':
    nd=Node(640,640)
    pass