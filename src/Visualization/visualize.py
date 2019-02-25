# -*- coding:utf-8 -*- 

import mayavi.mlab as mlab
import pointcloud as pc


def display(pcdata):
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(900, 600))
    s = mlab.points3d(pcdata.x, pcdata.y, pcdata.z, pcdata.intensity,
                      figure=fig, mode='point', colormap='spectral')
    s.scene.show_axes = True
    return s


if __name__ == '__main__':
    pc_data = pc.PointCloud()
    pc_data.ReadFromBinFile('../../data/67.bin')
    display(pc_data)
    mlab.show()
