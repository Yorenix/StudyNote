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
```

#### 作用

避免模型在信息不足时胡乱生成答案。

---

### 4. Few-shot Prompting（少样本提示）

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