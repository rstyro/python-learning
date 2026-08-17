import numpy as np
import matplotlib.pyplot as plt

# 设置画布大小(8,5)，分辨率dpi=100
plt.figure(figsize=(8, 5), dpi=100)

x = np.linspace(0,10,100)
plt.plot(x, np.sin(x))
plt.show()