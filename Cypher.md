# Neo4j学习

官方文档[Neo4j 官方文档（中文版） - Amαdeus - 博客园 (cnblogs.com)](https://www.cnblogs.com/MAKISE004/p/17537963.html)







## 1Cypher语言

### 1.1运算符

| 常规运算   | DISTINCT, ., []                           |
| :--------- | :---------------------------------------- |
| 算数运算   | +, -, *, /, %, ^                          |
| 比较运算   | =, <>, <, >, <=, >=, IS NULL, IS NOT NULL |
| 逻辑运算   | AND, OR, XOR, NOT                         |
| 字符串操作 | +                                         |
| List操作   | +, IN, [x], [x .. y]                      |
| 正则操作   | =~                                        |
| 字符串匹配 | STARTS WITH, ENDS WITH, CONTAINS          |







### 1.2创建语句CREATE

#### 创建节点CREATE

```cypher
CREATE (n:SIGN {PROPERTY}) RETURN n
CREATE (n:Person {name:'张三'}) RETURN n 
CREATE (n:Location {city:'呼和浩特', state:'和林格尔'})
//"RETURN n"部分指示Neo4j返回该节点，以便在查询执行后显示或进一步处理它。
```

![image-20231024211618469](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024211618469.png)



#### 创建关系

MATCH语句是查询操作，用来匹配一定模式，可以是简单的节点、关联，也可以是复杂的路径。
MERGE语句是创建关系的操作，建立一条由a到b的边，边的关系类型是RELATION

```cypher
MATCH (a:SIGN {PROPERTY}),
      (b:SIGN {PROPERTY})
MERGE (a)-[:RELATION]->(b)
//示例
MATCH (a:Person {name:'张三'}), 
      (b:Location {city:'呼和浩特'}) 
MERGE (a)-[:FRIENDS]->(b)

```

![image-20231024212436570](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024212436570.png)

边也可以添加属性，例如：

```
MATCH (a:Person {name:'张三'}), 
      (b:Location {city:'呼和浩特'}) 
MERGE (a)-[:BORN_IN {year:1978}]->(b)

```

![image-20231024212803385](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024212803385.png)







### 1.3查找语句MATCH

#### 查看所有节点

```cypher
MATCH (n) RETURN n
```

![image-20231024213448429](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024213448429.png)

<hr/>



#### 查看所有节点及其关系

```
MATCH (n)-[r]->(m) RETURN n, r, m
```

![image-20231024213511572](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024213511572.png)

<hr/>



#### 查看所有对外有关系的节点

```
MATCH (a)-->() RETURN a
```

![image-20231024213530488](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024213530488.png)

<hr/>



#### 查看具有特点标签的节点：

```
MATCH (n:Label) RETURN n
//此处Label为Person
```

![image-20231024213808553](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024213808553.png)

<hr/>



#### 查看具有特定属性值的节点：

```
MATCH (n {property: value}) RETURN n
//MATCH (n {city: '呼和浩特'}) RETURN n  举例
```

![image-20231024213944109](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024213944109.png)

<hr/>



#### 查看节点及其邻居节点之间的关系：

```
MATCH (n)-[r]-(m) RETURN n, r, m
```

![image-20231024214006038](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024214006038.png)

<hr/>



#### 查看节点及其邻居节点之间的关系：

```
MATCH path = (n)-[r*]->() WHERE n.property = value RETURN path
```

原始数据

![image-20231024214311812](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024214311812.png)

查询后

```
MATCH path = (n)-[r*]->() WHERE n.name = '李四' RETURN path
```

![image-20231024214603345](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024214603345.png)

<hr/>





### 1.4修改语句SET

#### 修改节点

在这里，SET表示修改操作，如果属性不存在，则新建该属性并赋值

```
MATCH (a:SIGN {PROPERTY_1}) SET a.PROPERTY_1=x
MATCH (a:SIGN {PROPERTY_1}) SET a.PROPERTY_2=x
MATCH (a:Person {name:'张三'}) SET a.age=34  //示例
```

![image-20231024215445984](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024215445984.png)

![image-20231024215457303](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024215457303.png)

***



#### 修改关系

```
MATCH (n)-[r:结交]->(m) 
WHERE r.year = 2015 
SET r.year = 2023 
RETURN n, r, m
```

原始数据

![image-20231024215903110](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024215903110.png)

![image-20231024220140977](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024220140977.png)

修改后

![image-20231024220205447](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231024220205447.png)

***





### 1.5删除语句DELETE

删除节点

```
MATCH (a:SIGN {PROPERTY}) DELETE a
MATCH (a:Location {city:'呼和浩特'}) DELETE a  //示例
```

删除关系

```
MATCH ()-[r]-() DELETE r
```

删除节点但不删除关系

```
MATCH (n) WHERE id(n) = <node_id> DETACH DELETE n
```

删除关系但不删除节点

```
MATCH ()-[r]-() WHERE id(r) = <relationship_id> DELETE r
```

删除所有内容

```
MATCH (n) DETACH DELETE n
```

***







## 2导入csv文件

首先构造csv文件

将文件拷贝到如下操作

![image-20231025160407739](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231025160407739.png)

***



### 2.1创建节点

执行语句

```cypher
LOAD CSV WITH HEADERS FROM'file:///specialist.CSV' AS line
CREATE (:specialist {id:line.id,name:line.name,direction:line.direction})
```

结果

![image-20231025160516374](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231025160516374.png)

***

### 2.2创建关系

申请者

![image-20231025165750772](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231025165750772.png)

专家

![image-20231025165810919](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231025165810919.png)

关系

![image-20231025165824548](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231025165824548.png)

```cypher
LOAD CSV WITH HEADERS FROM'file:///relationship.CSV' AS line
MATCH (from:applicant{id:line.application_id}),(to:specialist {id:line.specialist_id})
MERGE (from)-[r:递交]->(to)

//解释
applicant{id:line.application_id}
id:申请者表里的字段
application_id:关系表里的字段

specialist {id:line.specialist_id}
id:专家表里的字段
specialist_id:关系表里的字段

```

结果

![image-20231025165856615](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231025165856615.png)

***



### 2.3创建索引

提升搜索速度，设置name唯一

```
create constraint on (b:)
assert b.name is unique
```



### 2.3批量导入csv文件

[操作方法：使用 Neo4j 桌面导入 CSV 数据 - 入门](https://neo4j.com/docs/getting-started/appendix/tutorials/guide-import-desktop-csv/)

#### 在该目录下导入csv文件

![image-20231027193151667](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027193151667.png)

#### 绘图之前先检查数据

产品.csv

```
//view data rows in products.csv

LOAD CSV FROM 'file:///products.csv' AS row
RETURN row
LIMIT 3;
```

![image-20231027194214584](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027194214584.png)

***



订单.csv

```
//count data rows in orders.csv (headers)

LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
RETURN row
LIMIT 5;
```

![image-20231027194238558](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027194238558.png)

***

订单细节.csv

```
//count data rows in order-details.csv (headers)
LOAD CSV WITH HEADERS FROM 'file:///order-details.csv' AS row
RETURN row
LIMIT 8;
```

![image-20231027194951577](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027194951577.png)

***







#### 注意数据的数据类型

该命令将所有值读取为字符串。 无论该值在文件中如何显示，它都将作为字符串加载。 因此，在导入之前，请确保转换任何非字符串值。`LOAD CSV``LOAD CSV`

Cypher中有多种转换功能。 您将用于本练习的那些如下：

- `**toInteger()**`：将值转换为整数。
- `**toFloat()**`：将值转换为浮点数（在本例中为货币金额）。
- `**datetime()**`：将值转换为*日期时间*。



产品.csv

```
LOAD CSV FROM 'file:///products.csv' AS row
WITH toInteger(row[0]) AS productId, row[1] AS productName, toFloat(row[2]) AS unitCost
RETURN productId, productName, unitCost
LIMIT 3;
```

![image-20231027195122373](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027195122373.png)

***



订单.csv

```
LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
WITH toInteger(row.orderID) AS orderId, datetime(replace(row.orderDate,' ','T')) AS orderDate, row.shipCountry AS country
RETURN orderId, orderDate, country
LIMIT 5;
```

![image-20231027195153727](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027195153727.png)

***



订单详情.csv

```
LOAD CSV WITH HEADERS FROM 'file:///order-details.csv' AS row
WITH toInteger(row.productID) AS productId, toInteger(row.orderID) AS orderId, toInteger(row.quantity) AS quantityOrdered
RETURN productId, orderId, quantityOrdered
LIMIT 8;
```

![image-20231027195742778](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027195742778.png)

***



#### 绘图

添加约束

```
CREATE CONSTRAINT UniqueProduct FOR (p:Product) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT UniqueOrder FOR (o:Order) REQUIRE o.id IS UNIQUE;
```

构建产品节点

```
LOAD CSV FROM 'file:///products.csv' AS row
WITH toInteger(row[0]) AS productId, row[1] AS productName, toFloat(row[2]) AS unitCost
MERGE (p:Product {productId: productId})
  SET p.productName = productName, p.unitCost = unitCost
RETURN count(p);

//查看
//validate products loaded correctly
MATCH (p:Product)
RETURN p LIMIT 20;
```

![image-20231027195955872](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027195955872.png)

***



构建订单节点

```
LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
WITH toInteger(row.orderID) AS orderId, datetime(replace(row.orderDate,' ','T')) AS orderDate, row.shipCountry AS country
MERGE (o:Order {orderId: orderId})
  SET o.orderDateTime = orderDate, o.shipCountry = country
RETURN count(o);

//查看
//validate orders loaded correctly
MATCH (o:Order)
RETURN o LIMIT 20;
```

![image-20231027200041093](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027200041093.png)

***



构建订单细节关系

```
:auto LOAD CSV WITH HEADERS FROM 'file:///order-details.csv' AS row
CALL {
 WITH row
 MATCH (p:Product {productId: toInteger(row.productID)})
 MATCH (o:Order {orderId: toInteger(row.orderID)})
 MERGE (o)-[rel:CONTAINS {quantityOrdered: toInteger(row.quantity)}]->(p)
} IN TRANSACTIONS OF 500 ROWS

//查看
MATCH (o:Order)-[rel:CONTAINS]->(p:Product)
RETURN p, rel, o LIMIT 50;
```

![image-20231027200128348](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231027200128348.png)





## 3算法设计



加载数据

```
load csv with headers from'file:///transport-nodes.csv' as row
merge(place:Place{id:row.id})
set place.latitude = toFloat(row.latitude),
    place.longitude = toFloat(row.latitude),
    place.population = toInteger(row.population)

load csv with headers from'file:///transport-relationships.csv' as row
match (origin:Place {id:row.src})
match(destination:Place {id:row.dst})
merge(origin)-[:EROAD {distance:toInteger(row.cost)}]->(destination)

```

最短路径算法

```
MATCH (source:Place {id: "Amsterdam"})
MATCH (destination:Place {id: "London"})
call algo.SHORTESTPATH.stream(source, destination, null)
yield nodeId, cost
return algo.getNodeById(nodeId).id as place, cost

```

## 4导入数据

### 节点

```
LOAD CSV WITH HEADERS FROM'file:///object.CSV' AS line
CREATE (:Object {id:line.id,spusername:line.spusername,name:line.name,xmlb:line.xmlb,yjsx:line.yjsx,yjxk:line.yjxk,sjxk:line.sjxk,starttime:line.starttime,endtime:line.endtime,ytjd:line.ytjd,fzr:line.fzr,xuew:line.xuew,zhic:line.zhic,birthday:line.birthday,dwmc:line.dwmc,sqjf:line.sqjf,xmzy:line.xmzy,hwgiz:line.hwgiz,sbnd:line.sbnd})
项目节点
```

```
LOAD CSV WITH HEADERS FROM'file:///team.CSV' AS line
CREATE (:Person {id:line.id,name:line.name,sex:line.sex,spusername:line.spusername,xuew:line.xuew,zhic:line.zhic,dwmc:line.dwmc,sxzy:line.sxzy,stae:line.stae,sbnd:line.sbnd,birthday:line.birthday,starttime:line.starttime,endtime:line.endtime})
科研人员节点
```

### 关系

#### 项目-人员

```
LOAD CSV WITH HEADERS FROM'file:///o_t_relationship.CSV' AS line
MATCH (from:Person{id:line.teamID}),(to:Object {id:line.objectID})
MERGE (from)-[r:申报]->(to)
人员-申报-项目
```

```
LOAD CSV WITH HEADERS FROM'file:///duiyou_object.CSV' AS line
MATCH (from:Person{id:line.personID}),(to:Object {id:line.objectID})
MERGE (from)-[r:队友申报]->(to)
人员-队友申报-项目
```

#### 人员-人员

```
LOAD CSV WITH HEADERS FROM'file:///f_m_relationship.CSV' AS line
MATCH (from:Person{id:line.memberID}),(to:Person{id:line.fzrID})
MERGE (from)-[r:协作]->(to)
成员-协作-负责人
```

```
LOAD CSV WITH HEADERS FROM'file:///sxzy_relationship.CSV' AS line
MATCH (from:Person{id:line.sxzy_A_id}),(to:Person{id:line.sxzy_B_id})
MERGE (from)-[r:相同专业]->(to)
人员-相同专业-人员
```



#### 项目-项目

```
LOAD CSV WITH HEADERS FROM'file:///ytjd_relationship.CSV' AS line
MATCH (from:Object{id:line.ytjd_A_id}),(to:Object{id:line.ytjd_B_id})
MERGE (from)-[r:相同依托基地]->(to)
项目-相同依托基地-项目
```

```
LOAD CSV WITH HEADERS FROM'file:///yjxk_relationship.CSV' AS line
MATCH (from:Object{id:line.yjxk_A_id}),(to:Object{id:line.yjxk_B_id})
MERGE (from)-[r:相同一级学科]->(to)
项目-相同一级学科-项目
```

```
LOAD CSV WITH HEADERS FROM'file:///sjxk_relationship.CSV' AS line
MATCH (from:Object{id:line.sjxk_A_id}),(to:Object{id:line.sjxk_B_id})
MERGE (from)-[r:相同三级学科]->(to)
项目-相同三级学科-项目
```

