# -*- coding:utf-8 -*-

import sys
sys.path.append("/home/reme/桌面/Lidar_Perception_Apollo/src/Pointcloud")
import numpy as np
import pointcloud as pc

pcdata=pc.PointCloud()
pcdata.ReadFromPcdFile("/home/reme/桌面/Lidar_Perception_Apollo/data/test.pcd")
pcdata.ReadFromBinFile("/home/reme/桌面/Lidar_Perception_Apollo/data/51.bin")
pass