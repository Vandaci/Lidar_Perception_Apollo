# -*- coding:utf-8 -*-
import numpy as np
from scipy.spatial import ConvexHull
import rec4points as r4p
# import matplotlib.pyplot as plt


class MinBox:
    def __init__(self, points):
        self.min_area_idx = None  # 面积最小矩形索引
        self.boundary = None  # 点集最外围点索引
        self.valid_bon = None  # 有效边索引
        # self.boundary_points = None
        self.rec = []  # 有效边构成的矩形列表，Rec类
        self.points = points
        self.min_box = None

        self.GetBoundary()   # 获取凸包
        self.GetValidBon()  # 获取有效边
        self.GetBox()  # 有效边构成的各个矩形
        self.GetMinBox()  # 获取最小矩形框

    def GetBoundary(self):
        hull = ConvexHull(self.points)
        self.boundary = hull.vertices

    def GetValidBon(self):
        bon_Points = self.points[self.boundary]  # 边界点
        # 先计算后排序
        min_point = bon_Points[0]
        max_point = bon_Points[0]
        max_point_idx = self.boundary[0]
        min_point_idx = self.boundary[0]
        for point, idx in zip(bon_Points, self.boundary):
            if max_point[0] * point[1] - point[0] * max_point[1] < 0:
                max_point = point
                max_point_idx = idx
            if min_point[0] * point[1] - point[0] * min_point[1] > 0:
                min_point = point
                min_point_idx = idx
        divide = max_point - min_point
        valid_value = np.dot(bon_Points - min_point, np.array([divide[1], -divide[0]]))
        self.valid_bon = self.boundary[valid_value >= 0]
        center_x = np.mean(self.points[:, 0])
        center_y = np.mean(self.points[:, 1])
        deg = np.arctan2(self.points[self.valid_bon, 1] - center_y,
                         self.points[self.valid_bon, 0] - center_x)
        idx = deg.argsort()[::-1]
        self.valid_bon = self.valid_bon[idx]
        max_idx = np.where(self.valid_bon == max_point_idx)[0][0]
        min_idx = np.where(self.valid_bon == min_point_idx)[0][0]
        # print(self.valid_bon)
        self.valid_bon = np.hstack((self.valid_bon[max_idx:], self.valid_bon[0:min_idx + 1]))
        # print(self.valid_bon)
        # 临时
        # self.minpoint = min_point
        # self.maxpoint = max_point
        # self.boundary_points = bon_Points

    def GetBox(self):
        for i in range(self.valid_bon.shape[0] - 1):
            bon_idx = np.array([self.valid_bon[i], self.valid_bon[i + 1]])
            rec = r4p.Rec(self.points, bon_idx)
            self.rec.append(rec)

    def GetMinBox(self):
        box_area = []
        for ar in self.rec:
            box_area.append(ar.area)
        self.min_area_idx = np.argmin(np.array(box_area))
        self.min_box = self.rec[self.min_area_idx]


# if __name__ == '__main__':
#     x = np.random.uniform(10, 20, (35,))
#     y = np.random.uniform(20, 40, (35,))
#     points = np.hstack((x.reshape((35, 1)), y.reshape((35, 1))))
#     axes = plt.axes()
#     axes.axis('equal')
#     axes.plot(x, y, '.')
#     plt.plot(0, 0, '*', markersize=10)
#     mbox = MinBox(points)
#     hull = np.vstack((mbox.boundary_points, mbox.boundary_points[0, :]))
#     plt.plot(hull[:, 0], hull[:, 1])
#     minmaxpoint = np.vstack((mbox.minpoint, mbox.maxpoint))
#     plt.plot(minmaxpoint[:, 0], minmaxpoint[:, 1], 'or')
#     plt.text(mbox.minpoint[0] + 1, mbox.minpoint[1] + 1, 'MinPoint')
#     plt.text(mbox.maxpoint[0] + 1, mbox.maxpoint[1] + 1, 'MaxPoint')
#     for i in mbox.boundary:
#         plt.text(mbox.points[i, 0], mbox.points[i, 1], str(i))
#     # for rec in mbox.rec:
#     #     vertices = np.vstack((rec.vertices, rec.vertices[0]))
#     #     plt.plot(vertices[:, 0], vertices[:, 1])
#     # pass
#     vertices=np.vstack((mbox.min_box.vertices,mbox.min_box.vertices[0]))
#     plt.plot(vertices[:, 0], vertices[:, 1])
#     plt.show()
