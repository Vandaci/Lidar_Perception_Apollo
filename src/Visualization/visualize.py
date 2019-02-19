# -*- coding:utf-8 -*- 

from mayavi import mlab 

def display(pcdata):
    fig=mlab.figure(bgcolor=(0,0,0),size=(900,600))
    s=mlab.points3d(pcdata.x,pcdata.y,pcdata.z,pcdata.intensity,
                  figure=fig,mode='point',colormap='spectral')
    s.scene.show_axes=True
    return s 
