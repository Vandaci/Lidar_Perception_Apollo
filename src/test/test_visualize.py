import sys
sys.path.append("/home/reme/桌面/Lidar_Perception_Apollo/src/Visualization")
import visualize as vlz 
sys.path.append("/home/reme/桌面/Lidar_Perception_Apollo/src/Pointcloud")
import numpy as np
import pointcloud as pc
import mayavi.mlab as mlab
import drawcuboid as dc 

pcdata=pc.PointCloud()
pcdata.ReadFromBinFile("/home/reme/桌面/Lidar_Perception_Apollo/data/51.bin")
vlz.display(pcdata)

with open('/home/reme/桌面/Lidar_Perception_Apollo/data/002_00000051.bin.txt') as f:
    line=f.readline()
    while line:
        tdata=line.strip().split(" ")
        otype=tdata[0]
        center=list(map(float,tdata[1:4]))
        len=float(tdata[4])
        wid=float(tdata[5])
        height=float(tdata[6])
        yaw=float(tdata[7])
        dc.drawfromcenter(center,len,wid,height,yaw,otype)
        line=f.readline()
mlab.show()
