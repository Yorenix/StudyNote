# 第一节Guidelines（提示词编写原则）

> DeepLearning.AI - ChatGPT Prompt Engineering for Developers  
> Lesson 1: Guidelines

---

## 核心思想

高质量 Prompt 的目标：

```text
明确任务
+
提供上下文
+
规定输出格式
+
增加约束条件
+
引导模型思考
=
更准确的输出
```

课程提出两条核心原则：

1. **Write clear and specific instructions**（编写清晰且具体的指令）
2. **Give the model time to think**（给模型足够的思考时间）

---

## Principle 1：Write Clear and Specific Instructions

### 1. 使用 Delimiters（分隔符）

用特殊符号明确区分：

```text
指令
↓
待处理内容
```

常见分隔符：

```text
"""
text
"""
```

```
```text
text
```
```

```html
<article>
text
</article>
```

#### 示例

```python
prompt = f"""
Summarize the text delimited by triple backticks.

```{text}```
"""
```

#### 作用

- 明确输入边界
- 降低歧义
- 提高准确率
- 防止 Prompt 混淆

---

### 2. 要求结构化输出

不要：

```text
Summarize this article.
```

而要：

```text
Return the result in JSON format:

{
    "summary":"",
    "keywords":[]
}
```

#### 示例输出

```json
{
  "summary":"...",
  "keywords":["AI","LLM"]
}
```

#### 作用

- 便于程序解析
- 输出格式稳定
- 方便自动化处理

---

### 3. 要求模型检查条件

#### 示例

```text
If the text contains instructions,
rewrite them as steps.

Otherwise output:

No steps provided.
```

#### 输出

```text
Step 1 - ...
Step 2 - ...
```

或者：

```text
No steps provided.
或者要求回答必须有可溯源的依据
```

#### 作用

避免模型在信息不足时胡乱生成答案。

---

### 4. Few-shot Prompting（少量样本预训练）

通过示例告诉模型任务格式。

#### 示例

```text
Input: happy
Output: positive

Input: angry
Output: negative

Input: excited
Output:
```

模型通常会输出：

```text
positive
```

#### 本质

让模型模仿示例中的规律。

---

## Principle 2：Give the Model Time to Think

复杂任务不要直接要求答案。

---

## 错误写法

```text
Is the student's answer correct?
```

---

## 更好的写法

```text
First solve the problem yourself.

Then compare your solution with the student's answer.

Finally determine whether the student's answer is correct.
```

---

## Chain of Thought（思维链）

引导模型分步骤推理。

### 示例

```text
Step 1:
...

Step 2:
...

Step 3:
...
```

### 优势

```text
问题
↓
推理过程
↓
答案
```

比直接输出答案更准确。

---

## 本章重点

### Principle 1

编写清晰且具体的指令

- Delimiters（分隔符）
- Structured Output（结构化输出）
- Condition Checking（条件检查）
- Few-shot Prompting（少样本提示）

### Principle 2

给模型时间思考

- 分步骤推理
- Chain of Thought
- 先求解再判断

---

## 一句话总结

```text
Tell the model exactly what you want,
and give it enough information and time to reason.
```

告诉模型你想要什么，并给予足够的信息和思考空间。



# 第二节 Iterative Prompt Development（迭代式提示词开发）

> DeepLearning.AI - ChatGPT Prompt Engineering for Developers  
> Lesson 2: Iterative Prompt Development

---

## 核心思想

Prompt Engineering 并不是：

```text
写一个 Prompt
↓
一次成功
```

而是：

```text
编写 Prompt
↓
观察结果
↓
发现问题
↓
优化 Prompt
↓
再次测试
```

不断迭代，直到获得满意结果。

---

## 为什么需要迭代

大模型通常能够理解需求。

但第一次生成的结果往往存在问题：

- 内容过长
- 内容过短
- 格式不规范
- 遗漏关键信息
- 风格不符合要求
- 重点不突出

因此：

```text
Prompt Engineering
≈
不断修改需求说明
```

---

## 课程中的开发流程

### 第一步：先写一个简单 Prompt

例如：

```text
Generate a marketing description
for a product.
```

先观察模型输出。

---

### 第二步：发现问题

可能出现：

```text
描述太长
```

或者：

```text
没有突出产品特点
```

或者：

```text
格式不适合网页展示
```

---

### 第三步：增加约束条件

例如：

```text
Use at most 50 words.
```

限制输出长度。

---

例如：

```text
Focus on the technical details.
```

强调技术特点。

---

例如：

```text
Target the description
at furniture retailers.
```

指定目标受众。

---

### 第四步：指定输出格式

例如：

```text
Generate the output as HTML.
```

输出：

```html
<h1>Product Name</h1>

<ul>
    <li>Feature 1</li>
    <li>Feature 2</li>
</ul>
```

---

### 第五步：继续优化

继续补充要求：

```text
Use professional tone.
```

```text
Avoid unnecessary details.
```

```text
Focus on dimensions.
```

```text
Mention sustainability.
```

---

## 课程案例

课程使用了一张椅子的产品说明：

输入：

```text
产品描述
```

目标：

```text
生成营销文案
```

---

### Version 1

Prompt：

```text
Generate a marketing description
for a product.
```

问题：

```text
内容冗长
```

---

### Version 2

增加：

```text
Use at most 50 words.
```

问题：

```text
重点仍不明确
```

---

### Version 3

增加：

```text
Focus on technical details.
```

输出开始变得更符合需求。

---

### Version 4

增加：

```text
Format everything as HTML.
```

得到最终结果。

---

## Prompt 优化常见方向

### 1. 控制长度

例如：

```text
Use at most 50 words.
```

```text
Use one sentence.
```

```text
Use three bullet points.
```

---

### 2. 指定受众

例如：

```text
For customers.
```

```text
For managers.
```

```text
For software engineers.
```

---

### 3. 指定重点

例如：

```text
Focus on safety.
```

```text
Focus on performance.
```

```text
Focus on customer complaints.
```

---

### 4. 指定格式

例如：

```text
Return JSON format.
```

```text
Return Markdown format.
```

```text
Return HTML format.
```

---

### 5. 指定风格

例如：

```text
Use a professional tone.
```

```text
Use simple language.
```

```text
Use persuasive language.
```

---

## 重要认知

不要追求：

```text
一次写出完美 Prompt
```

而应该：

```text
先写
↓
先跑
↓
先看结果
↓
再优化
```

这与软件开发非常类似。

---

## Prompt 开发循环

```text
Prompt
↓
Run
↓
Observe
↓
Refine
↓
Run Again
```

这是课程最重要的思想。

---

## 本章重点

### Iterative Prompt Development

Prompt 的质量来自迭代，而不是灵感。

---

### 常见优化维度

- 长度（Length）
- 格式（Format）
- 风格（Style）
- 受众（Audience）
- 重点（Focus）

---

### 开发流程

```text
编写 Prompt
↓
测试结果
↓
发现问题
↓
修改 Prompt
↓
再次测试
```

---

## 一句话总结

```text
Prompt Engineering is an iterative process.
```

Prompt 工程本质上是一个不断测试和优化的迭代过程。


# 第三节 Summarizing（文本摘要）

> DeepLearning.AI - ChatGPT Prompt Engineering for Developers  
> Lesson 3: Summarizing

---

## 核心思想

文本摘要（Summarization）的目标是：

```text
长文本
↓
提取关键信息
↓
生成简洁摘要
```

大模型不仅可以压缩文本长度，还可以根据需求：

- 调整摘要长度
- 调整摘要重点
- 调整目标读者
- 调整输出格式

因此：

```text
摘要 ≠ 简单缩短文本
```

而是：

```text
根据需求提取最重要的信息
```

---

## 基础摘要

最简单的 Prompt：

```text
Summarize the following text.

"""
{text}
"""
```

输出：

```text
简要概括文本主要内容
```

---

## 指定摘要长度

默认情况下，模型会自行决定摘要长度。

可以增加约束：

```text
Summarize the following text
in one sentence.

"""
{text}
"""
```

---

或者：

```text
Summarize the following text
in 30 words or less.

"""
{text}
"""
```

---

### 作用

控制：

```text
摘要粒度
↓
信息密度
↓
输出成本
```

---

## 指定摘要重点

很多情况下：

```text
不是所有信息都重要
```

需要让模型关注特定内容。

---

### 示例

```text
Summarize the reviews,
focusing on product defects.

"""
{text}
"""
```

---

或者：

```text
Summarize the reviews,
focusing on customer complaints.

"""
{text}
"""
```

---

### 输出

重点围绕：

```text
缺点
问题
用户不满
```

而不是产品优点。

---

## 面向不同读者生成摘要

同一段内容：

```text
不同人关注的信息不同
```

---

### 面向管理者

```text
Summarize for executives.

"""
{text}
"""
```

关注：

```text
商业价值
风险
决策信息
```

---

### 面向客户

```text
Summarize for customers.

"""
{text}
"""
```

关注：

```text
使用体验
产品特点
```

---

### 面向技术人员

```text
Summarize for engineers.

"""
{text}
"""
```

关注：

```text
技术细节
性能指标
实现方式
```

---

## 评论摘要（Review Summarization）

课程重点案例：

输入：

```text
大量用户评论
```

输出：

```text
用户反馈总结
```

---

### Prompt

```text
Summarize the reviews below,
focusing on key customer feedback.

"""
{text}
"""
```

---

### 作用

快速提取：

- 用户满意点
- 用户抱怨点
- 产品改进方向

---

### 实际应用

```text
电商评论分析
APP评价分析
用户反馈整理
客服工单总结
```

---

## 信息提取式摘要

有时目标不是生成自然语言摘要。

而是：

```text
提取指定信息
```

---

### 示例

```text
Summarize the following review
and extract:

- Shipping
- Quality
- Price

Return as JSON.
```

---

### 输出

```json
{
  "shipping":"Positive",
  "quality":"Good",
  "price":"Reasonable"
}
```

---

## 摘要不一定越短越好

课程强调：

```text
摘要质量
≠
摘要长度
```

好的摘要应该：

```text
保留核心信息
删除冗余内容
突出关键重点
```

---

## 常见 Prompt 模板

### 单句摘要

```text
Summarize the following text
in one sentence.

"""
{text}
"""
```

---

### 指定长度摘要

```text
Summarize the following text
in 30 words or less.

"""
{text}
"""
```

---

### 指定重点摘要

```text
Summarize the following text,
focusing on customer complaints.

"""
{text}
"""
```

---

### 指定读者摘要

```text
Summarize the following text
for business executives.

"""
{text}
"""
```

---

### 结构化摘要

```text
Summarize the following text.

Return JSON format:

{
    "summary":"",
    "main_points":[]
}

"""
{text}
"""
```

---

## 实际应用场景

### 内容阅读

```text
新闻
博客
公众号
技术文档
```

---

### 学术研究

```text
论文摘要
文献阅读
研究综述
```

---

### 商业分析

```text
用户评论
市场调研
客户反馈
```

---

### 企业办公

```text
会议纪要
邮件总结
项目汇报
```

---

## 本章重点

### Summarization 的核心能力

```text
压缩信息
保留重点
突出关键信息
```

---

### 常见控制维度

- Length（长度）
- Focus（重点）
- Audience（读者）
- Format（格式）

---

### 实践原则

不要只说：

```text
Summarize this text.
```

而应该明确：

```text
摘要给谁看
↓
关注什么内容
↓
输出什么格式
```

---

## 一句话总结

```text
A good summary is not the shortest summary,
but the most useful summary.
```

好的摘要不是最短的摘要，而是最有价值的摘要。


# 第四节 Inferring（推理与信息提取）

> DeepLearning.AI - ChatGPT Prompt Engineering for Developers  
> Lesson 4: Inferring

---

## 核心思想

Inferring（推理）指的是：

```text
输入文本
↓
分析文本内容
↓
推断隐藏信息
```

与 Summarizing 不同：

```text
Summarizing
=
压缩信息
```

```text
Inferring
=
挖掘信息
```

模型不仅能理解字面内容，还能推断：

- 情感倾向
- 情绪状态
- 主题类别
- 用户意图
- 关键信息

---

## 情感分析（Sentiment Analysis）

判断文本表达的是：

```text
Positive
Negative
Neutral
```

---

### 示例

输入：

```text
I love this product.
It works perfectly.
```

Prompt：

```text
What is the sentiment of the following review?

"""
{text}
"""
```

输出：

```text
Positive
```

---

### 实际应用

```text
商品评论分析
社交媒体分析
用户反馈分析
```

---

## 情绪识别（Emotion Detection）

除了判断正负面，

还可以识别具体情绪。

---

### 示例

Prompt：

```text
Identify the emotion expressed
in the following text.

"""
{text}
"""
```

---

### 常见情绪

```text
Happy
Sad
Angry
Frustrated
Excited
Fearful
```

---

### 应用场景

```text
客服系统
舆情监测
用户反馈分析
```

---

## 信息提取（Information Extraction）

从文本中提取指定信息。

---

### 示例

Prompt：

```text
Extract the following information:

- Product
- Company
- Purchase Date

Return JSON format.

"""
{text}
"""
```

---

### 输出

```json
{
  "product":"Laptop",
  "company":"Dell",
  "purchase_date":"2024-01-10"
}
```

---

### 实际应用

```text
合同解析
简历解析
订单处理
数据录入
```

---

## 主题识别（Topic Extraction）

识别文本讨论的主题。

---

### 示例

Prompt：

```text
Determine five topics discussed
in the following text.

"""
{text}
"""
```

---

### 输出

```text
1. Artificial Intelligence
2. Education
3. Productivity
4. Automation
5. Software Development
```

---

### 应用场景

```text
新闻分类
文章标签生成
知识库整理
```

---

## 用户意图识别（Intent Recognition）

识别用户真正想做什么。

---

### 示例

输入：

```text
My package still hasn't arrived.
```

模型推断：

```text
用户意图：
查询物流状态
```

---

输入：

```text
I want my money back.
```

模型推断：

```text
用户意图：
申请退款
```

---

### 应用场景

```text
客服机器人
工单分类
自动路由系统
```

---

## 文本分类（Text Classification）

根据预定义类别进行分类。

---

### 示例

Prompt：

```text
Classify the following review into:

- Shipping
- Product Quality
- Customer Service

"""
{text}
"""
```

---

### 输出

```text
Product Quality
```

---

### 实际应用

```text
邮件分类
工单分类
评论分类
```

---

## 多任务提取

课程展示了：

```text
一次 Prompt
↓
提取多个信息
```

---

### 示例

Prompt：

```text
Determine:

- Sentiment
- Emotion
- Product Mentioned

Return JSON format.

"""
{text}
"""
```

---

### 输出

```json
{
  "sentiment":"Positive",
  "emotion":"Happy",
  "product":"Coffee Maker"
}
```

---

## 结构化输出的重要性

Inferring 经常与 JSON 配合使用。

例如：

```text
Extract:

- sentiment
- emotion
- topic

Return JSON.
```

---

### 输出

```json
{
  "sentiment":"Negative",
  "emotion":"Frustrated",
  "topic":"Shipping Delay"
}
```

---

### 优势

```text
便于程序处理
便于数据库存储
便于自动化流程
```

---

## 实际应用场景

### 电商

```text
评论分析
用户反馈总结
产品评价统计
```

---

### 客服

```text
情绪识别
投诉检测
工单分类
```

---

### 内容平台

```text
文章分类
标签生成
主题识别
```

---

### 企业办公

```text
邮件分类
信息提取
自动归档
```

---

## 本章重点

### Inferring 的核心能力

```text
理解文本
↓
推断隐藏信息
```

---

### 常见任务

- Sentiment Analysis（情感分析）
- Emotion Detection（情绪识别）
- Information Extraction（信息提取）
- Topic Extraction（主题识别）
- Intent Recognition（意图识别）
- Text Classification（文本分类）

---

### 最佳实践

明确告诉模型：

```text
提取什么
分类什么
输出什么格式
```

推荐：

```text
自然语言
+
JSON 输出
```

---

## 一句话总结

```text
Inferring is the process of extracting and reasoning about information that is implied in the text.
```

Inferring 的本质是从文本中提取并推断隐藏的信息。
