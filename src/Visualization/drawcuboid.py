# -*- coding:utf-8 -*- 
import numpy as np 
import mayavi.mlab as mlab 

def drawfromcenter(center,len,wid,height,yaw,otype):
    # 计算中心与宽方向交点
    ground=center[2]-height/2
    A=np.array([center[0]+len/2*np.cos(yaw),
                center[1]+len/2*np.sin(yaw),ground])
    B=np.array([center[0]-len/2*np.cos(yaw),
                center[1]-len/2*np.sin(yaw),ground])
    A1=np.array([A[0]-wid/2*np.sin(yaw),
                 A[1]+wid/2*np.cos(yaw),ground]) 
    A2=np.array([A[0]+wid/2*np.sin(yaw),
                 A[1]-wid/2*np.cos(yaw),ground])
    B1=np.array([B[0]+wid/2*np.sin(yaw),
                 B[1]-wid/2*np.cos(yaw),ground])
    B2=np.array([B[0]-wid/2*np.sin(yaw),
                 B[1]+wid/2*np.cos(yaw),ground])
    rec4points=np.vstack((A1,A2,B1,B2))
    color_type={'vehicle':(1,0,0),'pedestrian':(0,1,0),
                'cyclist':(0,0,1),'dontCare':(1,1,0)}
    drawfromrec4points(rec4points,height,color_type[otype])

def drawfromrec4points(rec4points,h,clr):
    fig=mlab.gcf()
    x=np.hstack((rec4points[:,0],rec4points[0,0]))
    x=np.hstack((x,x))
    y=np.hstack((rec4points[:,1],rec4points[0,1]))
    y=np.hstack((y,y))
    z=np.hstack((rec4points[:,2],rec4points[0,2]))
    z=np.hstack((z,z+h))
    mlab.plot3d(x,y,z,figure=fig,tube_radius=None,color=clr)
    for idx in np.arange(1,4):
        xnew=np.vstack((x[idx],x[idx+5]))
        ynew=np.vstack((y[idx],y[idx+5]))
        znew=np.vstack((z[idx],z[idx+5]))
        mlab.plot3d(xnew,ynew,znew,figure=fig,tube_radius=None,color=clr)

def drawrec(rec4points):
    fig=mlab.gcf()
    rec4points=np.vstack((rec4points,rec4points[0,:]))
    mlab.plot3d(rec4points[:,0],rec4points[:,1],
                rec4points[:,2],tube_radius=None,figure=fig)

def drawfrom4points(x,y,height,clr):
    color_type={'Vehicle':(1,0,0),'Pedestrian':(0,1,0),
                'Bicycle':(0,0,1),'Unknown':(1,1,0)}
    fig=mlab.gcf()
    x=np.hstack((x,x[0]))
    x=np.hstack((x,x))
    y=np.hstack((y,y[0]))
    y=np.hstack((y,y))
    z=np.hstack((height[0]*np.ones((5,)),
                 height[1]*np.ones((5,))))
    mlab.plot3d(x,y,z,figure=fig,tube_radius=None,color=color_type[clr])
    for idx in np.arange(1,4):
        xnew=np.vstack((x[idx],x[idx+5]))
        ynew=np.vstack((y[idx],y[idx+5]))
        znew=np.vstack((z[idx],z[idx+5]))
        mlab.plot3d(xnew,ynew,znew,figure=fig,tube_radius=None,color=color_type[clr])



if __name__=='__main__':
    center=np.array([-10.4464406967,1.63741445541,-0.878034293652])
    len=4.91083
    wid=2.09113
    height=1.56142 
    yaw=0.7135195
    otype='vehicle'
    drawfromcenter(center,len,wid,height,yaw,otype)
    mlab.show()
