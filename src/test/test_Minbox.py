# -*- coding:utf-8 -*-

import minbox as mb
import matplotlib.pyplot as plt
import numpy as np
plt.ion()
x = np.random.uniform(10, 20, (35,))
y = np.random.uniform(20, 40, (35,))
points = np.hstack((x.reshape((35, 1)), y.reshape((35, 1))))
axes = plt.axes()
axes.plot(x, y, '.')
axes.set_xlim([0, 40])
axes.set_ylim([0, 40])

mbox = mb.MinBox(points)
for box in mbox.rec:
    vertices = box.vertices
    vertices = np.vstack((vertices, vertices[0, :]))
    axes.plot(vertices[:, 0], vertices[:, 1])
axes.axis('equal')
plt.show()
