import matplotlib.pyplot as plt
import numpy as np
img = [[(1., 1., 1.), (0, 0, 0)], [(0, 0, 0), (0, 0, 0)]]
plt.ion()
for i in range(2):
    y = np.random.random([10,1])
    plt.imshow(img[i])
    plt.draw()
    plt.pause(1)
    plt.clf()