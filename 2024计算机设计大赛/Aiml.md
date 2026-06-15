# AIML学习

- aiml不区分大小写

## 基本标签

<table><thead><tr><th>AIML标签</th><th>定义</th></tr></thead><tbody><tr><td>&lt;aiml&gt;</td><td>定义AIML文档的<strong>开头和结尾</strong>.</td></tr><tr><td>&lt;category&gt;</td><td>在Alicebot的知识中定义<strong>知识单元</strong> .</td></tr><tr><td>&lt;pattern&gt;</td><td>定义模式以匹配用户可以输入到Alicebot的内容.<strong>匹配输入</strong></td></tr><tr><td>&lt;template&gt;</td><td>定义一个响应Alicebot到用户的输入. <strong>控制输出</strong></td></tr></tbody></table>

## 特殊标签

<table><thead><tr><th>AIML标签</th><th>定义</th></tr></thead><tbody><tr><td>&lt;star&gt;</td><td>用于匹配&lt; pattern&gt;中的通配符 * 字符标签.</td></tr><tr><td>&lt;srai&gt;</td><td>多用途标记，用于调用/匹配其他类别.</td></tr><tr><td>&lt;random&gt;</td><td>使用&lt; random&gt; 获得随机回复.</td></tr><tr><td>&lt;li&gt;</td><td>用于表示多个回复.</td></tr><tr><td>&lt;set&gt;</td><td>用于设置AIML变量中的值.</td></tr><tr><td>&lt;get&gt;</td><td>用于获取存储在AIML变量中的值.</td></tr><tr><td>&lt;that&gt;</td><td>在AIML中用于根据上下文做出回应.</td></tr><tr><td>&lt;topic&gt;</td><td>在AIML中用于存储上下文，以便以后的会话可以根据该上下文完成.</td></tr><tr><td>&lt;think&gt;</td><td>在AIML中用于存储变量而不通知用户.</td></tr><tr><td>&lt;condition&gt;</td><td>与编程语言中的switch语句类似.它有助于ALICE响应匹配的输入.</td></tr></tbody></table>

***



## 基本用法

### aiml

< aiml> 标签标记AIML文档的**开头**和**结尾**   必须指定版本和编码方式

```
<aiml version = "1.0" encoding = "UTF-8"?>
   ...
</aiml>
```

### category

一个 < category> 标记必须包含输入< pattern> 和输出< template> 标记.
其中： < pattern> 表示用户输入，< template> 表示机器人的响应.

- < pattern> 标签表示用户的输入.它应该是< category>中的**第一个**标记标签
- < template>标签表示机器人对用户的响应.它应该是< category>中的**第二个**标记标签.

```
<category>
   <pattern> HELLO ALICE </pattern>
   <template>Hello User</template>
</category>
```

### star

< star> 标记用于匹配< pattern>中的通配符 * 字符

```
<star index = "n"/>
```

**n** 表示< pattern>中用户输入中*的位置标记

示例

```
   <category>
      <pattern>I LIKE *</pattern>
      <template>
         I too like <star/>.
      </template>
   </category>
```

如果用户输入"I like dogs"
然后机器人会回答"I too like dogs."

```
   <category>
      <pattern> A * is a *. </pattern>
      <template>
         When a <star index = "1"/> is not a <star index = "2"/>?
      </template>
   </category>
```

如果用户输入"A dog is a kind of animal."
然后机器人会回答"When a dog is not a kind of animal？"

### srai

< srai> 标签是一种多用途标签.此标记使AIML能够为同一模板定义不同的目标.

- 符号缩减

  符号缩减技术用于简化模式.它有助于用简单的模式减少复杂的语法模式.

  ```
  <category>
     <pattern> 谁是张三? </pattern>
     <template> 张三是学生 </template>
  </category>
  
  <category>
     <pattern> 谁是李四? </pattern>
     <template> 李四是老师 </template>
  </category>
  
  <category>
     <pattern> * 是谁? </pattern>
     <template>
        <srai> 谁是 <star/></srai>
     </template>
  </category>
  ```

  Human: 张三是谁？

  Robot:张三是学生 

  

- 分而治之

  Divide and Conquer用于在完成回复时重复使用子句.它有助于减少定义多个类别

  ```
     <category>
        <pattern>再见</pattern>
        <template>拜拜</template>
     </category>
  
     <category>
        <pattern>再见 *</pattern>
        <template>
           <srai>再见</srai>
        </template>
     </category>
  ```

- 同义词解释

  同义词是具有相似含义的词.机器人应该以相同的方式回复类似的单词.

  ```
  <category>
     <pattern>FACTORY</pattern>
     <template>Development Center!</template>
  </category>
  
  <category>
     <pattern>INDUSTRY</pattern>
     <template>
        <srai>FACTORY</srai>
     </template>
  </category>
  ```

  Human: Factory
  Robot: Development Center!
  Human: Industry
  Robot: Development Center!

  

- 关键词检测

  使用 srai ，我们可以在用户返回简单响应键入一个特定的关键词，比如学校，无论句子中出现"学校".

  ```
  <category>
     <pattern>SCHOOL</pattern>
     <template>School is an important institution in a child's life.</template>
  </category>
  
  <category>
     <pattern>_ SCHOOL</pattern>
     <template>
        <srai>SCHOOL</srai>
     </template>
  </category>
  
  <category>
     <pattern>SCHOOL *</pattern>
     <template>
        <srai>SCHOOL</srai>
     </template>
  </category>
  
  <category>
     <pattern>_ SCHOOL *</pattern>
     <template>
        <srai>SCHOOL</srai>
     </template>
  </category>
  ```

  Human: I love going to school daily.
  Robot: School is an important institution in a child’s life.
  Human: I like my school.
  Robot: School is an important institution in a child’s life.



### that

连接上下文

```
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>WHAT ABOUT MOVIES</pattern>
      <template>Do you like comedy movies</template>  
   </category>

   <category>
      <pattern>YES</pattern>
      <that>Do you like comedy movies</that>
      <template>Nice, I like comedy movies too.</template>
   </category>

   <category>
      <pattern>NO</pattern>
      <that>Do you like comedy movies</that>
      <template>Ok! But I like comedy movies.</template>
   </category> 

</aiml>
```

Human: What about movies? Robot: Do you like comedy movies? Human: No Robot: Ok! But I like comedy movies.



### random & li

< random> 标签用于获取随机响应.此标签使AIML能够针对相同的输入做出不同的响应. < random>标签与< li>一起使用标签. < li> 标签带有随机传递给用户的不同响应.

```
   <category>
      <pattern>HI</pattern>
      
      <template>
         <random>
            <li> Hello! </li>
            <li> Hi! Nice to meet you! </li>
         </random>
      </template>
   <category>      
```

Human: Hi
Robot: Hi! Nice to meet you!
Human: Hi
Robot: Hello!



### set & get

< set> 和< get> 标记用于处理AIML中的变量.变量可以是预定义变量或程序员创建的变量

< set> tag用于设置变量中的值.

```
<set name = "variable-name"> variable-value </set>
```

< get> tag用于从变量中获取值.

```
<get name = "variable-name"></get>
```

```
   <category>
      <pattern>I am *</pattern>
      <template>
         Hello <set name = "username"> <star/>! </set>
      </template>  
   </category>  
   
   <category>
      <pattern>Good Night</pattern>
      <template>
         Good Night <get name = "username"/>!
      </template>  
   </category>  

```

Human: I am Mahesh
Robot: Hello Mahesh!
Human: Good Night
Robot: Good Night Mahesh! 



### topic

< topic> 标记在AIML中用于存储上下文，以便以后的对话可以根据该上下文完成.通常，< topic> 标记用于是/否类型对话.它有助于AIML搜索在主题上下文中编写的类别.

使用< set>定义主题标签

```
<template> 
   <set name = "topic"> topic-name </set>
</template>
```

使用< topic>定义类别标签

```
<topic name = "topic-name">
   <category>
      ...
   </category>     
</topic>
```

```
<aiml version = "1.0" encoding = "UTF-8"?>

   <category>
      <pattern>LET DISCUSS MOVIES</pattern>
      <template>Yes <set name = "topic">movies</set></template>  
   </category>
   
   <topic name = "movies">
      <category>
         <pattern> * </pattern>
         <template>Watching good movie refreshes our minds.</template>
      </category>
      
      <category>
         <pattern> I LIKE WATCHING COMEDY! </pattern>
         <template>I like comedy movies too.</template>
      </category>   
   </topic>
   
</aiml>
```

Human: let discuss movies
Robot: Yes movies
Human: Comedy movies are nice to watch
Robot: Watching good movie refreshes our minds.
Human: I like watching comedy
Robot: I too like watching comedy.



### think

< think> 标签在AIML中用于存储变量而不通知用户.

```
<think> 
   <set name = "variable-name"> variable-value </set>
</think>
```

示例：

```
<aiml version = "1.0" encoding = "UTF-8"?>

   <category>
      <pattern>My name is *</pattern>
      <template>
         Hello!<think><set name = "username"> <star/></set></think>
      </template>  
   </category>  
   
   <category>
      <pattern>Byeee</pattern>
      <template>
         Byeee <get name = "username"/>. Thanks for the conversation!
      </template>  
   </category>  

</aiml>
```

```
Human: My name is Mahesh
Robot: Hello!
Human: Byeee
Robot: Byeee Mahesh Thanks for the conversation!
```



### condition

< condition> 标记类似于编程语言中的switch语句.它有助于ALICE响应匹配的输入

```
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern> HOW ARE YOU FEELING TODAY </pattern>
      
      <template>
         <think><set name = "state"> happy</set></think>
         <condition name = "state" value = "happy">
            I am happy!
         </condition>
         
         <condition name = "state" value = "sad">
            I am sad!
         </condition>
      </template>
      
   </category>
</aiml>
```

Human: How are you feeling today
Robot: I am happy!



### system

system内部可以写python代码，获知使用XXX.py来调用等

![image-20240104212848845](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20240104212848845.png)



