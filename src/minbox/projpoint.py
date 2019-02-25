# -*- coding:utf-8 -*-

# 计算oa在ob上的投影,oa可以是多个点
import numpy as np


def projpoint(o, b, a):
    oa = a - o
    ob = b - o
    obunit = ob / (ob[0] * ob[0] + ob[1] * ob[1])
    op = np.dot(oa, ob.reshape((2, 1)))
    op = np.dot(op, obunit.reshape((1, 2)))
    pos = op + o
    height = np.abs(np.dot(oa, np.array([ob[1], -ob[0]]))) / np.sqrt(ob[0] * ob[0] + ob[1] * ob[1])
    return pos, height


'''
if __name__ == '__main__':
    a = np.array([[-4, 0.5], [1, 2]])
    b = np.array([1, 0])
    o = np.array([0, 0])
    pos, height = projpoint(o, b, a)
    print(pos, '\n', height)
    import matplotlib.pyplot as plt
    axes=plt.axes()
    axes.plot(np.array([o[0],b[0]]),np.array([o[1],b[1]]),'r-')
    axes.axis('equal')
    axes.plot(pos[:,0],pos[:,1],'b.')
    axes.plot(a[:,0],a[:,1],'.')
    plt.show()
'''
