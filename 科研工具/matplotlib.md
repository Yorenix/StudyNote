# Matplotlib 知识点整理





## 1. 基础设置

### 导入库

python

```
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
```

### 解决中文乱码与负号显示

python

```
plt.rcParams["font.sans-serif"] = ["SimHei"]      # 使用黑体显示中文
plt.rcParams["axes.unicode_minus"] = False        # 正常显示负号
```

### 关闭警告（可选）

python

```
import warnings
warnings.filterwarnings("ignore")
```

### 在 Jupyter Notebook 中直接显示图形

python

```
%matplotlib inline
```

------

## 2. 基本绘图函数 `plt.plot()`

### 基本用法

python

```
plt.plot([1,2,3,4])                     # 默认 x 为索引
plt.plot([1,2,3,4], [1,4,9,16])         # 指定 x 和 y
plt.plot(x, y, "ro")                    # 使用格式字符串："颜色+标记"
```

### 常用格式字符

| 字符 | 颜色 | 字符 | 线型/标记 |
| ---- | ---- | ---- | --------- |
| 'b'  | 蓝色 | '-'  | 实线      |
| 'g'  | 绿色 | '--' | 虚线      |
| 'r'  | 红色 | ':'  | 点线      |
| 'c'  | 青色 | 'o'  | 圆点      |
| 'm'  | 品红 | 's'  | 正方形点  |
| 'y'  | 黄色 | '^'  | 上三角点  |
| 'k'  | 黑色 | '*'  | 星形点    |
| 'w'  | 白色 | '+'  | 加号点    |

### 设置坐标轴范围

python

```
plt.axis([xmin, xmax, ymin, ymax])
```

### 同时绘制多条曲线

python

```
plt.plot(t, t, "r--", t, t**2, "bs", t, t**3, "g^")
```

### 设置线条属性

python

```
# 方式一：在 plot 中指定
plt.plot(x, y, linewidth=4.0, color='r')

# 方式二：使用返回值
line, = plt.plot(x, y)
line.set_antialiased(False)

# 方式三：使用 plt.setp()
plt.setp(line, color='r', linewidth=4)
```

------

## 3. 子图

python

```
plt.figure(figsize=(10,6))          # 设置图形大小
plt.subplot(2,1,1)                  # 2行1列，第1个子图
plt.plot(t1, f(t1), "bo")
plt.subplot(2,1,2)                  # 第2个子图
plt.plot(t2, np.cos(2*np.pi*t2), "r--")
plt.show()
```

- `plt.subplot(numrows, numcols, fignum)`，当乘积小于10时可省略逗号，如 `plt.subplot(211)`。

------

## 4. 常见图表绘制

### 4.1 柱状图 (bar)

python

```
plt.bar(x, y, color="g")
plt.title("标题", fontsize=20)
plt.xlabel("X轴标签", fontsize=18)
plt.ylabel("Y轴标签", fontsize=18)
plt.tick_params(labelsize=14)
plt.xticks(rotation=90)              # 旋转X轴标签

# 在柱子上方显示数值
for a,b in zip(x, y):
    plt.text(a, b+10, b, ha="center", va="bottom", fontsize=10)
```

### 4.2 曲线图 (plot)

python

```
plt.plot(x, y, color='b')
plt.title("每年电影数量", fontsize=20)
plt.xlabel("年份", fontsize=18)
plt.ylabel("电影数量", fontsize=18)

# 添加注释（箭头）
plt.annotate("2012年达到最大值", xy=(2012, value), xytext=(2025,2100),
             arrowprops=dict(facecolor="black", edgecolor="red"))

# 添加纯文本
plt.text(1980, 1000, "电影数量开始快速增长")
```

### 4.3 饼图 (pie)

python

```
plt.pie(x, labels=labels, autopct="%.1f %%", colors="bygr", startangle=90)
# 返回值：patches, l_text, p_text
# 设置文字属性
for i in p_text:
    i.set_size(15)
    i.set_color('w')
plt.legend()
```

**常用参数：**

- `x`：比例数据（自动归一化）
- `labels`：外侧说明文字
- `autopct`：百分比格式，如 `"%.1f %%"`
- `explode`：扇区离中心距离
- `shadow`：是否阴影
- `startangle`：起始角度
- `radius`：半径

### 4.4 直方图 (hist)

python

```
plt.hist(df["评分"], bins=20, edgecolor='k', alpha=0.5)
```

**常用参数：**

- `bins`：柱数
- `normed`：是否归一化
- `facecolor` / `edgecolor`：填充色/边框色
- `alpha`：透明度
- `histtype`：类型（`'bar'`, `'barstacked'`, `'step'`, `'stepfilled'`）

**返回值：** `n, bins, patches`

### 4.5 散点图 (scatter)

python

```
plt.scatter(x, y, color='c', marker='p', label="评分")
plt.legend()
```

**常用标记（marker）：** `'.'` 点, `','` 像素, `'o'` 圆, `'v'` 倒三角, `'^'` 正三角, `'s'` 正方形, `'p'` 五边形, `'*'` 星形, `'+'` 加号, `'x'` X号, `'D'` 钻石等。

### 4.6 箱线图 (boxplot)

python

```
plt.boxplot(data, whis=2,
            flierprops={"marker":'o', "markerfacecolor":"r", "color":'k'},
            patch_artist=True,
            boxprops={"color":'k', "facecolor":"#66ccff"},
            vert=False)      # vert=False 水平显示
```

**常用参数：**

- `notch`：凹口形式
- `sym`：异常点形状
- `vert`：垂直/水平
- `whis`：须与四分位的距离（倍数）
- `positions`：箱线图位置
- `widths`：宽度
- `patch_artist`：是否填充箱体
- `showmeans`：是否显示均值
- `labels`：标签
- `boxprops`, `flierprops`, `medianprops`, `meanprops`, `capprops`, `whiskerprops`：各类属性设置。

**多组箱线图：**

python

```
plt.boxplot([data1, data2, data3], labels=["A", "B", "C"], vert=False)
```

### 4.7 双轴图 (twinx)

python

```
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.hist(x, bins=100, color='m')
ax1.set_ylabel("数量")

ax2 = ax1.twinx()
ax2.plot(bins, y, "b--")
ax2.set_ylabel("概率密度")
```

### 4.8 热力图 (heatmap) - 使用 seaborn

python

```
import seaborn as sns

corr = data.corr()                 # 计算相关系数矩阵
sns.heatmap(corr, vmax=1, vmin=0, annot=True,
            annot_kws={"size":13, "weight":"bold"},
            linewidths=0.05)
```

**常用参数：**

- `data`：矩阵数据（DataFrame 或数组）
- `vmin, vmax`：颜色取值范围
- `cmap`：颜色映射
- `center`：颜色中心值
- `annot`：是否显示数值
- `fmt`：数值格式
- `linewidths` / `linecolor`：间隔线宽度/颜色
- `cbar`：是否显示颜色条
- `square`：是否方形单元格
- `xticklabels, yticklabels`：标签控制

------

## 5. 图形定制技巧

### 5.1 标题、轴标签、图例

python

```
plt.title("标题", fontsize=20)
plt.xlabel("X轴", fontsize=18)
plt.ylabel("Y轴", fontsize=18)
plt.legend()
```

### 5.2 文本标注

python

```
plt.text(x, y, "文本内容", ha="center", va="bottom", fontsize=10)
```

- `ha`：水平对齐（`'center'`, `'left'`, `'right'`）
- `va`：垂直对齐（`'top'`, `'bottom'`, `'center'`）

### 5.3 网格线

python

```
plt.grid()      # 默认显示网格
```

### 5.4 设置图形大小

python

```
plt.figure(figsize=(10,6))
```

### 5.5 获取当前坐标系并设置背景

python

```
ax = plt.gca()
ax.patch.set_facecolor("gray")
ax.patch.set_alpha(0.3)
```

------

## 6. 特殊功能

### 6.1 数据离散化与频数统计

python

```
pd.cut(df["时长"], [0,60,90,110,1000]).value_counts()
```

### 6.2 正态分布拟合（与直方图叠加）

python

```
from scipy.stats import norm
y = norm.pdf(bins, mean, std)
ax2.plot(bins, y, "b--")
```

### 6.3 相关系数矩阵图（scatter_matrix）

python

```
pd.plotting.scatter_matrix(data[::100], diagonal="kde", color='k', alpha=0.3, figsize=(10,10))
```

- `diagonal`：对角线图类型，`'hist'` 直方图，`'kde'` 核密度估计。

------

## 7. 综合示例：电影数据分析

以下是从两个 notebook 中提取的典型绘图流程：

python

```
# 1. 柱状图：各国家/地区电影数量
data = df["产地"].value_counts()
plt.bar(data.index, data.values)
plt.xticks(rotation=90)

# 2. 曲线图：每年上映电影数量
data = df["年代"].value_counts().sort_index()
plt.plot(data.index, data.values)

# 3. 饼图：电影时长占比
bins = [0,60,90,110,1000]
labels = ['(0,60]', '(60,90]', '(90,110]', '(110,1000]']
counts = pd.cut(df["时长"], bins).value_counts()
plt.pie(counts, labels=labels, autopct="%.1f%%")

# 4. 直方图：评分分布
plt.hist(df["评分"], bins=20, edgecolor='k', alpha=0.5)

# 5. 散点图：时长 vs 评分
plt.scatter(df["时长"][::100], df["评分"][::100], alpha=0.5)

# 6. 箱线图：不同地区评分比较
data_list = [df[df.产地==c]["评分"] for c in ["中国大陆","日本","中国香港"]]
plt.boxplot(data_list, labels=["中国大陆","日本","中国香港"], vert=False)

# 7. 热力图：数值特征相关性
sns.heatmap(df[["投票人数","评分","时长"]].corr(), annot=True)
```

------

以上是对 `6.ipynb` 和 `7.ipynb` 中 Matplotlib 知识点的整理，涵盖了基础绘图、常用图表类型、图形定制以及高级应用（双轴图、热力图等）。可以根据实际需要灵活组合使用。