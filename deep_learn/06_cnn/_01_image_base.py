import matplotlib.pyplot as plt
import numpy as np


img1 = plt.imread("./data/img.png")
print(img1.shape) # (500, 507, 3)
plt.imshow(img1)
plt.show()


# rows = 10
# cols = 25
# total_pixels = rows * cols  # 总共 250 个像素点
# continuous_data = np.linspace(255, 0, total_pixels).astype(np.uint8)
#
# img = continuous_data.reshape(rows, cols)
#
# plt.imshow(img, vmin=0, vmax=255)
#
# plt.show()







