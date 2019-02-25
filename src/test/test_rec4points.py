# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import rec4points as r4p
import numpy as np

points = np.random.uniform(10, 20, (12, 2))
boundary = np.array([0, 1])
rec1 = r4p.Rec(points, boundary)
rec1.GetBox()
axes = plt.axes()
axes.plot(points[:, 0], points[:, 1], 'r.')
i = 0
for txt in points[0:2, :]:
    axes.text(txt[0], txt[1], str(i))
    i += 1
vertices = np.vstack((rec1.vertices, rec1.vertices[0, :]))
axes.plot(vertices[:, 0], vertices[:, 1])
axes.axis('equal')
plt.show()
