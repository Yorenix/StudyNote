# 基础准备

```
dir()  # 知道工具箱有哪些工具，进入某个工具箱
help()  # 获取每个工具的使用方法
```

#核心数据结构：张量 (Tensor)



#自动求导机制 (Autograd)



#数据加载与预处理 (Data I/O)

###Dataset

Dataset：PyTorch的数据抽象基类，需重写`__len__`和`__getitem__`。前者返回样本总数，后者按索引读取单个样本（如图片与标签）。它将原始数据封装为可索引的集合，解耦数据存储与读取逻辑，为后续批量加载提供统一接口。

```
from torch.utils.data import Dataset
from PIL import Image
import os

class MyData(Dataset):
    """
    自定义PyTorch数据集类，用于加载图像数据
    Dataset 是一个抽象基类，需要重写 __getitem__ 和 __len__ 方法
    用于将数据组织成PyTorch可以处理的格式
    """
    def __init__(self, root_dir, label_dir):
        """
        构造函数，初始化数据集
        Args:
            root_dir (str): 数据集根目录路径
            label_dir (str): 标签目录名称，同时也是类别名称
        """
        # 存储根目录和标签目录
        self.root_dir = root_dir
        self.label_dir = label_dir
        # 构建完整的图像目录路径
        self.path = os.path.join(self.root_dir, self.label_dir)
        # 获取该目录下所有图像文件的文件名列表
        self.img_path = os.listdir(self.path)
    def __getitem__(self, idx):
        """
        根据索引获取单个数据样本
        Args:
            idx (int): 数据样本的索引
        Returns:
            tuple: (图像对象, 标签字符串)
        """
        # 根据索引获取图像文件名
        img_name = self.img_path[idx]
        # 构建完整的图像文件路径
        img_item_path = os.path.join(self.root_dir, self.label_dir, img_name)
        # 使用PIL打开图像文件
        img = Image.open(img_item_path)
        # 标签就是目录名称（假设每个目录对应一个类别）
        label = self.label_dir
        # 返回图像和标签（注意：这里应该返回img和label）
        return img, label
    def __len__(self):
        """
        返回数据集中样本的总数量
        Returns:
            int: 数据集中图像文件的数量
        """
        return len(self.img_path)

root_dir = "dataset/train"
ants_label_dir = "ants"
bees_label_dir = "bees"
ants_dataset = MyData(root_dir, ants_label_dir)
bees_dataset = MyData(root_dir, bees_label_dir)
train_dataset = ants_dataset + bees_dataset
"""
train_dataset是一个数据集，train_dataset[0]返回的是第0个样本，返回的是一个元组(img对象,标签字符串）
，执行img, label = train_dataset[0]后，要显示图片使用img.show()方法，要显示标签使用print(label)方法
"""
```

### Dataloader

Dataloader:包装Dataset的批量调度器，支持分批、乱序、多进程并行加载。通过`batch_size`、`shuffle`、`num_workers`等参数控制数据流，输出可直接送入模型的张量批次。利用`pin_memory`和`collate_fn`优化传输与堆叠效率，是训练循环的数据引擎。

| 参数                      | 默认值  | 含义                                                         |
| ------------------------- | ------- | ------------------------------------------------------------ |
| `dataset`                 | (必需)  | 要从中加载数据的数据集对象，必须是 `Dataset` 或 `IterableDataset` 的实例。 |
| `batch_size`              | `1`     | 每个批次包含的样本数量。若指定了 `batch_sampler`，则此参数被忽略。 |
| `shuffle`                 | `False` | 是否在每个 epoch 开始时重新打乱数据。仅在 `sampler` 和 `batch_sampler` 均为 `None` 时有效。 |
| `sampler`                 | `None`  | 定义从数据集中抽取单个样本索引的策略 (Sampler)。与 `shuffle` 互斥，不能同时指定。 |
| `batch_sampler`           | `None`  | 类似 `sampler`，但每次返回一批索引列表。若指定此参数，则 `batch_size`、`shuffle`、`sampler`、`drop_last` 均被忽略。 |
| `num_workers`             | `0`     | 用于并行加载数据的子进程数量。`0` 表示在主进程中同步加载，大于 `0` 则开启多进程加载。 |
| `collate_fn`              | `None`  | 将多个独立样本合并成一个批次张量（或自定义结构）的函数。默认行为是沿第0维堆叠张量。 |
| `pin_memory`              | `False` | 是否在返回批次前将张量复制到锁页内存（pinned memory），用于加速 CPU 到 GPU 的数据传输。 |
| `drop_last`               | `False` | 当数据集总样本数不能被 `batch_size` 整除时，是否丢弃最后一个不完整的批次。 |
| `timeout`                 | `0`     | 从 worker 进程中收集批次数据的最大等待时间（秒）。`0` 表示无限等待；超时会引发异常。 |
| `worker_init_fn`          | `None`  | 每个 worker 进程启动时调用的函数，接收 worker id (`[0, num_workers-1]`) 作为参数。常用于设置随机种子或数据分片。 |
| `multiprocessing_context` | `None`  | 用于指定多进程启动方式（如 `'spawn'`、`'fork'`、`'forkserver'`）。默认由平台自动选择。 |
| `generator`               | `None`  | 用于控制采样器（如 `RandomSampler`）随机性的伪随机数生成器 (`torch.Generator`)，有助于结果复现。 |
| `prefetch_factor`         | `2`     | 每个 worker 提前加载的批次数。总预取批次数为 `num_workers * prefetch_factor`。适当增大可减少数据等待时间。 |
| `persistent_workers`      | `False` | 当 `num_workers > 0` 时，是否在数据集被遍历完一个 epoch 后保持 worker 进程存活，避免重复创建销毁进程的开销。 |
| `pin_memory_device`       | `""`    | 指定将数据锁定到哪个设备的锁页内存中，例如 `"cuda:0"`。用于多 GPU 场景下的精确控制（PyTorch 2.0+）。 |

```
# 导入必要的库和模块
import torchvision  # PyTorch视觉库，包含常用的数据集和图像变换
from torch.utils.data import DataLoader  # 数据加载器，用于批量加载数据
from torch.utils.tensorboard import SummaryWriter  # TensorBoard写入器，用于可视化

# 准备测试数据集
# 使用torchvision.datasets.CIFAR10加载CIFAR-10数据集
# root: 数据集存储路径
# train=False: 加载测试集（train=True加载训练集）
# transform: 数据预处理变换，将PIL图像转换为PyTorch张量
test_data = torchvision.datasets.CIFAR10(root='./4_dataset', train=False, transform=torchvision.transforms.ToTensor())

# 创建数据加载器（DataLoader）
# DataLoader负责将数据集分成批次，方便模型训练和评估
test_loader = DataLoader(
    dataset=test_data,        # 要加载的数据集对象
    batch_size=64,            # 每个批次包含的样本数量（类似抽牌数量）
    shuffle=True,             # 是否在每个epoch开始时打乱数据顺序（类似洗牌）
    num_workers=0,            # 用于数据加载的子进程数量（0表示使用主进程）
    drop_last=False           # 是否丢弃最后一个不完整的批次
)

# 测试数据集中第一张图片（注释掉的调试代码）
# img, target = test_data[0]  # 获取第一个样本（图像和标签）
# print(img.shape)           # 打印图像张量的形状
# print(test_data.classes[target])  # 打印对应的类别名称

# 创建TensorBoard写入器，用于记录和可视化数据
# "logs"是TensorBoard日志文件的存储目录
writer = SummaryWriter("logs")

# 初始化步数计数器，用于TensorBoard中的时间轴
step = 0

# 遍历数据加载器中的所有批次
# DataLoader会按批次返回数据，每个批次包含batch_size个样本
for data in test_loader:
    # 解包批次数据：imgs是图像批次，targets是标签批次
    imgs, targets = data
    
    # 将当前批次的图像添加到TensorBoard
    # "test_data": 图像在TensorBoard中的标签名称
    # imgs: 图像批次张量，形状为[batch_size, channels, height, width]
    # step: 当前步数，用于在TensorBoard时间轴上定位
    writer.add_images("test_data", imgs, step)
    
    # 步数加1，准备记录下一个批次
    step += 1

# 关闭TensorBoard写入器，确保所有数据都已写入磁盘
writer.close()
```



### Transforms

**作用**:图像预处理与数据增强（PIL/ndarray ↔ Tensor、缩放、裁剪、翻转、归一化等）

常见工具使用：ToTensor()、Normalize、Resize()、Compose()、RandomCrop()

```
from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter

img_path = "images/1.jpg"
img_PIL = Image.open(img_path).convert('RGB')  # 确保转换为RGB格式，避免RGBA通道问题.convert('RGB')  # 确保转换为RGB格式，避免RGBA通道问题
writer = SummaryWriter("logs")

#to_tensor
trans_totensor = transforms.ToTensor()
img_tensor = trans_totensor(img_PIL)
writer.add_image("ToTensor", img_tensor)

#normalize
#归一化计算公式``output[channel] = (input[channel] - mean[channel]) / std[channel]``,即每个通道的像素值减去该通道的均值，再除以该通道的标准差
print(img_tensor[0][318][985])
trans_norm = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
img_norm = trans_norm(img_tensor)
print(img_norm[0][318][985])
writer.add_image("Normalize", img_norm)

#resize
print(img_PIL.size)
trans_resize = transforms.Resize((512,512))
# img PIL -> resize -> img_resize PIL
img_resize = trans_resize(img_PIL)
print(img_resize.size)
# img_resize PIL -> totensor -> img_resize tensor
img_resize = trans_totensor(img_resize)
writer.add_image("Resize", img_resize,0)

# compose 用于将多个transform组合起来，实现对图片的多个操作
trans_resize_2 = transforms.Resize((512,512))
# 列表中的transform按顺序执行，第一个是将图片resize为512*512，第二个是将图片转换为tensor，注意参数顺序不能反，因为resize的参数是PIL而不是tensor
trans_compose = transforms.Compose([trans_resize_2, trans_totensor])
img_resize_2 = trans_compose(img_PIL)
writer.add_image("Resize", img_resize_2,1)

# RandomCrop
trans_random_crop = transforms.RandomCrop((256,512))
trans_compose_2 = transforms.Compose([trans_random_crop,trans_totensor])
for i in range(10):
    img_crop = trans_compose_2(img_PIL)
    writer.add_image("RandomCrop", img_crop,i)

writer.close()


```



 **常用变换**

| 类别     | 函数                      | 说明                                      |
| -------- | ------------------------- | ----------------------------------------- |
| 类型转换 | `ToTensor()`              | (H,W,C) → (C,H,W) FloatTensor，像素 [0,1] |
|          | `ToPILImage()`            | 反向操作                                  |
| 尺寸裁剪 | `Resize(size)`            | 调整大小                                  |
|          | `CenterCrop(size)`        | 中心裁剪                                  |
|          | `RandomCrop(size)`        | 随机裁剪                                  |
|          | `RandomResizedCrop(size)` | 随机缩放+裁剪                             |
| 翻转旋转 | `RandomHorizontalFlip(p)` | 随机水平翻转                              |
|          | `RandomRotation(deg)`     | 随机旋转                                  |
| 像素变换 | `Normalize(mean, std)`    | 减均值除标准差                            |
|          | `ColorJitter(...)`        | 亮度/对比度/饱和度/色相                   |
| 其他     | `Pad(padding)`            | 填充                                      |
|          | `GaussianBlur(kernel)`    | 高斯模糊                                  |

**组合管道**：`Compose`

```
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.RandomCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])
```

**自定义 Transform**

实现 `__call__` 的类：

```
class MyTransform:
    def __call__(self, img):
        # 处理逻辑
        return img
```

 **在 Dataset 中使用**

```
class MyDataset(Dataset):
    def __init__(self, transform=None):
        self.transform = transform
    def __getitem__(self, idx):
        img = load_image(idx)
        if self.transform:
            img = self.transform(img)
        return img, label
```

**训练/验证差异**

- **训练**：增强型（随机裁剪、翻转、颜色抖动等）
- **验证/测试**：确定型（Resize + CenterCrop + ToTensor + Normalize）

**常用归一化参数**

- **ImageNet**：`mean=[0.485,0.456,0.406]`, `std=[0.229,0.224,0.225]`
- **CIFAR-10**：`mean=[0.4914,0.4822,0.4465]`, `std=[0.2023,0.1994,0.2010]`
- **MNIST**（单通道）：`mean=[0.1307]`, `std=[0.3081]`

**注意点**

- `ToTensor()` 必须在 `Normalize()` 之前
- `transforms.v2`（PyTorch ≥2.0）支持更丰富的变换（边界框、掩码等）




###Torchvision

为什么需要 Torchvision？

PyTorch 核心库只负责张量计算与自动求导，对于计算机视觉任务中常见的**数据集读取、图像预处理、经典模型架构**并没有内置。`torchvision` 作为官方配套库，填补了这一空白。

它与 PyTorch 的关系可以理解为：**PyTorch 是引擎，Torchvision 是车载的导航、空调和座椅**——让视觉任务开发更顺畅。



**四大核心模块及其定位**

| 模块             | 解决什么问题                    | 典型使用场景                                 |
| ---------------- | ------------------------------- | -------------------------------------------- |
| **`datasets`**   | 我不想手动写下载和解析代码      | 快速获取 MNIST、CIFAR、ImageNet 等公开数据集 |
| **`transforms`** | 原始图片无法直接输入网络        | 将 PIL 图片转为 Tensor、归一化、数据增强     |
| **`models`**     | 我没有资源和时间从头训练大模型  | 直接使用 ImageNet 预训练的 ResNet、ViT 等    |
| **`utils`**      | 我想在 TensorBoard 里看图片效果 | 将多张图拼成网格、在图上画检测框             |

```python
import torchvision
from torch.utils.tensorboard import writer, SummaryWriter
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

# 定义Compose工具列表，第一个工具是转换为ToTensor类型
dataset_transforms = transforms.Compose([
    transforms.ToTensor()  # 需要括号来创建实例
])
# 下载好后不会重复下载
train_set = torchvision.datasets.CIFAR10(root='./4_dataset', train=True, transform=dataset_transforms ,download=True)
test_set = torchvision.datasets.CIFAR10(root='./4_dataset', train=False, transform=dataset_transforms , download=True)

# 测试数据集是否加载成功
# print(test_set[0]) # PIL.Image对象
# print(test_set.classes) # 类别标签列表
#
# img, target = test_set[0]
# img.show() # 显示图像
# print(test_set.classes[target]) # 类别标签字符串

write = SummaryWriter("logs")
for i in range(10):
    img, target = test_set[i]
    write.add_image("test_set", img, i)
write.close()
```


## 模型构建 

### Torch.nn

#### 核心基类 

`nn.Module`

- 层定义 (`__init__`)
- 前向传播逻辑 (`forward`)
- 参数管理 (`model.parameters()`, `named_children`)

#### **常用网络层**

##### 线性层

 `nn.Linear`

![77719188698](C:\Users\21467\AppData\Local\Temp\1777191886984.png)

![77719253222](C:\Users\21467\AppData\Local\Temp\1777192532224.png)

```
import torch
import torchvision
from torch import nn
from torch.nn import Linear
from torch.ao.nn.intrinsic import LinearReLU
from torch.nn import ReLU
from torch.utils.tensorboard import SummaryWriter

# 加载CIFAR10数据集，转换为Tensor格式
dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

# 创建数据加载器，批次大小为64
dataloader = torch.utils.data.DataLoader(dataset, batch_size=64)


class MyModel(nn.Module):
    def __init__(self):
        super(MyModel,self).__init__()
        self.linear1 = Linear(196608, 10)

    def forward(self, input):
        output = self.linear1(input)
        return output

model = MyModel()

for data in dataloader:
    imgs, targets = data
    print(imgs.shape)
    output = torch.flatten(imgs)
    print(output.shape)
    output = model(output)
    print(output.shape)

```





##### 卷积层

 `nn.Conv1d/2d/3d`

| 参数名     | 必需性 | 形状 / 类型要求                       | 默认值 | 说明                                                         |
| ---------- | ------ | ------------------------------------- | ------ | ------------------------------------------------------------ |
| `input`    | 必需   | 4D 张量`(N, C_in, H, W)`              | 无     | 输入特征图，N 为批次，C_in 为输入通道，H/W 为高宽。          |
| `weight`   | 必需   | 4D 张量`(C_out, C_in/groups, kH, kW)` | 无     | 卷积核权重，C_out 为输出通道，kH/kW 为核高宽。               |
| `bias`     | 可选   | 1D 张量`(C_out,)`                     | `None` | 每个输出通道的偏置项，`None` 时无偏置。                      |
| `stride`   | 可选   | `int` 或 `(sH, sW)` 元组              | `1`    | 卷积核滑动的步幅，控制输出尺寸缩减程度。                     |
| `padding`  | 可选   | `int` 或 `(padH, padW)` 元组          | `0`    | 在输入各边填充零值的数量，用于控制输出尺寸。                 |
| `dilation` | 可选   | `int` 或 `(dH, dW)` 元组              | `1`    | 空洞卷积的扩张率，增大感受野而不增加参数量。                 |
| `groups`   | 可选   | `int`                                 | `1`    | 将输入通道和输出通道分成若干组分别卷积，减少参数量。`groups=in_channels` 为深度可分离卷积。 |

![77711033632](C:\Users\21467\AppData\Local\Temp\1777110336324.png)

nn_convoulution

```
import torch
import torch.nn.functional as F

# 定义5x5输入矩阵
input = torch.tensor([[1, 2, 0, 3, 1],
                      [0, 1, 2, 3, 1],
                      [1, 2, 1, 0, 0],
                      [5, 2, 3, 1, 1],
                      [2, 1, 0, 1, 1]])

# 定义3x3卷积核
kernel = torch.tensor([[1, 2, 1],
                       [0, 1, 0],
                       [2, 1, 0]])

# 将2D张量reshape为4D格式: (batch_size, channels, height, width)
input = torch.reshape(input, (1, 1, 5, 5))  # 批次1, 通道1, 高5, 宽5
kernel = torch.reshape(kernel, (1, 1, 3, 3))  # 输出通道1, 输入通道1, 高3, 宽3

print("输入形状:", input.shape)
print("卷积核形状:", kernel.shape)

# 执行卷积操作: 输入, 卷积核, 步长=1
output = F.conv2d(input, kernel, stride=1)
print("卷积结果:")
print(output)
output = F.conv2d(input, kernel,stride=2)
print(output)
output = F.conv2d(input, kernel,stride=1,padding=1)
print(output)
```

nn_conv2d

```
import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

# 创建数据加载器，批次大小为64
dataloader = DataLoader(dataset,batch_size=64)

# 定义自定义神经网络模型
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel,self).__init__()
        # 定义卷积层：输入通道3，输出通道6，卷积核3x3
        self.conv1 = nn.Conv2d(3,6,3,stride=1,padding=0)

    def forward(self,x):
        # 前向传播：应用卷积操作
        x = self.conv1(x)
        return x

# 创建模型实例
Model = MyModel()

# 创建TensorBoard写入器，用于可视化
writer = SummaryWriter("logs")
step = 0

# 遍历数据集进行训练/测试
for data in dataloader:
    imgs, targets = data  # 获取图像和标签
    output = Model(imgs)  # 模型推理
    print(imgs.shape)  # 打印输入形状
    print(output.shape)  # 打印输出形状
    
    # 将输入图像写入TensorBoard
    writer.add_images("input",imgs,step)
    
    # 重塑输出以适应TensorBoard显示（6通道->3通道）
    output = torch.reshape(output,(-1,3,30,30))
    
    # 将输出图像写入TensorBoard
    writer.add_images("output",output,step)
    step += 1  # 步数递增
```







##### 归一化层 

`nn.BatchNorm`, `nn.LayerNorm`



##### 激活函数 

`nn.ReLU`, `nn.Sigmoid`, `nn.Softmax`

| 参数名    | 类型   | 默认值  | 含义                                                         |
| --------- | ------ | ------- | ------------------------------------------------------------ |
| `inplace` | `bool` | `False` | 若为 `True`，则直接对输入张量进行修改，节省内存；为 `False` 时返回新的张量。 |

```
import torch
import torchvision
from torch import nn
from torch.nn import ReLU
from torch.utils.tensorboard import SummaryWriter

# 测试Sigmoid激活函数：将输入压缩到(0,1)范围
test_input = torch.tensor([[1, -0.5],
                           [-1, 3]])

# 将2D张量reshape为4D格式: (batch_size, channels, height, width)
test_input = torch.reshape(test_input, (-1, 1, 2, 2))
print("测试输入形状:", test_input.shape)

# 加载CIFAR10数据集，转换为Tensor格式
dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

# 创建数据加载器，批次大小为64
dataloader = torch.utils.data.DataLoader(dataset, batch_size=64)

# 定义只包含Sigmoid激活函数的神经网络模型
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel,self).__init__()
        self.sigmoid1 = nn.Sigmoid()  # Sigmoid激活函数：f(x)=1/(1+e^(-x))
        # self.ReLU1 = ReLU() # 法二

    def forward(self, input):
        # 前向传播：应用Sigmoid激活函数
        output = self.sigmoid1(input)  # 将输入压缩到(0,1)范围
        return output

# 创建模型实例
model = MyModel()

# 创建TensorBoard写入器，用于可视化
writer = SummaryWriter("logs")
step=0

# 遍历数据集进行Sigmoid激活函数测试
for data in dataloader:
    imgs, targets = data  # 获取图像和标签
    writer.add_images("input", imgs, step)  # 记录原始输入图像
    outputs = model(imgs)  # 模型推理（应用Sigmoid激活）
    writer.add_images("output", outputs, step)  # 记录激活后图像
    step+=1  # 步数递增

writer.close()  # 关闭TensorBoard写入器
```





##### 池化层

 `nn.MaxPool2d`, `nn.AdaptiveAvgPool2d`

![77717288396](C:\Users\21467\AppData\Local\Temp\1777172883965.png)

| 参数名           | 类型                       | 默认值         | 含义                                                         |
| ---------------- | -------------------------- | -------------- | ------------------------------------------------------------ |
| `kernel_size`    | `int` 或 `(int, int)` 元组 | 无（必须提供） | 最大池化的窗口尺寸。单个整数表示高宽相同，元组分别指定 (高, 宽)。 |
| `stride`         | `int` 或 `(int, int)` 元组 | `kernel_size`  | 窗口滑动的步幅。默认与 `kernel_size` 相同，即无重叠池化。    |
| `padding`        | `int` 或 `(int, int)` 元组 | `0`            | 在输入各边填充零值的数量。可增加边缘信息参与池化的机会。     |
| `dilation`       | `int` 或 `(int, int)` 元组 | `1`            | 窗口中元素之间的间距（空洞池化），用于扩大感受野，通常保持为 1。 |
| `return_indices` | `bool`                     | `False`        | 若为 `True`，则返回最大值的位置索引，结合 `nn.MaxUnpool2d` 可实现上采样。 |
| `ceil_mode`      | `bool`                     | `False`        | 若为 `True`，输出尺寸计算使用向上取整 (ceil) 而非向下取整 (floor)，可能会保留更多的边缘信息。 |

```
# 导入必要的库
import torch
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# 注释掉的示例：手动定义5x5输入矩阵进行最大池化测试
# input = torch.tensor([[1, 2, 0, 3, 1],
#                       [0, 1, 2, 3, 1],
#                       [1, 2, 1, 0, 0],
#                       [5, 2, 3, 1, 1],
#                       [2, 1, 0, 1, 1]], dtype=torch.float32)
#
# input = torch.reshape(input, (-1, 1, 5, 5))

# 加载CIFAR10数据集，转换为Tensor格式
dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

# 创建数据加载器，批次大小为64
dataloader = DataLoader(dataset,batch_size=64)

# 定义包含最大池化层的神经网络模型
class MyModule(torch.nn.Module):
    def __init__(self):
        super(MyModule,self).__init__()
        # 定义最大池化层：3x3池化窗口，使用向上取整模式
        self.maxpool1 = torch.nn.MaxPool2d(kernel_size=3,ceil_mode=True)

    def forward(self,input):
        # 前向传播：应用最大池化操作
        output = self.maxpool1(input)
        return output

# 创建模型实例
Module = MyModule()

# 创建TensorBoard写入器，用于可视化
writer = SummaryWriter("logs")
step=0

# 遍历数据集进行最大池化操作
for data in dataloader:
    imgs, targets = data  # 获取图像和标签
    writer.add_images("input",imgs,step)  # 记录输入图像
    output = Module(imgs)  # 应用最大池化
    writer.add_images("output",output,step)  # 记录池化后图像
    step+=1  # 步数递增

writer.close()  # 关闭TensorBoard写入器
```







##### 循环层

`nn.RNN`, `nn.LSTM`, `nn.GRU`



##### 嵌入层

`nn.Embedding`



#### **模型容器**

- `nn.Sequential` (顺序结构)
- `nn.ModuleList` / `nn.ModuleDict` (动态结构)

#### **参数初始化策略**

- Xavier / Kaiming 初始化
- 自定义初始化权重函数

![77708024426](C:\Users\21467\AppData\Local\Temp\1777080244265.png)

```
import torch
# 导入神经网络模块，包含各种神经网络层和工具
from torch import nn

# 定义自定义神经网络模块类，继承自nn.Module基类
# 所有PyTorch神经网络模块都必须继承nn.Module
class MyModule(nn.Module):
    # 初始化方法，在创建模块实例时调用
    def __init__(self):
        # 调用父类nn.Module的初始化方法
        # 这是必须的步骤，用于正确初始化模块的基础结构
        super().__init__()

    # 前向传播方法，定义数据如何通过模块
    # 这是神经网络的核心计算逻辑
    def forward(self, input):
        # 简单的计算示例：将输入值加1
        # 在实际神经网络中，这里会包含复杂的层间计算
        output = input + 1
        # 返回计算结果
        return output

# 实例化后，M就是一个完整的神经网络模块
M = MyModule()

# 创建测试输入张量
# torch.tensor(1.0) 创建一个值为1.0的标量张量
x = torch.tensor(1.0)

# 使用模块处理输入数据
# M(x) 实际上调用了 M.forward(x)
# 这是PyTorch的语法糖，让模块可以像函数一样被调用
print(M(x))
```



#### 小实战：CIFAR10数据集

![77728237890](C:\Users\21467\AppData\Local\Temp\1777282378908.png)

![77728053309](C:\Users\21467\AppData\Local\Temp\1777280533099.png)

```
import torch
import torchvision
from networkx.generators.classic import kneser_graph
from torch import nn
from torch.utils.tensorboard import SummaryWriter

# 加载CIFAR10数据集，转换为Tensor格式
dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel,self).__init__()
        #               方法一：分别定义各个卷积、池化、展开、线性。。。
        # self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2, stride=1)
        # self.maxpool1 = nn.MaxPool2d(kernel_size=2)
        # self.conv2 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2, stride=1)
        # self.maxpool2 = nn.MaxPool2d(kernel_size=2)
        # self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2, stride=1)
        # self.maxpool3 = nn.MaxPool2d(kernel_size=2)
        # self.flatten = nn.Flatten()
        # self.linear1 = nn.Linear(in_features=1024, out_features=64)
        # self.linear2 = nn.Linear(in_features=64, out_features=10)
        #              方法二：使用Sequential
        self.model1 = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Flatten(),
                                    nn.Linear(in_features=1024, out_features=64),
                                    nn.Linear(in_features=64, out_features=10)
                                    )

    def forward(self, x):
        #      方法一
        # x = self.conv1(x)
        # x = self.maxpool1(x)
        # x = self.conv2(x)
        # x = self.maxpool2(x)
        # x = self.conv3(x)
        # x = self.maxpool3(x)
        # x = self.flatten(x)
        # x = self.linear1(x)
        # x = self.linear2(x)
        #      方法二
        return self.model1(x)
        return x

Model = MyModel()
print(Model)
# 测试
input = torch.ones(64,3,32,32)
output = Model(input)
print(output.shape)

writer = SummaryWriter("logs")
writer.add_graph(Model,input)
writer.close()

```





#损失函数与优化器

###**损失函数 (Loss Functions)**

- 分类：`CrossEntropyLoss`, `NLLLoss`, `BCEWithLogitsLoss`
- 回归：`MSELoss`, `L1Loss`, `SmoothL1Loss`

![77734430160](C:\Users\21467\AppData\Local\Temp\1777344301603.png)

```
import torch
from torch.nn import L1Loss, MSELoss

# 创建输入和目标张量
input = torch.tensor([1,2,3], dtype=torch.float)
target = torch.tensor([1,2,5], dtype=torch.float)

# 调整形状为(batch, channel, height, width)
input = torch.reshape(input,(1,1,1,3))
target = torch.reshape(target,(1,1,1,3))

# L1损失(绝对值损失)，reduction='sum'表示求和
loss = L1Loss(reduction='sum')
output = loss(input, target)
print(output)

# MSE损失(均方误差)，默认reduction='mean'
loss = MSELoss()
output = loss(input, target)
print(output)

```

![77736758259](C:\Users\21467\AppData\Local\Temp\1777367582598.png)

```
import torch
import torchvision.datasets
import torch.nn as nn

# 加载CIFAR10数据集，转换为Tensor格式
dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

dataloader = torch.utils.data.DataLoader(dataset,batch_size=25)

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel,self).__init__()
        self.model1 = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Flatten(),
                                    nn.Linear(in_features=1024, out_features=64),
                                    nn.Linear(in_features=64, out_features=10)
                                    )
    def forward(self, x):
        return self.model1(x)

model = MyModel()
loss = nn.CrossEntropyLoss()

for data in dataloader:
    imgs, targets = data
    outputs = model(imgs)
    result_loss = loss(outputs, targets)
    print(result_loss)
    # print(outputs)
    # print(targets)
    
```

###**优化器 (Optimizers)**

- 基础：`SGD`, `Adam`, `AdamW`, `RMSprop`
- 学习率策略 (`torch.optim.lr_scheduler`)
    - `StepLR`, `CosineAnnealingLR`, `ReduceLROnPlateau`


```
import torch
import torchvision.datasets
import torch.nn as nn

# 加载CIFAR10数据集，转换为Tensor格式
dataset = torchvision.datasets.CIFAR10(root='./4_dataset', train=False,transform=torchvision.transforms.ToTensor(),download=True)

dataloader = torch.utils.data.DataLoader(dataset,batch_size=3)

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel,self).__init__()
        self.model1 = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2, stride=1),
                                    nn.MaxPool2d(kernel_size=2),
                                    nn.Flatten(),
                                    nn.Linear(in_features=1024, out_features=64),
                                    nn.Linear(in_features=64, out_features=10)
                                    )
    def forward(self, x):
        return self.model1(x)

# 创建模型和损失函数
model = MyModel()
loss = nn.CrossEntropyLoss()

# 创建优化器（随机梯度下降），设置学习率为0.01
optim = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练20个epoch（完整遍历数据集20次）
for epoch in range(20):
    # 初始化当前epoch的累计损失
    runing_loss = 0.0
    
    # 遍历数据加载器中的所有批次
    for data in dataloader:
        # 解包批次数据：图像和对应的标签
        imgs, targets = data
        
        # 前向传播：模型对输入图像进行预测
        outputs = model(imgs)
        
        # 计算损失：比较模型输出与真实标签
        result_loss = loss(outputs, targets)
        
        # 梯度清零：清除上一批次的梯度，防止梯度累积
        optim.zero_grad()
        
        # 反向传播：计算损失相对于模型参数的梯度
        result_loss.backward()
        
        # 参数更新：根据梯度使用优化器更新模型权重
        optim.step()
        
        # 累计损失：将当前批次的损失加到总损失中
        runing_loss+=result_loss
    
    # 打印当前epoch的总损失
    print(runing_loss)
```





#标准训练流程 (Train Loop)

### 标准CPU训练

```model.py
# *******************************模型定义
import torch
from torch import nn

class Mymodel(nn.Module):
    def __init__(self):
        super(Mymodel,self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3,32,kernel_size=5,stride=1,padding=2),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(32,32,kernel_size=5,stride=1,padding=2),
            nn.MaxPool2d(2),
            nn.Conv2d(32,64,kernel_size=5,stride=1,padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64*4*4,64),
            nn.Linear(64,10)
        )

    def forward(self,x):
        return self.model(x)

if __name__ == '__main__':
    mymodel = Mymodel()
    input = torch.ones(64,3,32,32)
    output = mymodel(input)
    print(output.shape)
```

```train.py
# *******************************利用CPU进行模型训练
import torch.optim
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from model import *

#加载数据集
train_data = torchvision.datasets.CIFAR10(root='./4_dataset', train=True,
                                          transform=torchvision.transforms.ToTensor(),download=True)
test_data = torchvision.datasets.CIFAR10(root="./4_dataset", train=False,
                                         transform=torchvision.transforms.ToTensor(),download=True)

#获取数据集长度
train_data_size = len(train_data)
test_data_size = len(test_data)
# print(train_data_size)
# print(test_data_size)

#使用dataloader数据采集器
train_dataloader = DataLoader(dataset=train_data,batch_size=64)
test_dataloader = DataLoader(dataset=test_data,batch_size=64)

#创建网络模型
mymodel = Mymodel()

#创建损失函数
loss_fn = nn.CrossEntropyLoss()

#定义优化器
learning_rate = 0.001
optimizer = torch.optim.SGD(mymodel.parameters(),lr=learning_rate)

#设置训练网络的一些参数
#记录训练的次数
total_train_step = 0
#记录测试的次数
total_test_step = 0
#训练的轮数
epochs = 10

#添加tensorboard
writer = SummaryWriter(log_dir='./logs')

# 训练循环：遍历每个训练轮次
for i in range(epochs):
    print("-----------第{}轮训练开始了-----------".format(i+1))
    
    # 训练步骤开始：遍历训练数据集
    for data in train_dataloader:
        # 获取批次数据：图片和对应的标签
        imgs, targets = data
        # 前向传播：将图片输入模型，获得预测输出
        outputs = mymodel(imgs)
        # 计算损失：使用损失函数比较预测输出与真实标签
        loss = loss_fn(outputs, targets)
        # 反向传播与优化：
        optimizer.zero_grad()  # 1. 清空上一轮的梯度（避免梯度累积）
        loss.backward()        # 2. 反向传播计算梯度
        optimizer.step()       # 3. 根据梯度更新模型参数
        # 记录训练次数
        total_train_step += 1
        # 打印训练进度（每步都打印，可改为定期打印）
        if total_train_step % 100 == 0:
            print("训练次数：{}，Loss：{}".format(total_train_step, loss.item()))
            writer.add_scalar('train_loss',loss.item(),total_train_step)

    #训练结束后用测试集测试，看模型训练是否达到预期
    #测试开始
    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs, targets = data
            outputs = mymodel(imgs)
            loss = loss_fn(outputs, targets)
            total_test_loss += loss.item()
            accuracy = (outputs.argmax(1) == targets).sum()
            total_accuracy += accuracy.item()
    print("整体测试的loss：{}".format(total_test_loss))
    print("整体测试集上的正确率：{}".format(total_accuracy/test_data_size))
    writer.add_scalar('test_loss',total_test_loss,total_test_step)
    writer.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step)
    total_test_step += 1

    #保存模型
    torch.save(mymodel, "mymodel_{}.pth".format(i))
    # torch.save(mymodel.state_dict(), "mymodel_{}.pth".format(i)) 官方推荐的保存方式
    print("模型已保存")

writer.close()

```

### 使用GPU训练-1

对网络模型、损失函数、输入数据（imgs、targets）做修改：    .cuda()

依次设置

* ```
  if torch.cuda.is_available():
      mymodel = mymodel.cuda()
  ```

* ```
  if torch.cuda.is_available():
      loss_fn = loss_fn.cuda()
  ```

*         if torch.cuda.is_available():
              imgs = imgs.cuda()
              targets = targets.cuda()

```
# *******************************利用GPU进行模型训练
import torch.optim
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from model import *

# 加载数据集
train_data = torchvision.datasets.CIFAR10(root='./4_dataset', train=True,
                                          transform=torchvision.transforms.ToTensor(), download=True)
test_data = torchvision.datasets.CIFAR10(root="./4_dataset", train=False,
                                         transform=torchvision.transforms.ToTensor(), download=True)

# 获取数据集长度
train_data_size = len(train_data)
test_data_size = len(test_data)
# print(train_data_size)
# print(test_data_size)

# 使用dataloader数据采集器
train_dataloader = DataLoader(dataset=train_data, batch_size=64)
test_dataloader = DataLoader(dataset=test_data, batch_size=64)

# 创建网络模型
mymodel = Mymodel()
# ***********************************************************************GPU训练
if torch.cuda.is_available():
    mymodel = mymodel.cuda()

# 创建损失函数
loss_fn = nn.CrossEntropyLoss()
# ***********************************************************************GPU训练
if torch.cuda.is_available():
    loss_fn = loss_fn.cuda()

# 定义优化器
learning_rate = 0.001
optimizer = torch.optim.SGD(mymodel.parameters(), lr=learning_rate)

# 设置训练网络的一些参数
# 记录训练的次数
total_train_step = 0
# 记录测试的次数
total_test_step = 0
# 训练的轮数
epochs = 10

# 添加tensorboard
writer = SummaryWriter(log_dir='./logs')

# 训练循环：遍历每个训练轮次
for i in range(epochs):
    print("-----------第{}轮训练开始了-----------".format(i + 1))

    # 训练步骤开始：遍历训练数据集
    for data in train_dataloader:
        # 获取批次数据：图片和对应的标签
        imgs, targets = data
        # ***********************************************************************GPU训练
        if torch.cuda.is_available():
            imgs = imgs.cuda()
            targets = targets.cuda()
        # 前向传播：将图片输入模型，获得预测输出
        outputs = mymodel(imgs)
        # 计算损失：使用损失函数比较预测输出与真实标签
        loss = loss_fn(outputs, targets)
        # 反向传播与优化：
        optimizer.zero_grad()  # 1. 清空上一轮的梯度（避免梯度累积）
        loss.backward()  # 2. 反向传播计算梯度
        optimizer.step()  # 3. 根据梯度更新模型参数
        # 记录训练次数
        total_train_step += 1
        # 打印训练进度（每步都打印，可改为定期打印）
        if total_train_step % 100 == 0:
            print("训练次数：{}，Loss：{}".format(total_train_step, loss.item()))
            writer.add_scalar('train_loss', loss.item(), total_train_step)

    # 训练结束后用测试集测试，看模型训练是否达到预期
    # 测试开始
    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs, targets = data
            # ***********************************************************************GPU训练
            if torch.cuda.is_available():
                imgs = imgs.cuda()
                targets = targets.cuda()
            outputs = mymodel(imgs)
            loss = loss_fn(outputs, targets)
            total_test_loss += loss.item()
            accuracy = (outputs.argmax(1) == targets).sum()
            total_accuracy += accuracy.item()
    print("整体测试的loss：{}".format(total_test_loss))
    print("整体测试集上的正确率：{}".format(total_accuracy / test_data_size))
    writer.add_scalar('test_loss', total_test_loss, total_test_step)
    writer.add_scalar('test_accuracy', total_accuracy / test_data_size, total_test_step)
    total_test_step += 1

    # 保存模型
    torch.save(mymodel, "mymodel_{}.pth".format(i))
    # torch.save(mymodel.state_dict(), "mymodel_{}.pth".format(i)) 官方推荐的保存方式
    print("模型已保存")

writer.close()

```

### 使用GPU训练-2

设置 device = torch.device("cpu")    或者 device = torch.device("cuda:0")

依次设置

* mymodel = mymodel.to(device)
* loss_fn = loss_fn.to(device)
* imgs = imgs.to(device)
* targets = targets.to(device)

```
import torch.optim
import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
import time
from model import *

# 加载数据集
train_data = torchvision.datasets.CIFAR10(root='./4_dataset', train=True,
                                          transform=torchvision.transforms.ToTensor(), download=True)
test_data = torchvision.datasets.CIFAR10(root="./4_dataset", train=False,
                                         transform=torchvision.transforms.ToTensor(), download=True)

# 定义训练的设备
device = torch.device("cpu")

# 获取数据集长度
train_data_size = len(train_data)
test_data_size = len(test_data)
# print(train_data_size)
# print(test_data_size)

# 使用dataloader数据采集器
train_dataloader = DataLoader(dataset=train_data, batch_size=64)
test_dataloader = DataLoader(dataset=test_data, batch_size=64)

# 创建网络模型
mymodel = Mymodel()
# ***********************************************************************GPU训练
mymodel = mymodel.to(device)

# 创建损失函数
loss_fn = nn.CrossEntropyLoss()
# ***********************************************************************GPU训练
loss_fn = loss_fn.to(device)

# 定义优化器
learning_rate = 0.001
optimizer = torch.optim.SGD(mymodel.parameters(), lr=learning_rate)

# 设置训练网络的一些参数
# 记录训练的次数
total_train_step = 0
# 记录测试的次数
total_test_step = 0
# 训练的轮数
epochs = 10

# 添加tensorboard
writer = SummaryWriter(log_dir='./logs')
start_time = time.time()
# 训练循环：遍历每个训练轮次
for i in range(epochs):
    print("-----------第{}轮训练开始了-----------".format(i + 1))

    # 训练步骤开始：遍历训练数据集
    for data in train_dataloader:
        # 获取批次数据：图片和对应的标签
        imgs, targets = data
        # ***********************************************************************GPU训练
        imgs = imgs.to(device)
        targets = targets.to(device)
        # 前向传播：将图片输入模型，获得预测输出
        outputs = mymodel(imgs)
        # 计算损失：使用损失函数比较预测输出与真实标签
        loss = loss_fn(outputs, targets)
        # 反向传播与优化：
        optimizer.zero_grad()  # 1. 清空上一轮的梯度（避免梯度累积）
        loss.backward()  # 2. 反向传播计算梯度
        optimizer.step()  # 3. 根据梯度更新模型参数
        # 记录训练次数
        total_train_step += 1
        # 打印训练进度（每步都打印，可改为定期打印）
        if total_train_step % 100 == 0:
            end_time = time.time()
            print("所用时间："+str(end_time-start_time))
            print("训练次数：{}，Loss：{}".format(total_train_step, loss.item()))
            writer.add_scalar('train_loss', loss.item(), total_train_step)

    # 训练结束后用测试集测试，看模型训练是否达到预期
    # 测试开始
    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs, targets = data
            # ***********************************************************************GPU训练
            imgs = imgs.to(device)
            targets = targets.to(device)
            outputs = mymodel(imgs)
            loss = loss_fn(outputs, targets)
            total_test_loss += loss.item()
            accuracy = (outputs.argmax(1) == targets).sum()
            total_accuracy += accuracy.item()
    print("整体测试的loss：{}".format(total_test_loss))
    print("整体测试集上的正确率：{}".format(total_accuracy / test_data_size))
    writer.add_scalar('test_loss', total_test_loss, total_test_step)
    writer.add_scalar('test_accuracy', total_accuracy / test_data_size, total_test_step)
    total_test_step += 1

    # 保存模型
    torch.save(mymodel, "mymodel_{}.pth".format(i))
    # torch.save(mymodel.state_dict(), "mymodel_{}.pth".format(i)) 官方推荐的保存方式
    print("模型已保存")

writer.close()

```









#现有网络模型的使用与修改

```
import torchvision
import torch
from torch import nn

# 不使用这个模型了，因为这个模型有一百多G
# train_data = torchvision.datasets.ImageNet(root="./5_data_image_net", train=True,
#                                        download=True,transform=torchvision.transforms.ToTensor())

# pretrained=False：
# 加载模型的架构，但不加载预训练权重,模型参数会被随机初始化,适用于从头开始训练模型
# pretrained=True：
# 加载模型的架构并加载预训练权重,权重是在大型数据集（如ImageNet）上预训练得到的,适用于迁移学习或微调
vgg16_false = torchvision.models.vgg16(pretrained=False)
vgg16_true = torchvision.models.vgg16(pretrained=True)
print(vgg16_true)

# 根据vgg16这个模型的输出分析，vgg16有1000个分类，我们在模型最后添加一个全连接层，输出10个分类结果
# vgg16_true.add_module("add_Linear", nn.Linear(1000, 10)) 添加到vgg16模型的一级模块中
vgg16_true.classifier.add_module("add_Linear", nn.Linear(1000, 10)) # 添加到vgg16的classifier模块中
print(vgg16_true)

print(vgg16_false)
vgg16_false.classifier[6] = nn.Linear(4096, 10) # 修改vgg16的classifier模块中第6个全连接层的输出维度为10
print(vgg16_false)
```







#模型保存、加载与可视化



### 模型保存，加载

```
import torchvision
import torch
from sympy import false

vgg16 = torchvision.models.vgg16(weights=None)

#保存方式一:保存模型结构+模型参数
torch.save(vgg16, "./18_vgg16_method1.pth")

#保存方式二：仅保存模型参数(官方推荐)
torch.save(vgg16.state_dict(), "./18_vgg16_method2.pth")
```

```
import torch
import torchvision

#加载方式一
model = torch.load("./18_vgg16_method1.pth", weights_only=False)
# print(model)

#加载方式二
vgg16 = torchvision.models.vgg16(pretrained=False)
vgg16.load_state_dict(torch.load("./18_vgg16_method2.pth",weights_only=False))
print(vgg16)

```





### TensorBoard

TensorBoard:TensorBoard 是专为深度学习打造的**可视化仪表板（Dashboard）**，它就像一个“仪表盘”，能将模型训练过程中各种抽象、难以理解的数据，转换成直观的图表和图像，帮助你实时、高效地监控和调试模型。

| 方法名            | 用途                                                       | 关键参数说明                                               |
| ----------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| **add_scalar**    | 记录**单个数值**（如 Loss、Accuracy）随训练步数的变化曲线  | `tag`(图表标题), `scalar_value`(数值), `global_step`(x轴)  |
| **add_scalars**   | 在同一张图中对比**多条曲线**（如训练/验证 Loss 同框）      | `main_tag`(主标题), `tag_scalar_dict`(字典{名称:值})       |
| **add_graph**     | 记录**模型计算图结构**，直观检查层连接是否正确             | `model`(模型实例), `input_to_model`(样例输入张量)          |
| **add_histogram** | 记录张量**数值分布直方图**（监控权重、梯度的分布变化）     | `tag`, `values`(张量), `global_step`                       |
| **add_image**     | 显示单张**图片数据**（如输入样本、生成结果、特征图）       | `tag`, `img_tensor`(CHW格式), `global_step`                |
| **add_images**    | 显示**多张图片**组成的网格（如一个 batch 的样本）          | `tag`, `img_tensor`(NCHW格式), `global_step`               |
| **add_embedding** | **高维向量降维可视化**（如词嵌入、特征向量的 PCA / t-SNE） | `mat`(向量矩阵), `metadata`(标签列表), `label_img`(缩略图) |
| **add_text**      | 记录**文本内容**（适用于 NLP 任务生成结果或调试信息）      | `tag`, `text_string`, `global_step`                        |
| **add_pr_curve**  | 绘制**二分类任务的精确率-召回率曲线**                      | `tag`, `labels`(真值), `predictions`(预测概率)             |
| **add_hparams**   | 记录**超参数与最终指标对照表**（便于多组实验对比）         | `hparam_dict`(超参数字典), `metric_dict`(最终指标字典)     |

```
🚀 启动与查看命令
在终端运行以下命令，然后浏览器打开 http://localhost:6006 即可查看：

bash
tensorboard --logdir=runs
```

```
from torch.utils.tensorboard import SummaryWriter
import numpy as np
from PIL import Image

writer = SummaryWriter("logs")
img_path = "2_data/train/ants_image/6240329_72c01e663e.jpg"
img_PIL = Image.open(img_path)
img_arr = np.array(img_PIL)

writer.add_image("test", img_arr, 2, dataformats='HWC')


for i in range(100):
    writer.add_scalar("y=x^3", i**3, i)


writer.close()

print("done")
```



# 完整的模型验证套路

```

```








#调试技巧与常见坑

使用   **google colab**   使用免费GPU

* ```
  #测试GPU是否可用
  import torch
  print(torch.cuda.is_available())
  ```

* 运行模型代码

  ```
  import torch
  import torch.optim
  import torchvision
  from torch import nn
  from torch.utils.data import DataLoader
  from torch.utils.tensorboard import SummaryWriter
  import time
  ```


  # 创建模型
  class Mymodel(nn.Module):
      def __init__(self):
          super(Mymodel, self).__init__()

          self.model = nn.Sequential(
    
              # 第一层
              nn.Conv2d(3, 32, kernel_size=5, padding=2),
              nn.ReLU(),
              nn.MaxPool2d(2),
    
              # 第二层
              nn.Conv2d(32, 64, kernel_size=5, padding=2),
              nn.ReLU(),
              nn.MaxPool2d(2),
    
              # 第三层
              nn.Conv2d(64, 64, kernel_size=5, padding=2),
              nn.ReLU(),
              nn.MaxPool2d(2),
    
              nn.Flatten(),
    
              # 全连接层
              nn.Linear(64 * 4 * 4, 512),
              nn.ReLU(),
    
              # 防止过拟合
              nn.Dropout(0.5),
    
              nn.Linear(512, 10)
          )
    
      def forward(self, x):
          return self.model(x)

  # 加载数据集
  # 加载数据集
  train_data = torchvision.datasets.CIFAR10(
      root='./4_dataset',
      train=True,
      transform=torchvision.transforms.ToTensor(),
      download=True
  )

  test_data = torchvision.datasets.CIFAR10(
      root="./4_dataset",
      train=False,
      transform=torchvision.transforms.ToTensor(),
      download=True
  )

  # GPU
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

  # 数据集长度
  train_data_size = len(train_data)
  test_data_size = len(test_data)

  print("训练集长度:", train_data_size)
  print("测试集长度:", test_data_size)

  # DataLoader
  train_dataloader = DataLoader(
      dataset=train_data,
      batch_size=64,
      shuffle=True   # 非常重要
  )

  test_dataloader = DataLoader(
      dataset=test_data,
      batch_size=64,
      shuffle=False
  )

  # 创建模型
  mymodel = Mymodel().to(device)

  # 损失函数
  loss_fn = nn.CrossEntropyLoss().to(device)

  # Adam优化器（比SGD更适合初学）
  learning_rate = 0.001

  optimizer = torch.optim.Adam(
      mymodel.parameters(),
      lr=learning_rate
  )

  # 训练参数
  total_train_step = 0
  total_test_step = 0
  epochs = 30

  # TensorBoard
  writer = SummaryWriter("./logs")

  start_time = time.time()

  # 开始训练
  for i in range(epochs):

      print("----------- 第{}轮训练开始 -----------".format(i + 1))
    
      # 训练模式
      mymodel.train()
    
      for data in train_dataloader:
    
          imgs, targets = data
    
          imgs = imgs.to(device)
          targets = targets.to(device)
    
          # 前向传播
          outputs = mymodel(imgs)
    
          # loss
          loss = loss_fn(outputs, targets)
    
          # 反向传播
          optimizer.zero_grad()
    
          loss.backward()
    
          optimizer.step()
    
          total_train_step += 1
    
          if total_train_step % 100 == 0:
    
              end_time = time.time()
    
              print("训练时间：{:.2f}".format(end_time - start_time))
    
              print("训练次数：{}，Loss：{:.4f}".format(
                  total_train_step,
                  loss.item()
              ))
    
              writer.add_scalar(
                  'train_loss',
                  loss.item(),
                  total_train_step
              )
    
      # ================= 测试 =================
      mymodel.eval()
    
      total_test_loss = 0
      total_accuracy = 0
    
      with torch.no_grad():
    
          for data in test_dataloader:
    
              imgs, targets = data
    
              imgs = imgs.to(device)
              targets = targets.to(device)
    
              outputs = mymodel(imgs)
    
              loss = loss_fn(outputs, targets)
    
              total_test_loss += loss.item()
    
              accuracy = (outputs.argmax(1) == targets).sum()
    
              total_accuracy += accuracy.item()
    
      print("整体测试Loss：{}".format(total_test_loss))
    
      print(
          "整体测试正确率：{:.2f}%".format(
              total_accuracy / test_data_size * 100
          )
      )
    
      writer.add_scalar(
          'test_loss',
          total_test_loss,
          total_test_step
      )
    
      writer.add_scalar(
          'test_accuracy',
          total_accuracy / test_data_size,
          total_test_step
      )
    
      total_test_step += 1
    
      # 保存模型
      torch.save(
          mymodel.state_dict(),
          "mymodel_{}.pth".format(i)
      )
    
      print("模型已保存")

  writer.close()
  ```

* 在文件夹中找到训练后保存好的模型

* 将该模型（XXXX.pth）保存到自己的项目中进行测试
  ```