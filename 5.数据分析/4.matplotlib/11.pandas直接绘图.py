import pandas as pd
import matplotlib.pyplot as plt

# 创建简单DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [4, 3, 2, 1]
}
)

# pandas内置plot方法，自动绘制折线
df.plot()

plt.show()