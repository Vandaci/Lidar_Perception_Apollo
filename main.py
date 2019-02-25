# -*- coding:utf-8 -*-

import cnnsegmentation as csg
import visualize as vlz
import mayavi.mlab as mlab
import drawcuboid as drb
import minbox as mbox
import numpy as np

proto_Path = 'model/deploy.prototxt'
cnnseg_net_Path = 'model/deploy.caffemodel'
test_file_Path = 'data/67.bin'
cnnseg = csg.CNNSegmention()
cnnseg.forward(proto_Path, cnnseg_net_Path,
               test_file_Path, USE_CAFFE_GPU=False,
               readformat='bin')
ok = cnnseg.segment()
if ok:
    print('Congratulations! \nAll the tasks have been completed \nand will generate obstacle information for you!')
    print('Valid objects index:', cnnseg.cluster.valid_objects)
    J = 1
    for i in cnnseg.cluster.objects:
        print('%i' % J + ':' + i.type, ' score:%f' % i.score)
        J += 1
else:
    print('Failed! \n Please Check it')
pcdata = cnnseg.vldpc
obstacles = cnnseg.cluster.objects
vlz.display(pcdata)
for obs in obstacles:
    x = pcdata.x[obs.cloud]
    y = pcdata.y[obs.cloud]
    z = pcdata.z[obs.cloud]
    points = np.vstack((x, y))
    points = points.T
    box = mbox.MinBox(points)
    drb.drawfrom4points(box.min_box.vertices[:, 0],
                        box.min_box.vertices[:, 1], [np.min(z), np.max(z)], obs.type)
mlab.show()
