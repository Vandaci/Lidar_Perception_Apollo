# -*- coding:utf-8 -*-
"""
boundary : (m,n)  1 by 2
points  :  (m,2) m by 2
"""

import numpy as np
import projpoint as pj


class Rec:
    def __init__(self, points, boundary):
        self.vertices = None
        self.points_ = points
        self.boundary_ = boundary
        self.length = None
        self.width = None
        self.yaw = None
        self.area = None
        self.GetBox()

    def GetBox(self):
        # step 1 : 计算底边顶点
        o = self.points_[self.boundary_[0], :]
        b = self.points_[self.boundary_[1], :]
        ob = b - o
        vertices, height = pj.projpoint(o, b, self.points_)
        max_height_idx = height.argmax()
        K = ob[1] / ob[0]
        if 0 <= K or K < 0:
            v1 = vertices[vertices[:, 0].argmin(), :]
            v4 = vertices[vertices[:, 0].argmax(), :]
        else:
            v1 = vertices[vertices[:, 1].argmax(), :]
            v4 = vertices[vertices[:, 1].argmin(), :]
        # step2 : 计算另外两个顶点
        bo = v4 - v1
        ot1 = np.array([1, -bo[0] / bo[1]]) + v1
        v2, _ = pj.projpoint(v1, ot1, self.points_[max_height_idx, :])
        ot2 = np.array([1, -bo[0] / bo[1]]) + v4
        v3, _ = pj.projpoint(v4, ot2, self.points_[max_height_idx, :])
        self.vertices = np.vstack((v1, v2, v3, v4))
        self.width = height[max_height_idx]
        self.length = v4 - v1
        self.length = np.sqrt(self.length[0] * self.length[0] +
                              self.length[1] * self.length[1])
        if self.width > self.length:
            self.width, self.length = self.length, self.width
        self.yaw = np.arctan(K)
        self.area = self.length * self.width
        pass


if __name__ == '__main__':
    a = np.random.uniform(-2, 5, (6, 2))
    bound = [0, 1]
    aasd = Rec(a, bound)
    aasd.GetBox()
