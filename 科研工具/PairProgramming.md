# 第一节 Getting Started（开始使用 LLM 进行结对编程）

> DeepLearning.AI - Pair Programming with a Large Language Model
> Lesson 1: Getting Started

---
## 代码框架
```python
"""
Gemini API 初始化与调用示例

功能：
1. 配置 Gemini API
2. 查看可用模型
3. 创建模型对象
4. 封装文本生成函数
"""

# =========================
# 1. 导入依赖
# =========================

import os

# Google Gemini SDK
import google.generativeai as genai

# 用于自定义 API Endpoint
from google.api_core import client_options as client_options_lib

# 课程提供的工具函数
# 用于读取 API Key
from utils import get_api_key


# =========================
# 2. 配置 Gemini API
# =========================

genai.configure(
    # API Key
    api_key=get_api_key(),

    # 使用 REST 接口
    transport="rest",

    # 自定义 API 地址
    # DeepLearning.AI 的课程环境会自动提供
    client_options=client_options_lib.ClientOptions(
        api_endpoint=os.getenv("GOOGLE_API_BASE")
    )
)


# =========================
# 3. 查看可用模型
# =========================

for model in genai.list_models():

    print(f"模型名称: {model.name}")

    print(f"模型描述: {model.description}")

    print(
        f"支持的方法: "
        f"{model.supported_generation_methods}"
    )

    print("-" * 50)


# 输出示例：
#
# 模型名称:
# models/gemini-1.5-flash
#
# 模型描述:
# Fast and efficient model...
#
# 支持的方法:
# ['generateContent']


# =========================
# 4. 创建模型对象
# =========================

model_flash = genai.GenerativeModel(
    model_name="gemini-3-flash-preview"
)

# 相当于：
#
# model = GPT(...)
#
# 后续所有请求都会发送给这个模型


# =========================
# 5. 封装调用函数
# =========================

def generate_text(
    prompt,
    model=model_flash,
    temperature=1.0
):
    """
    向 Gemini 发送 Prompt

    Parameters
    ----------
    prompt : str
        用户提示词

    model : GenerativeModel
        使用的模型

    temperature : float
        控制随机性

        0.0 -> 最稳定
        1.0 -> 默认
        2.0 -> 更有创造力

    Returns
    -------
    Gemini Response
    """

    response = model.generate_content(
        prompt,

        generation_config={
            "temperature": temperature
        }
    )

    return response


# =========================
# 6. 测试
# =========================

prompt = """
Explain binary search in simple terms.
"""

response = generate_text(
    prompt,
    temperature=0
)

print(response.text)
```
## 核心思想


课程提出新的工作方式：

```text
需求
↓
LLM
↓
讨论方案
↓
生成代码
↓
测试修改
↓
完成开发
```

因此：

```text
LLM
=
Pair Programmer（结对编程伙伴）
```

而不是：

```text
LLM
=
自动代码生成器
```

---

## 什么是 Pair Programming

传统结对编程：

```text
程序员A
+
程序员B
```

共同完成开发任务。

---

现在：

```text
程序员
+
LLM
```

共同完成开发任务。

---

LLM 可以帮助：

- 理解代码
- 解释代码
- 编写注释
- 编写文档
- 生成测试
- 调试错误
- 优化代码

---

## 第一个示例：解释代码

输入代码：

```python
for i in range(len(items)):
    print(items[i])
```

Prompt：

```text
Explain what this code does.
```

输出：

```text
This code iterates through the list
and prints every element.
```

---

### 作用

```text
读代码
↓
理解代码
```

---

## 第二个示例：生成注释

输入：

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Prompt：

```text
Add comments to this code.
```

输出：

```python
def factorial(n):
    # Base case
    if n <= 1:
        return 1

    # Recursive case
    return n * factorial(n - 1)
```

---

### 作用

```text
代码
↓
自动注释
```

---

## 第三个示例：生成文档

Prompt：

```text
Write documentation for this function.
```

输出：

```python
"""
Calculate factorial recursively.

Args:
    n (int)

Returns:
    int
"""
```

---

### 作用

```text
代码
↓
文档
```

---

## Prompt 设计原则

不要：

```text
Write code.
```

而要：

```text
Explain this code.

Add comments.

Write documentation.

Suggest improvements.
```

---

### 原因

课程强调：

```text
先理解
再生成
```

通常效果更好。

---

## Temperature 参数

课程使用：

```python
temperature = 0
```

---

### 作用

控制模型输出随机性。

---

### temperature = 0

```text
最稳定
最确定
最容易复现
```

适用于：

- 编程
- 调试
- 文档生成
- 代码解释

---

### temperature > 0

```text
创造性更强
结果变化更大
```

适用于：

- 创意写作
- 文案生成
- 故事创作

---

## 编程场景推荐

```python
temperature = 0
```

原因：

```text
希望获得稳定答案
而不是随机答案
```

---

## 使用 LLM 的正确方式

错误方式：

```text
帮我写完整项目
```

---

正确方式：

```text
解释代码

↓

理解代码

↓

补充代码

↓

生成测试

↓

优化代码
```

---

## 本章重点

### Pair Programming

```text
程序员
+
LLM
```

共同完成开发任务。

---

### LLM 能做什么

- Explain Code
- Add Comments
- Write Documentation
- Generate Tests
- Debug Errors
- Refactor Code

---

### Temperature

```text
0
↓
稳定

高
↓
随机
```

---

## 一句话总结

```text
Use the LLM as a programming partner,
not just a code generator.
```

把 LLM 当成编程搭档，而不仅仅是代码生成器。

# 第二节 Using a String Template（使用字符串模板）

> DeepLearning.AI - Pair Programming with a Large Language Model
> Lesson 2: Using a String Template

---

## 核心思想

在编程场景中：

```text
Prompt
≠
固定字符串
```

很多时候需要：

```text
需求
+
代码
+
错误信息
+
用户输入
```

动态组合 Prompt。

因此：

```text
String Template
=
可复用的 Prompt 模板
```

---

## 为什么使用模板

不要这样写：

```python
prompt = """
Explain this code:

def add(a,b):
    return a+b
"""
```

因为每次换代码都需要修改 Prompt。

---

更好的方式：

```python
prompt = f"""
Explain the following code:

{code}
"""
```

这样：

```text
Prompt 不变
代码可变
```

---

## Python 中的 f-string

课程使用：

```python
prompt = f"""
Explain the following code:

{code}
"""
```

其中：

```python
{code}
```

会被变量内容替换。

---

例如：

```python
code = """
def add(a,b):
    return a+b
"""
```

最终 Prompt：

```text
Explain the following code:

def add(a,b):
    return a+b
```

---

## Prompt 模板的结构

通常由两部分组成：

```text
固定指令
+
动态内容
```

---

例如：

```python
prompt = f"""
Explain the following code:

{code}
"""
```

固定部分：

```text
Explain the following code:
```

动态部分：

```python
{code}
```

---

## 示例：代码解释器

### 输入

```python
code = """
for i in range(10):
    print(i)
"""
```

---

### Prompt

```python
prompt = f"""
Explain the following code:

{code}
"""
```

---

### 输出

```text
This loop prints the numbers
from 0 to 9.
```

---

## 示例：生成代码注释

### Prompt

```python
prompt = f"""
Add comments to the following code:

{code}
"""
```

---

### 输出

```python
# Iterate through numbers
for i in range(10):
    print(i)
```

---

## 示例：生成文档

### Prompt

```python
prompt = f"""
Write documentation
for the following function:

{code}
"""
```

---

### 输出

```python
"""
Print numbers from 0 to 9.
"""
```

---

## 使用 Delimiters

课程延续了 Prompt Engineering 中的技巧：

```text
Delimiter（分隔符）
```

用于区分：

```text
指令
↓
代码
```

---

### 示例

```python
prompt = f"""
Explain the following code:

```python
{code}
```

```

---

### 优势

- 降低歧义
- 提高准确率
- 让模型明确代码边界

---

## 让模板更具体

不要：

```text
Explain this.
```

---

而要：

```text
Explain this code line by line.
```

---

或者：

```text
Analyze:

1. Purpose
2. Time Complexity
3. Space Complexity
```

---

### 原因

Prompt 越明确：

```text
输出越稳定
```

---

## 模板复用

定义一次：

```python
TEMPLATE = """
Explain the following code:

{code}
"""
```

---

以后：

```python
prompt = TEMPLATE.format(
    code=my_code
)
```

---

或者：

```python
prompt = f"""
Explain the following code:

{my_code}
"""
```

---

这样：

```text
一个模板
↓
处理任意代码
```

---

## 实际应用场景

### 代码解释

```text
代码
↓
解释
```

---

### 调试

```text
代码
+
报错
↓
分析问题
```

---

### 代码审查

```text
代码
↓
优化建议
```

---

### LeetCode 学习

```text
题解
↓
解释思路
```

---

## 常见模板

### 解释代码

```python
prompt = f"""
Explain the following code:

```python
{code}
```

```

---

### 添加注释

```python
prompt = f"""
Add detailed comments
to the following code:

```python
{code}
```

```

---

### 分析复杂度

```python
prompt = f"""
Analyze this solution.

Please provide:

1. Idea
2. Time Complexity
3. Space Complexity

```python
{code}
```

```

---

### 代码优化

```python
prompt = f"""
Suggest improvements
for the following code:

```python
{code}
```

```

---

## 本章重点

### String Template

```text
固定 Prompt
+
动态内容
```

---

### 核心价值

```text
复用 Prompt
提高开发效率
```

---

### 常见用途

- Explain Code
- Add Comments
- Generate Docs
- Debug Errors
- Analyze Complexity

---

## 一句话总结

```text
A string template allows you to reuse prompts by inserting dynamic content into a fixed instruction.
```

字符串模板让我们能够将动态内容插入固定 Prompt，从而实现 Prompt 的复用。


# 第三节 Pair Programming Scenarios（结对编程场景）

> DeepLearning.AI - Pair Programming with a Large Language Model  
> Lesson 3: Pair Programming Scenarios

---

## 核心思想

前两节学习了：

```text
Getting Started
↓
学会调用 LLM

Using a String Template
↓
学会构造 Prompt
```

本节回答的问题：

```text
什么时候使用 LLM？
```

课程通过多个实际案例展示：

```text
LLM
=
编程助手
```

可以贯穿整个开发流程。

---

## 软件开发流程

一个典型开发流程：

```text
需求分析
↓
设计方案
↓
编写代码
↓
调试代码
↓
测试代码
↓
优化代码
↓
编写文档
```

课程强调：

```text
LLM 可以参与每个环节
```

---

## 场景 1：学习陌生代码

### 问题

接手新项目时：

```text
代码很多
↓
难以理解
```

---

### Prompt

```text
Explain this code.

What is its purpose?

How does it work?
```

---

### LLM 能做什么

- 解释代码逻辑
- 说明函数作用
- 分析执行流程
- 解释关键变量

---

### 工作流

```text
代码
↓
LLM解释
↓
快速理解
```

---

## 场景 2：编写新功能

### 问题

知道需求

但不知道如何开始。

---

### Prompt

```text
Implement a Python function that...

Requirements:
...
```

---

### LLM 能做什么

- 生成代码框架
- 提供实现思路
- 推荐数据结构
- 推荐算法

---

### 工作流

```text
需求
↓
LLM生成初稿
↓
人工修改
```

---

## 场景 3：调试（Debugging）

课程重点场景之一。

---

### Prompt

```text
This code produces the following error:

<error message>

Please explain the cause
and suggest a fix.
```

---

### 输入

```text
代码
+
报错信息
```

---

### 输出

```text
错误原因
+
修复方案
```

---

### 工作流

```text
Bug
↓
LLM分析
↓
修复
```

---

## 场景 4：代码优化

### Prompt

```text
Review this code.

Suggest improvements for:

- readability
- performance
- maintainability
```

---

### LLM 能做什么

- 删除重复代码
- 拆分函数
- 优化变量命名
- 提升可读性

---

### 工作流

```text
现有代码
↓
LLM审查
↓
优化建议
```

---

## 场景 5：编写测试

课程强调：

```text
测试很重要
```

但开发者通常：

```text
懒得写测试
```

---

### Prompt

```text
Generate unit tests
for the following function.
```

---

### 输出

```python
def test_case_1():
    ...

def test_case_2():
    ...
```

---

### LLM 能做什么

- 生成测试用例
- 生成边界条件
- 发现遗漏情况

---

### 工作流

```text
函数
↓
LLM
↓
测试代码
```

---

## 场景 6：编写文档

### Prompt

```text
Write documentation
for this function.
```

---

### 输出

```python
"""
Description

Parameters
Returns
Examples
"""
```

---

### 应用

- API 文档
- README
- 函数说明

---

## 场景 7：代码转换

### 示例

```text
Python
↓
Java
```

---

### Prompt

```text
Convert this Python code
to Java.
```

---

### LLM 能做什么

- 跨语言迁移
- 学习新语言
- 快速原型开发

---

## 课程强调的重要原则

### 不要盲目信任 LLM

错误方式：

```text
让 AI 写代码
↓
直接提交
```

---

正确方式：

```text
AI生成
↓
人工审查
↓
测试验证
↓
使用
```

---

### LLM 是助手

不是：

```text
自动程序员
```

而是：

```text
编程搭档
```

---

## Pair Programming 工作模式

课程推荐：

```text
提出问题
↓
获得建议
↓
修改代码
↓
继续提问
↓
不断迭代
```

---

### 示例

```text
请解释代码
↓
请优化代码
↓
请生成测试
↓
请写文档
```

---

## 本章重点

### 常见使用场景

- 理解代码
- 编写功能
- 调试错误
- 优化代码
- 编写测试
- 编写文档
- 代码转换

---

### 正确使用方式

```text
LLM
+
开发者
=
协作开发
```

---

### 开发流程

```text
需求
↓
生成代码
↓
调试
↓
测试
↓
优化
↓
文档
```

LLM 可以参与整个流程。

---

## 一句话总结

```text
Use the LLM throughout the software development lifecycle, not just for generating code.
```

不要只让 LLM 写代码，而要让它参与整个软件开发生命周期。


# 第四节 Technical Debt（技术债务）

> DeepLearning.AI - Pair Programming with a Large Language Model
> Lesson 4: Technical Debt

---

## 核心思想

课程提出：

```text
写出能运行的代码
≠
写出高质量的代码
```

在开发过程中，为了快速完成需求，经常会出现：

```text
代码能跑
↓
但难以维护
```

这就是：

```text
Technical Debt
（技术债务）
```

---

## 什么是 Technical Debt

可以理解为：

```text
今天省下的开发时间
↓
未来需要偿还的维护成本
```

---

例如：

为了赶进度：

```python
if x == 1:
    ...
elif x == 2:
    ...
elif x == 3:
    ...
elif x == 4:
    ...
```

代码虽然能运行：

```text
✓ 能交付
```

但是：

```text
难扩展
难维护
难阅读
```

未来修改成本越来越高。

---

## 技术债务的表现

### 重复代码

```python
def process_a():
    ...

def process_b():
    ...
```

大量逻辑重复。

---

### 命名不清晰

```python
a = 0
b = []
c = {}
```

无法理解变量用途。

---

### 函数过长

```python
def solve():
    # 500行代码
```

阅读困难。

---

### 缺少注释和文档

```python
def process():
    ...
```

不知道函数作用。

---

### 缺少测试

```text
代码能运行
↓
不确定是否正确
```

---

## 为什么会产生技术债务

常见原因：

```text
时间压力
```

---

```text
快速上线
```

---

```text
需求频繁变更
```

---

```text
缺少代码审查
```

---

```text
开发者偷懒
```

---

## LLM 如何帮助减少技术债务

课程核心观点：

```text
LLM
不仅能写代码

还能帮助维护代码
```

---

## 场景 1：解释旧代码

Prompt：

```text
Explain this code.

What does it do?
```

---

作用：

```text
快速理解遗留代码
```

---

## 场景 2：生成注释

Prompt：

```text
Add comments to this code.
```

---

输出：

```python
# Calculate total order price
total = ...
```

---

作用：

```text
提高可读性
```

---

## 场景 3：生成文档

Prompt：

```text
Write documentation
for this function.
```

---

输出：

```python
"""
Parameters
Returns
Examples
"""
```

---

作用：

```text
减少知识流失
```

---

## 场景 4：代码审查

Prompt：

```text
Review this code.

Suggest improvements for:

- readability
- maintainability
- performance
```

---

LLM 可以发现：

- 重复逻辑
- 不合理命名
- 复杂函数
- 潜在问题

---

## 场景 5：重构（Refactoring）

Prompt：

```text
Refactor this code.
```

---

例如：

原代码：

```python
if ...
elif ...
elif ...
```

---

重构后：

```python
mapping = {
    ...
}
```

---

作用：

```text
降低维护成本
```

---

## 场景 6：生成测试

Prompt：

```text
Generate unit tests
for this function.
```

---

作用：

```text
保证重构安全
```

---

### 工作流程

```text
旧代码
↓
生成测试
↓
重构代码
↓
运行测试
```

---

## 课程案例

课程通过一个已有项目演示：

```text
阅读代码
↓
理解逻辑
↓
发现问题
↓
补充文档
↓
重构代码
```

说明：

```text
LLM 可以帮助处理历史项目
```

---

## LLM 与技术债务

课程强调：

```text
LLM
不能自动消除技术债务
```

因为：

```text
LLM 不了解真实业务
```

---

正确方式：

```text
开发者分析
+
LLM辅助
```

---

## 最佳实践

### 1. 先理解

```text
Explain this code.
```

---

### 2. 再审查

```text
Review this code.
```

---

### 3. 再重构

```text
Refactor this code.
```

---

### 4. 最后测试

```text
Generate tests.
```

---

### 工作流

```text
理解
↓
审查
↓
重构
↓
测试
```

---

## 本章重点

### Technical Debt

```text
短期节省时间
↓
长期增加成本
```

---

### 常见表现

- 重复代码
- 命名混乱
- 大函数
- 缺少文档
- 缺少测试

---

### LLM 能做什么

- Explain Code
- Add Comments
- Write Documentation
- Review Code
- Refactor Code
- Generate Tests

---

### 推荐流程

```text
Explain
↓
Review
↓
Refactor
↓
Test
```

---

## 一句话总结

```text
Technical debt is easier to prevent and reduce when you use an LLM to understand, document, review, and refactor code.
```

利用 LLM 理解、文档化、审查和重构代码，可以更高效地减少技术债务。