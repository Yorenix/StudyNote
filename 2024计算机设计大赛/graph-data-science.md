# graph-data-science库

## 1内存估计

下面的查询是估计具有 100 个节点和 1000 个关系的虚构图的示例。

例

```cypher
CALL gds.graph.project.estimate('*', '*', {
  nodeCount: 100,
  relationshipCount: 1000,
  nodeProperties: 'foo',
  relationshipProperties: 'bar'
})
YIELD requiredMemory, treeView, mapView, bytesMin, bytesMax, nodeCount, relationshipCount
```

| required内存 | 字节最小值 | 字节最大值 | 节点计数 | relationshipCount |
| :----------- | :--------- | :--------- | :------- | :---------------- |
| “593 KiB”    | 607576     | 607576     | 100      | 1000              |

***





## 2运行算法



- `stream`
  - 以记录流的形式返回算法的结果。
- `stats`
  - 返回汇总统计信息的单个记录，但不写入 Neo4j 数据库。
- `mutate`
  - 将算法的结果写入投影图，并返回汇总统计信息的单条记录。
- `write`
  - 将算法结果写入 Neo4j 数据库，并返回一条汇总统计记录。

### 常见算法调用参数

- concurrency - 整数

  控制执行算法的并行度。 默认情况下，此值设置为 4。 有关并发设置和限制的更多详细信息，请参阅系统要求的 [CPU 部分](https://neo4j.com/docs/graph-data-science/current/installation/System-requirements/#system-requirements-cpu)。

- nodeLabels - 字符串列表

  如果运行算法的图形是使用多个节点标签投影投影的，则此参数可用于仅选择投影标签的子集。 该算法将仅考虑具有任何选定标签的节点。

- relationshipTypes - 字符串列表

  如果运行算法的图形是使用多个关系类型投影投影的，则此参数可用于仅选择投影类型的子集。 该算法将仅考虑与任何选定类型的关系。

- nodeWeightProperty - 字符串

  在支持节点权重的算法中，此参数定义包含权重的节点属性。

- relationshipWeightProperty - 字符串

  在支持关系权重的算法中，此参数定义包含权重的关系属性。 指定的属性必须存在于所有指定关系[类型的指定关系图](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-relationship-types)中。 这些值必须是数字，并且某些算法可能具有其他值限制，例如仅需要正权重。

- maxIterations - 整数

  对于迭代算法，此参数控制最大迭代次数。

- 公差 - 浮点

  许多迭代算法都接受容差参数。 它控制两次迭代之间的最小增量。 如果增量小于容差值，则认为算法收敛并停止。

- seedProperty - 字符串

  某些算法可以增量计算。 这意味着即使图形已更改，也可以考虑先前执行的结果。 该参数定义包含种子值的节点属性。 种子设定可以加快计算和写入时间。`seedProperty`

- writeProperty - 字符串

  在模式下，此参数设置将结果写入的节点或关系属性的名称。 如果该属性已存在，则将覆盖现有值。`write`

- writeConcurrency - 整数

  在模式下，此参数控制写入操作的并行度。 默认值为`write``concurrency`

- jobId - 字符串

  可以提供要启动的作业的 ID，以便更轻松地对其进行跟踪，例如。GDS [的日志记录功能](https://neo4j.com/docs/graph-data-science/current/common-usage/logging/)。

- logProgress - 布尔值

  允许在运行过程时转动百分比日志记录的配置参数。默认情况下`off/on``on`

  ***

  

## 3图形管理

### 3.1采样

#### 随机游走采样方法

**语法**

```
CALL gds.graph.sample.rwr(
  graphName: String,
  fromGraphName: String,
  configuration: Map
)
YIELD
  graphName,
  fromGraphName,
  nodeCount,
  relationshipCount,
  startNodeCount,
  projectMillis
  
  
graphName：图的名称，表示采样后生成的新图的名称。
fromGraphName：起始图的名称，表示用于采样的原始图的名称。
nodeCount：采样后新图中的节点数量。
relationshipCount：采样后新图中的关系数量。
startNodeCount：采样操作的起始节点数量。
projectMillis：采样操作的持续时间，以毫秒为单位。
```

| Name                                                         | Type            | Default                             | Optional | Description                                                  |
| :----------------------------------------------------------- | :-------------- | :---------------------------------- | :------- | :----------------------------------------------------------- |
| [nodeLabels](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-node-labels) | List of String  | `['*']`                             | yes      | 使用给定的节点标签过滤命名图。将包含具有任何给定标签的节点。 |
| [relationshipTypes](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-relationship-types) | List of String  | `['*']`                             | yes      | 使用给定的关系类型筛选命名图。将包括与任何给定类型的关系。   |
| [concurrency](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-concurrency) | Integer         | `4`                                 | yes      | 用于运行算法的并发线程数。                                   |
| [jobId](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-jobid) | String          | `Generated internally`              | yes      | 可以提供该 ID 以更轻松地跟踪算法的进度。                     |
| [logProgress](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-logProgress) | Boolean         | `true`                              | yes      | 如果禁用，则不会记录进度百分比。                             |
| [relationshipWeightProperty](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-relationship-weight-property) | String          | `null`                              | yes      | 要用作权重的关系属性的名称。如果未指定，则算法运行未加权。   |
| samplingRatio                                                | Float           | `0.15`                              | yes      | 原始图中要采样的节点的比例。                                 |
| restartProbability                                           | Float           | `0.1`                               | yes      | 采样随机游走从其中一个起始节点重新开始的概率。               |
| startNodes                                                   | List of Integer | `A node chosen uniformly at random` | yes      | 原始图的初始节点集的 ID，采样随机游走将从中开始。            |
| nodeLabelStratification                                      | Boolean         | `false`                             | yes      | 如果为 true，则保留原始图的节点标签分布。                    |
| randomSeed                                                   | Integer         | `n/a`                               | yes      | 一个随机种子，用于计算中的所有随机性,需要concurrency = 1     |

示例

1创建数据

```
CREATE
  (nAlice:User {name: 'Alice'}),
  (nBridget:User {name: 'Bridget'}),
  (nCharles:User {name: 'Charles'}),
  (nDoug:User {name: 'Doug'}),
  (nMark:User {name: 'Mark'}),
  (nMichael:User {name: 'Michael'}),

  (nAlice)-[:LINK]->(nBridget),
  (nAlice)-[:LINK]->(nCharles),
  (nCharles)-[:LINK]->(nBridget),

  (nAlice)-[:LINK]->(nDoug),

  (nMark)-[:LINK]->(nDoug),
  (nMark)-[:LINK]->(nMichael),
  (nMichael)-[:LINK]->(nMark);
```

![image-20231104150004345](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104150004345.png)

2将该图形投影，并创建一个名为"myGraph"的新图形，并从现有图形中复制"User"节点和"LINK"关系类型到新图形中

```
CALL gds.graph.project( 'myGraph', 'User', 'LINK' )
```

3现在，我们可以继续使用 RWR 从“myGraph”中采样子图。 使用“Alice”节点作为我们的起始节点集，我们将冒险访问图中的四个节点作为我们的示例。 由于我们的图中总共有六个节点，并且 4/6 ≈ 0.66，我们将使用它作为我们的采样率。`User`

```
MATCH (start:User {name: 'Alice'})
CALL gds.graph.sample.rwr('mySample', 'myGraph', { samplingRatio: 0.66, startNodes: [start] })
YIELD nodeCount, relationshipCount
RETURN nodeCount, relationshipCount
```

![image-20231104155940474](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104155940474.png)

***



#### 共同邻居感知随机游走采样法

图形采样算法可用于减小大型复杂图形的大小，同时保留结构属性。 这有助于减少偏见，确保隐私，并使图形分析更具可扩展性。 采样算法广泛用于机器学习、社交网络分析和许多其他应用。

公共邻居感知随机游走 （CNARW） 是一种图采样技术，涉及优化下一跳节点的选择。 它考虑了当前节点和下一跃点候选项之间的公共邻居的数量。

根据这篇论文，简单随机游走趋向于缓慢收敛的一个主要原因是由于某些类型的图形（例如在线社交网络（OSN））的典型特征。 当随机统一移动到邻居时，很容易陷入局部循环并重新访问以前访问过的节点，从而减慢收敛速度。

为了解决这个问题，一种解决方案是优先考虑在每个步骤中提供更高概率探索未访问节点的节点。 具有较高度数的节点可能会提供此机会，但它们也可能与以前访问过的节点具有更共同的邻居，从而增加了重新访问的可能性。

因此，选择具有较高度数且与先前访问过的节点（或当前节点）较少的公共邻居的节点，不仅可以增加发现未访问节点的机会，还可以降低在后续步骤中重新访问以前访问过的节点的概率。

该算法的实现基于以下论文：

- [共同邻居很重要：具有共同邻居意识的快速随机游走采样](https://ieeexplore.ieee.org/abstract/document/9712235)

**语法**

```
CALL gds.graph.sample.cnarw(
  graphName: String,
  fromGraphName: String,
  configuration: Map
)
YIELD
  graphName,
  fromGraphName, //图形目录中原始图形的名称
  nodeCount,
  relationshipCount,
  startNodeCount,
  projectMillis  //投影子图的毫秒数
  
  
```

| [nodeLabels](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-node-labels) |     List of String      | `['*']`                             | yes  | 使用给定的节点标签过滤命名图。将包含具有任何给定标签的节点。 |
| :----------------------------------------------------------: | :---------------------: | ----------------------------------- | ---- | ------------------------------------------------------------ |
| [relationshipTypes](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-relationship-types) |     List of String      | `['*']`                             | yes  | 使用给定的关系类型筛选命名图。将包括与任何给定类型的关系。   |
| [concurrency](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-concurrency) |         Integer         | `4`                                 | yes  | 用于运行算法的并发线程数。                                   |
| [jobId](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-jobid) |         String          | `Generated internally`              | yes  | 可以提供该 ID 以更轻松地跟踪算法的进度。                     |
| [logProgress](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-logProgress) |         Boolean         | `true`                              | yes  | 如果禁用，则不会记录进度百分比。                             |
| [relationshipWeightProperty](https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/#common-configuration-relationship-weight-property) |         String          | `null`                              | yes  | 要用作权重的关系属性的名称。如果未指定，则算法运行未加权。   |
|                        samplingRatio                         |          Float          | `0.15`                              | yes  | 原始图中要采样的节点的比例。                                 |
|                      restartProbability                      |          Float          | `0.1`                               | yes  | 采样随机游走从其中一个起始节点重新开始的概率。               |
|                          startNodes                          | List of Integer or Node | `A node chosen uniformly at random` | yes  | 原始图的初始节点集的 ID，采样随机游走将从中开始。            |
|                   nodeLabelStratification                    |         Boolean         | `false`                             | yes  | 如果为 true，则保留原始图的节点标签分布。                    |
|                          randomSeed                          |         Integer         | `n/a`                               | yes  | 用于控制算法随机性的种子值。 请注意，设置此参数时必须设置为 1。 |



**示例**

1创建数据

```
CREATE
    (J:Female {name:'Juliette'}),
    (R:Male {name:'Romeo'}),
    (r1:Male {name:'Ryan'}),
    (r2:Male {name:'Robert'}),
    (r3:Male {name:'Riley'}),
    (r4:Female {name:'Ruby'}),
    (j1:Female {name:'Josie'}),
    (j2:Male {name:'Joseph'}),
    (j3:Female {name:'Jasmine'}),
    (j4:Female {name:'June'}),
    (J)-[:LINK]->(R),
    (R)-[:LINK]->(J),
    (r1)-[:LINK]->(R),   (R)-[:LINK]->(r1),
    (r2)-[:LINK]->(R),   (R)-[:LINK]->(r2),
    (r3)-[:LINK]->(R),   (R)-[:LINK]->(r3),
    (r4)-[:LINK]->(R),   (R)-[:LINK]->(r4),
    (r1)-[:LINK]->(r2),  (r2)-[:LINK]->(r1),
    (r1)-[:LINK]->(r3),  (r3)-[:LINK]->(r1),
    (r1)-[:LINK]->(r4),  (r4)-[:LINK]->(r1),
    (r2)-[:LINK]->(r3),  (r3)-[:LINK]->(r2),
    (r2)-[:LINK]->(r4),  (r4)-[:LINK]->(r2),
    (r3)-[:LINK]->(r4),  (r4)-[:LINK]->(r3),
    (j1)-[:LINK]->(J),   (J)-[:LINK]->(j1),
    (j2)-[:LINK]->(J),   (J)-[:LINK]->(j2),
    (j3)-[:LINK]->(J),   (J)-[:LINK]->(j3),
    (j4)-[:LINK]->(J),   (J)-[:LINK]->(j4),
    (j1)-[:LINK]->(j2),  (j2)-[:LINK]->(j1),
    (j1)-[:LINK]->(j3),  (j3)-[:LINK]->(j1),
    (j1)-[:LINK]->(j4),  (j4)-[:LINK]->(j1),
    (j2)-[:LINK]->(j3),  (j3)-[:LINK]->(j2),
    (j2)-[:LINK]->(j4),  (j4)-[:LINK]->(j2),
    (j3)-[:LINK]->(j4),  (j4)-[:LINK]->(j3) ;
```

![image-20231104162859401](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104162859401.png)

2投影图形并将其存储在图形目录中

```
CALL gds.graph.project( 'graph', ['Male', 'Female'], 'LINK' );
```

3现在，我们可以继续使用 CNARW 从“myGraph”中采样子图。 使用“Juliette”节点作为我们的一组起始节点，我们将冒险访问图中的五个节点作为我们的示例。 由于我们的图中总共有六个节点，并且 5/10 = 0.5，因此我们将使用它作为我们的采样率。

```
MATCH (start:Female {name: 'Juliette'})
CALL gds.graph.sample.cnarw('sampledGraph', 'graph',
{
    samplingRatio: 0.5,
    startNodes: [start]
})
YIELD nodeCount
RETURN nodeCount;
```

![image-20231104163048744](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104163048744.png)

***



### 3.2随机生成图形

图形生成按三个维度进行参数化：

- 节点计数 - 生成的图形中的节点数
- 平均度数 - 描述生成节点的平均出度数
- 关系分布函数 - 用于连接生成节点的概率分布方法

语法

```
CALL gds.graph.generate(
    graphName: String,
    nodeCount: Integer,
    averageDegree: Integer,
    configuration: Map
})
YIELD name, nodes, relationships, generateMillis, relationshipSeed, averageDegree, relationshipDistribution, relationshipProperty
```

参数

![image-20231104163932441](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104163932441.png)

配置

![image-20231104163943708](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104163943708.png)

结果

![image-20231104163954724](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104163954724.png)



关系分布

该参数控制用于生成新关系的统计方法。 目前有三种支持的方法：`relationshipDistribution`

- `UNIFORM`- 均匀分布传出关系，即每个节点具有完全相同的出出度（等于平均度数）。目标节点是随机选择的。
- `RANDOM`- 使用平均值为 和标准差为 的正态分布来分配传出关系。目标节点是随机选择的。`averageDegree``2 * averageDegree`
- `POWER_LAW`- 使用幂律分布来分配传入关系。out 度基于正态分布。



关系属性

图形生成器能够生成关系属性。 这可以使用接受以下参数的参数进行控制：`relationshipProperty`

配置

![image-20231104164404296](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104164404296.png)

目前，有两种支持生成关系属性的方法：

- `FIXED`- 为每个关系分配一个固定值。必须设置该参数。`value`
- `RANDOM`- 在下限 （） 和上限 （） 之间分配一个随机值。`min``max`

示例

#### 未加权图

创建数据

```
CALL gds.graph.generate('graph',5,2, {relationshipSeed:19})
YIELD name, nodes, relationships, relationshipDistribution
```

![image-20231104171616359](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104171616359.png)

已创建一个名为“包含节点和关系”的新内存中图形，并将其添加到图形目录中。 我们可以通过该过程检查其拓扑结构。

展示

```
CALL gds.graph.relationships.stream('graph')
YIELD sourceNodeId,targetNodeId
RETURN  sourceNodeId as source, targetNodeId as target
ORDER BY source ASC,target ASC
```

![image-20231104171703616](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104171703616.png)

#### 加权图

常见数据

```
CALL gds.graph.generate('weightedGraph',5,2, {relationshipSeed:19,
  relationshipProperty: {type: 'RANDOM', min: 5.0, max: 10.0, name: 'score'}})
YIELD name, nodes, relationships, relationshipDistribution
```

![image-20231104172258166](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104172258166.png)

生成的图形 具有一个名为的属性，该属性包含每个关系的随机值介于 5.0 和 10.0 之间。 我们可以用来流式传输图形的关系及其分数值

展示

```
CALL gds.graph.relationshipProperty.stream('weightedGraph','score')
YIELD sourceNodeId, targetNodeId, propertyValue
RETURN  sourceNodeId as source, targetNodeId as target, propertyValue as score
ORDER BY source ASC,target ASC, score
```

![image-20231104172335867](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231104172335867.png)

***



### 3.3图形操作

#### 创建图形

```
CALL gds.graph.project(
  graphName: String,
  nodeLabel: String,
  relationshipType: String,
  configuration: Map
)
YIELD
  graphName,
  nodeCount,
  relationshipCount

//实践
call gds.graph.project(
    'graph',
    ['Object', 'Person'],
    ['协作', '申报', '相同一级学科', '相同专业', '相同依托基地']
)
YIELD
graphName,nodeProjection,nodeCount,relationshipProjection,relationshipCount,projectMillis
```

- `graphName`：要进行投影的源图的名称，即在 Neo4j 图数据库中定义的已存在的图的名称。
- `nodeLabel`：要进行投影的源图中节点的标签。可以是单个标签或多个标签，如 `'Person'` 或 `['Person', 'Company']`。
- `relationshipType`：要进行投影的源图中关系的类型。可以是单个关系类型或多个关系类型，如 `'FOLLOWS'` 或 `['FOLLOWS', 'KNOWS']`。
- `configuration`：一个可选的配置选项的Map，用于配置过程的行为。可以包括节点属性、关系属性等配置信息。

配置

- `nodeProperties`: 指定要在投影中包含的节点属性。可以传递一个字符串数组，指定要包含的属性名称，或者可以使用 `'*'` 表示包含所有属性。
- `relationshipProperties`: 指定要在投影中包含的关系属性。可以传递一个字符串数组，指定要包含的属性名称，或者可以使用 `'*'` 表示包含所有属性。
- `modelName`: 指定新建的投影图的名称。
- `relationshipTypes`: 指定要在投影中包含的关系类型列表。可以传递一个字符串数组，指定要包含的关系类型，或者可以使用 `'*'` 表示包含所有关系类型。
- `includeIntermediateNodes`: 设置是否在投影中包含连接两个节点之间的中间节点。接受一个布尔值参数，默认为 `false`，表示不包含中间节点。

#### 更新图形

添加节点标签：

```
CALL gds.graph.nodeLabel.mutate(
    graphName: String,
    nodeLabel: String,
    configuration: Map
)
YIELD
    mutateMillis: Integer,
    graphName: String,
    nodeLabel: String,
    nodeLabelsWritten: Integer,
    nodeCount: Integer,
    configuration: Map
```

将定向关系转换为非定向关系

```
CALL gds.graph.relationships.toUndirected(
    graphName: String,
    configuration: Map
)
YIELD
    inputRelationships: Integer,
    relationshipsWritten: Integer,
    mutateMillis: Integer,
    postProcessingMillis: Integer,
    preProcessingMillis: Integer,
    computeMillis: Integer,
    configuration: Map
```

折叠路径：

折叠路径算法是一种遍历算法，能够在遍历的开始节点和结束节点之间创建关系。 换言之，起始节点和结束节点之间的路径被折叠成一个关系（直接路径）。 该算法旨在支持创建许多图算法所需的单部分图。

该算法的主要输入是路径模板列表。 从指定图中的每个节点开始，按照配置中指定的顺序逐个遍历每个模板的关系。 只有在遍历整个路径后到达的节点才被用作结束节点。 对于从开始节点到结束节点至少存在一条路径的每对节点，将创建一个有向关系。

```
CALL gds.collapsePath.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  mutateMillis: Integer,
  relationshipsWritten: Integer,
  configuration: Map
```



#### 列表图表

语法

```
CALL gds.graph.list(
  graphName: String
) YIELD
  graphName: String,
  database: String,
  configuration: Map,
  nodeCount: Integer,
  relationshipCount: Integer,
  schema: Map,
  schemaWithOrientation: Map,
  degreeDistribution: Map,
  density: Float,
  creationTime: Datetime,
  modificationTime: Datetime,
  sizeInBytes: Integer,
  memoryUsage: String
```

![image-20231105143813883](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105143813883.png)

示例

创建数据

```
CREATE
  (florentin:Person { name: 'Florentin', age: 16 }),
  (adam:Person { name: 'Adam', age: 18 }),
  (veselin:Person { name: 'Veselin', age: 20 }),
  (florentin)-[:KNOWS { since: 2010 }]->(adam),
  (florentin)-[:KNOWS { since: 2018 }]->(veselin)
```

![image-20231105144150085](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105144150085.png)

投影

```
CALL gds.graph.project('personsNative', 'Person', 'KNOWS')
//参数一：图形名称
//参数二：节点类别
//参数三：关系类别
```

继续

```
MATCH (n:Person)
OPTIONAL MATCH (n)-[r:KNOWS]->(m:Person)
RETURN gds.graph.project('personsCypher', n, m,
  {
    sourceNodeLabels: labels(n),
    targetNodeLabels: labels(m),
    relationshipType: type(r)
  }
)
```

继续

```
CALL gds.graph.project(
  'personsWithAgeNative',
  {
    Person: {properties: 'age'}
  },
  'KNOWS'
)
```

列出列表中的所有信息

```
CALL gds.graph.list()
YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount
ORDER BY graphName ASC
```

![image-20231105144740385](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105144740385.png)

列出目录中名为 graph 的特定 Cypher 的扩展信息：

```
CALL gds.graph.list('personsCypher')
YIELD graphName, configuration, schemaWithOrientation
RETURN graphName, configuration.query AS query, schemaWithOrientation
```

![image-20231105145009363](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105145009363.png)

列出有关特定图形的度分布的信息：

```
CALL gds.graph.list('personsNative')
YIELD graphName, degreeDistribution;
```

![image-20231105145202076](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105145202076.png)



#### 检查图形是否存在

语法

```
CALL gds.graph.exists(graphName: String) YIELD
  graphName: String,
  exists: Boolean
  
  //或者
  
  RETURN gds.graph.exists(graphName: String)::Boolean
```

示例

创建数据

```
CREATE
  (florentin:Person { name: 'Florentin', age: 16 }),
  (adam:Person { name: 'Adam', age: 18 }),
  (veselin:Person { name: 'Veselin', age: 20 }),
  (florentin)-[:KNOWS { since: 2010 }]->(adam),
  (florentin)-[:KNOWS { since: 2018 }]->(veselin)
  
  
```

![image-20231105150146543](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105150146543.png)

投影

```
CALL gds.graph.project('persons', 'Person', 'KNOWS')
```

检查是否存在

```
UNWIND ['persons', 'books'] AS graph
CALL gds.graph.exists(graph)
  YIELD graphName, exists
RETURN graphName, exists
```

![image-20231105150231682](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105150231682.png)

#### 删除图形

```
CALL gds.graph.drop(
  graphName: String,
  failIfMissing: Boolean,
  dbName: String,
  username: String
) YIELD
  graphName: String,
  database: String,
  configuration: Map,
  nodeCount: Integer,
  relationshipCount: Integer,
  schema: Map,
  schemaWithOrientation: Map,
  density: Float,
  creationTime: Datetime,
  modificationTime: Datetime,
  sizeInBytes: Integer,
  memoryUsage: String
  
  //实践
  call gds.graph.drop('graph')
```

![image-20231105150431035](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105150431035.png)

删除图形部分

```
CALL gds.graph.nodeProperties.drop(
    graphName: String,
    nodeProperties: String or List of Strings,
    configuration: Map
)
YIELD
    propertiesRemoved: Integer,
    graphName: String,
    nodeProperties: String or List of String
    

    
CALL gds.graph.relationships.drop(
    graphName: String,
    relationshipType: String
)
YIELD
  graphName: String,
  relationshipType: String,
  deletedRelationships: Integer,
  deletedProperties: Map
```



#### 查找节点属性

1语法

1.1查单个属性

```
CALL gds.graph.nodeProperty.stream(
    graphName: String,
    nodeProperties: String,
    nodeLabels: String or List of Strings,
    configuration: Map
)
YIELD
    nodeId: Integer,
    propertyValue: Integer or Float or List of Integer or List of Float,
    nodeLabels: List of Strings
```

![image-20231105161537980](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161537980.png)

![image-20231105161547807](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161547807.png)

![image-20231105161557810](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161557810.png)

1.2:检查多个

```
CALL gds.graph.nodeProperties.stream(
    graphName: String,
    nodeProperties: String or List of Strings,
    nodeLabels: String or List of Strings,
    configuration: Map
)
YIELD
    nodeId: Integer,
    nodeProperty: String,
    propertyValue: Integer or Float or List of Integer or List of Float,
    nodeLabels: List of Strings
```

![image-20231105161822928](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161822928.png)

![image-20231105161833039](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161833039.png)

![image-20231105161838485](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161838485.png)



2示例

创建

```
CREATE
  (florentin:Person { name: 'Florentin', age: 16 }),
  (adam:Person { name: 'Adam', age: 18 }),
  (veselin:Person { name: 'Veselin', age: 20 }),
  (hobbit:Book { name: 'The Hobbit', numberOfPages: 310 }),
  (florentin)-[:KNOWS { since: 2010 }]->(adam),
  (florentin)-[:KNOWS { since: 2018 }]->(veselin),
  (adam)-[:READ]->(hobbit)
 
```

![image-20231105161940758](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105161940758.png)

投影

```
CALL gds.graph.project(
  'socialGraph',
  {
    Person: {properties: "age"},
    Book: {}
  },
  ['KNOWS', 'READ']
)
```

计算社交图谱的度中心性

```
CALL gds.degree.mutate('socialGraph', {mutateProperty: 'score'})
```

2.1单一属性：所有节点的score属性

```
CALL gds.graph.nodeProperty.stream('socialGraph', 'score')
YIELD nodeId, propertyValue
RETURN gds.util.asNode(nodeId).name AS name, propertyValue AS score
ORDER BY score DESC
```

![image-20231105162333583](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105162333583.png)

 2.2节点标签

流式传输节点的属性：person节点的score属性

```
CALL gds.graph.nodeProperty.stream('socialGraph', 'score', ['Person'])
YIELD nodeId, propertyValue
RETURN gds.util.asNode(nodeId).name AS name, propertyValue AS score
ORDER BY score DESC
```

![image-20231105164946467](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105164946467.png)

person节点的score和age属性

```
CALL gds.graph.nodeProperties.stream('socialGraph', ['score', 'age'])
YIELD nodeId, nodeProperty, propertyValue
RETURN gds.util.asNode(nodeId).name AS name, nodeProperty, propertyValue
ORDER BY name, nodeProperty
```

![image-20231105165250634](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105165250634.png)

所有节点的名称、属性名称、属性值和节点标签

```
CALL gds.graph.nodeProperties.stream(
  'socialGraph',
  ['score'],
  ['*'],
  { listNodeLabels: true }
)
YIELD nodeId, nodeProperty, propertyValue, nodeLabels
RETURN
  gds.util.asNode(nodeId).name AS name,
  nodeProperty,
  propertyValue,
  nodeLabels
```

![image-20231105165406525](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105165406525.png)

3访问特定节点的属性值

```
gds.util.nodeProperty(
  graphName: String,
  nodeId: Node or Integer,
  propertyKey: String,
  nodeLabel: String
)
```

![image-20231105165600658](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105165600658.png)

示例

访问 Florentin 的属性节点属性：

```
MATCH (florentin:Person {name: 'Florentin'})
RETURN
  florentin.name AS name,
  gds.util.nodeProperty('socialGraph', florentin, 'score') AS score
```

![image-20231105165647377](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105165647377.png)

***



#### 查找关系属性

1获取指定类型的关系流

```
CALL gds.graph.relationships.stream(
    graphName: String,
    relationshipTypes: List of Strings,
    configuration: Map
)
YIELD
    sourceNodeId: Integer,
    targetNodeId: Integer,
    relationshipType: String
```

![image-20231105170054779](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105170054779.png)

2获取指定类型的关系的属性流

```
CALL gds.graph.relationshipProperty.stream(
    graphName: String,
    relationshipProperty: String,
    relationshipTypes: List of Strings,
    configuration: Map
)
YIELD
    sourceNodeId: Integer,
    targetNodeId: Integer,
    relationshipType: String,
    propertyValue: Integer or Float
```

![image-20231105170452564](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105170452564.png)

3获取指定类型的关系的多个属性流

```
CALL gds.graph.relationshipProperties.stream(
    graphName: String,
    relationshipProperties: List of String,
    relationshipTypes: List of Strings,
    configuration: Map
)
YIELD
    sourceNodeId: Integer,
    targetNodeId: Integer,
    relationshipType: String,
    relationshipProperty: String,
    propertyValue: Integer or Float
```

![image-20231105170600685](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105170600685.png)

#### 写回neo4j

写入节点属性

```
CALL gds.graph.nodeProperties.write(
    graphName: String,
    nodeProperties: String or Map of Strings or List of Strings and/or Maps of Strings,
    nodeLabels: String or List of Strings,
    configuration: Map
)
YIELD
    writeMillis: Integer,
    propertiesWritten: Integer,
    graphName: String,
    nodeProperties: String or List of String
```

写入节点标签

```
CALL gds.graph.nodeLabel.write(
    graphName: String,
    nodeLabel: String,
    configuration: Map
)
YIELD
    writeMillis: Integer,
    nodeLabelsWritten: Integer,
    nodeLabel: String,
    graphName: String,
    nodeCount: Integer,
    configuration: Map
```

写入一个关系

```
CALL gds.graph.relationship.write(
    graphName: String,
    relationshipType: String,
    relationshipProperty: String,
    configuration: Map
)
YIELD
  writeMillis: Integer,
  graphName: String,
  relationshipType: String,
  relationshipsWritten: Integer,
  relationshipProperty: String,
  propertiesWritten: Integer
```

写入多个关系

```
CALL gds.graph.relationshipProperties.write(
    graphName: String,
    relationshipType: String,
    relationshipProperties: List of String,
    configuration: Map
)
YIELD
  writeMillis: Integer,
  graphName: String,
  relationshipType: String,
  relationshipsWritten: Integer,
  relationshipProperties: List of String,
  propertiesWritten: Integer
```

#### 导出图形

导出到neo4j

```
CALL gds.graph.export(graphName: String, configuration: Map)
YIELD
    dbName: String,
    graphName: String,
    nodeCount: Integer,
    nodePropertyCount: Integer,
    relationshipCount: Integer,
    relationshipTypeCount: Integer,
    relationshipPropertyCount: Integer,
    writeMillis: Integer
```

导出到csv

```
CALL gds.graph.export.csv(graphName: String, configuration: Map)
YIELD
    graphName: String,
    exportName: String,
    nodeCount: Integer,
    nodePropertyCount: Integer,
    relationshipCount: Integer,
    relationshipTypeCount: Integer,
    relationshipPropertyCount: Integer,
    writeMillis: Integer
```

***



### 4图形算法

#### 4.1中心性

```
中心性算法可以对该系统有以下用处：

评估专家的重要程度：中心性算法可以衡量专家在整个网络中的重要程度或者在特定社区中的重要程度。通过计算专家的中心性指标，可以评估其在项目评审中的影响力和权威性。

识别关键专家：中心性算法可以识别出网络中最重要的专家，即关键专家。关键专家在评审过程中具有很高的影响力和决策权，其意见和评估结果可能会对项目决策产生重要影响。因此，通过中心性算法，可以找到适合担任项目评委的关键专家。

优化评委选择：通过中心性算法，可以根据专家的中心性指标，选择那些在整个网络或特定社区中具有较高中心性的专家作为评委。这可以确保选择的评委具有更大的影响力和权威性，可以提供更有效和准确的评审结果。

管理专家资源：中心性算法可以帮助管理专家资源，确保优质的专家被充分利用和调度。通过识别关键专家和社区中的中心性专家，系统可以更好地分配评委任务，使得评审流程更加高效和公正。

综上所述，中心性算法可以帮助评估专家的重要程度、识别关键专家、优化评委选择以及管理专家资源。通过运用中心性算法，系统可以选择具有更大影响力和权威性的评委，并确保评审过程的高效和公正。
```



##### PageRank算法

PageRank算法是图算法中的一种重要算法，用于评估网络图中节点的重要性。它最初由Google创始人之一拉里·佩奇（Larry Page）提出，被广泛应用于网页排名和网络分析等领域。

PageRank算法的核心思想是通过分析节点之间的链接关系，计算每个节点的权重值。具体来说，它将节点视为一个图，并将每个链接看作是图中的一条边。节点的权重在网页排名中表示其重要性。

stream

```
CALL gds.articleRank.stream(
  graphName: String,
  configuration: Map
)
YIELD
  nodeId: Integer,
  score: Float
 
//实践
call gds.pageRank.stream('graph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
```

stats

```
CALL gds.articleRank.stats(
  graphName: String,
  configuration: Map
)
YIELD
  ranIterations: Integer,
  didConverge: Boolean,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  centralityDistribution: Map,
  configuration: Map
```

mutate

```
CALL gds.articleRank.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  nodePropertiesWritten: Integer,
  ranIterations: Integer,
  didConverge: Boolean,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  mutateMillis: Integer,
  centralityDistribution: Map,
  configuration: Map
```

write

```
CALL gds.articleRank.write(
  graphName: String,
  configuration: Map
)
YIELD
  nodePropertiesWritten: Integer,
  ranIterations: Integer,
  didConverge: Boolean,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  writeMillis: Integer,
  centralityDistribution: Map,
  configuration: Map
```

配置

![image-20231105213551087](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105213551087.png)



加权：

默认情况下，该算法认为图形的关系是未加权的。 要更改此行为，我们可以使用配置参数。 如果设置了该参数，则关联的属性值将用作关系权重。 在这种情况下，发送到其邻居的节点的先前分数乘以归一化关系权重。 请注意，负关系权重在计算过程中被忽略。`relationshipWeightProperty``weighted`

在以下示例中，我们使用输入图的属性作为关系权重属性。`weight`

```
CALL gds.articleRank.stream('myGraph', {
  relationshipWeightProperty: 'weight'
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
```



公差

配置参数表示迭代之间分数的最小变化。 如果所有分数的变化都小于配置的容差，则迭代将中止并被视为收敛。 请注意，设置较高的容差会导致更早的收敛，但也会导致中心性分数的准确性降低。`tolerance`

```
CALL gds.articleRank.stream('myGraph', {
  tolerance: 0.1
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
```



个性化文章排名

个性化文章排名是文章排名的一种变体，它偏向于一组 . 默认情况下，电源迭代从所有节点的相同值开始：。 对于一组给定的源节点，对于所有剩余节点，每个源节点的初始值设置为 和 to。`sourceNodes``1 / |V|``S``1 / |S|``0`

以下示例说明如何运行以“站点 A”和“站点 B”为中心的特征向量中心性。

```
MATCH (siteA:Page {name: 'Site A'}), (siteB:Page {name: 'Site B'})
CALL gds.articleRank.stream('myGraph', {
  maxIterations: 20,
  sourceNodes: [siteA, siteB]
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
```



缩放中心性分数

要在算法执行过程中对最终分数进行归一化，可以使用配置参数。 可以在 [`scaleProperties`](https://neo4j.com/docs/graph-data-science/current/machine-learning/pre-processing/scale-properties/) 过程的文档中找到所有可用缩放器的说明。`scaler`

```
CALL gds.articleRank.stream('myGraph', {
  scaler: "StdScore"
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
```





##### 中介中心性算法

介绍

中介中心性是一种检测节点对图中信息流的影响量的方法。 它通常用于查找充当从图形的一部分到另一部分的桥梁的节点。

该算法计算图形中所有节点对之间的最短路径。 每个节点都会根据通过节点的最短路径数获得一个分数。 更频繁地位于其他节点之间的最短路径上的节点将具有更高的中介中心性分数。

中介中心性是为没有权重或具有正权重的图实现的。 GDS 实施基于[布兰德斯近似算法](https://www.uni-konstanz.de/mmsp/pubsys/publishedFiles/BrPi07.pdf)对于未加权的图形。 对于加权图，使用多个并发 [Dijkstra 算法](https://neo4j.com/docs/graph-data-science/current/algorithms/dijkstra-single-source/)。 该实现需要 *O（n +* m） 空间，并在 *O（n \* m）* 时间内运行，其中 *n* 是图中的节点数，*m* 是关系数。



注意事项和抽样

中介中心性算法的计算可能非常耗费资源。[布兰德斯近似算法](https://www.uni-konstanz.de/mmsp/pubsys/publishedFiles/BrPi07.pdf)计算一组源节点的单源最短路径 （SSSP）。 当所有节点都被选为源节点时，该算法将生成确切的结果。 但是，对于大型图形，这可能会导致运行时间过长。 因此，通过仅计算节点子集的 SSSP 来近似结果可能很有用。 在GDS中，我们将这种技术称为采样，其中源节点集的大小是*采样大小*。

在大型图形上执行算法时，需要考虑两件事：

- 更高的并行度会导致更高的内存消耗，因为每个线程按顺序为源节点的子集执行 SSSP。
  - 在最坏的情况下，单个 SSSP 需要在内存中复制整个图形。
- 更高的采样量会带来更准确的结果，但也可能导致更长的执行时间。

分别更改配置参数 和 的值有助于管理这些注意事项。`concurrency``samplingSize`



stream

```
CALL gds.betweenness.stream(
  graphName: String,
  configuration: Map
)
YIELD
  nodeId: Integer,
  score: Float
```

status

```
CALL gds.betweenness.stats(
  graphName: String,
  configuration: Map
)
YIELD
  centralityDistribution: Map,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  configuration: Map
```

mutate

```
CALL gds.betweenness.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  centralityDistribution: Map,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  mutateMillis: Integer,
  nodePropertiesWritten: Integer,
  configuration: Map
```

write

```
CALL gds.betweenness.write(
  graphName: String,
  configuration: Map
)
YIELD
  centralityDistribution: Map,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  writeMillis: Integer,
  nodePropertiesWritten: Integer,
  configuration: Map
```

配置

![image-20231105220146766](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105220146766.png)



##### 亲近中心性算法

介绍

亲近中心性（Closeness Centrality）是一种用于衡量图中节点在网络中的“中心性”程度的指标。该指标用于衡量节点与其他节点之间的距离，以及节点在信息传播、资源流动等方面的影响能力。

亲近中心性算法的计算是基于节点到其他节点的最短路径的平均距离。节点的亲近中心性值越高，表示该节点离其他节点的距离越近，信息能够更快地在网络中传播，节点具有更高的影响力。

亲近中心性算法在社交网络中具有以下应用和用途：

1. 识别网络中的关键节点：亲近中心性算法可以帮助识别网络中具有较高中心性的节点，这些节点在信息传播、资源分配等方面起着重要的作用。通过识别关键节点，可以更好地理解网络的结构和功能。
2. 预测信息传播路径：通过计算节点的亲近中心性，可以预测信息在网络中的传播路径。具有高亲近中心性的节点更有可能成为信息传播的关键节点，从而指导信息传播策略的制定。
3. 优化资源分配：在资源有限的情况下，通过计算亲近中心性，可以确定资源分配的优先级。具有高亲近中心性的节点更需要优先分配资源，以提高整个网络的效率和性能。
4. 建立社群发现算法的基础：亲近中心性是许多社群发现算法的基础之一。通过节点之间的亲近中心性，可以帮助划分社群，并理解网络中节点的聚集程度。

总之，亲近中心性算法在图算法中用于衡量节点在网络中的中心性，可应用于关键节点识别、信息传播预测、资源分配优化等方面，为社交网络分析和应用提供了有力的工具和指标。



适用情景

- 亲密中心性用于研究组织网络，其中具有高度接近中心性的个人处于有利地位，可以控制和获取组织内的重要信息和资源。 其中一项研究是[“绘制恐怖组织网络图”](http://www.orgnet.com/MappingTerroristNetworks.pdf)瓦尔迪斯·克雷布斯 （Valdis E. Krebs） 着。
- 接近中心性可以解释为信息流经电信或包裹递送网络的估计到达时间，其中信息通过最短路径流向预定义的目标。 它还可用于信息同时通过所有最短路径传播的网络，例如通过社交网络传播的感染。 查找更多详细信息[“中心性和网络流”](http://www.analytictech.com/borgatti/papers/centflow.pdf)斯蒂芬·博尔加蒂 （Stephen P. Borgatti）。
- 基于基于图形的关键词提取过程，接近中心性已用于估计文档中单词的重要性。 弗洛里安·布丁 （Florian Boudin） 在[“基于图的关键词提取的中心性度量比较”](https://www.aclweb.org/anthology/I/I13/I13-1102.pdf).

非适用情景

- 从学术上讲，接近中心性在连接图上效果最好。 如果我们在未连接的图上使用原始公式，我们最终可能会在单独的连接组件中的两个节点之间产生无限距离。 这意味着，当我们将与该节点的所有距离相加时，我们最终会得到一个无限接近的中心性分数。



stream

```
CALL gds.closeness.stream(
  graphName: String,
  configuration: Map
)
YIELD
  nodeId: Integer,
  score: Float
```

stats

```
CALL gds.closeness.stats(
  graphName: String,
  configuration: Map
)
YIELD
  centralityDistribution: Map,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  preProcessingMillis: Integer,
  configuration: Map
```

mutate

```
CALL gds.closeness.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  nodePropertiesWritten: Integer,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  mutateMillis: Integer,
  centralityDistribution: Map,
  configuration: Map
```

write

```
CALL gds.closeness.write(
  graphName: String,
  configuration: Map
)
YIELD
  nodePropertiesWritten: Integer,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  writeMillis: Integer,
  centralityDistribution: Map,
  configuration: Map
```

配置

![image-20231105221632375](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105221632375.png)



##### 度中心性算法

度中心性算法可用于查找图中的热门节点。 度中心性衡量来自节点的传入或传出（或两者）关系的数量，具体取决于关系投影的方向。 有关关系方向的详细信息，请参阅[关系投影语法部分](https://neo4j.com/docs/graph-data-science/current/management-ops/graph-creation/graph-project/#relationship-projection-syntax)。

它可以应用于加权或未加权图形。 在加权情况下，该算法计算图中每个节点的相邻关系的所有正权重之和。 非正权重将被忽略。

它可以应用于异构图，但该算法不会计算每种关系类型的度中心性。相反，它会将图形视为同质的，如算法特征所示。

有关此算法的详细信息，请参阅：

- [Linton C. Freeman：《社交网络中的中心性概念澄清》，1979 年。](https://www.cin.ufpe.br/~rbcp/taia/Freeman1979-centrality.pdf)



适用场景

度中心性算法已被证明在许多不同的应用中都很有用。 例如：

- 度中心性是任何试图确定社交网络中最重要的人的重要组成部分。 例如，在 BrandWatch 的[2017 年 Twitter 上最具影响力的男性和女性](https://www.brandwatch.com/blog/react-influential-men-and-women-2017/)每个类别的前 5 名每个人都有超过 40 万粉丝，这比平均水平高得多。
- 加权度中心性已被用于帮助将欺诈者与在线拍卖的合法用户区分开来。 欺诈者的加权中心性要高得多，因为他们倾向于相互串通，人为地提高商品价格。 阅读更多内容[基于图的两步半监督学习在线拍卖欺诈检测](https://link.springer.com/chapter/10.1007/978-3-319-23461-8_11)



stream

```
CALL gds.degree.stream(
  graphName: String,
  configuration: Map
) YIELD
  nodeId: Integer,
  score: Float
```

stats

```
CALL gds.degree.stats(
  graphName: String,
  configuration: Map
) YIELD
  centralityDistribution: Map,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  configuration: Map
```

mutate

```
CALL gds.degree.mutate(
  graphName: String,
  configuration: Map
) YIELD
  centralityDistribution: Map,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  mutateMillis: Integer,
  nodePropertiesWritten: Integer,
  configuration: Map
```

write

```
CALL gds.degree.write(
  graphName: String,
  configuration: Map
) YIELD
  centralityDistribution: Map,
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  writeMillis: Integer,
  nodePropertiesWritten: Integer,
  configuration: Map
```

配置

![image-20231105222433222](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231105222433222.png)

***



#### 4.2社区检测

```
在给项目申请者推荐专家作为项目评委的系统中，采用图算法的社区检测算法可以有以下用处：

识别专家社区：社区检测算法可以根据专家之间的关联关系，将他们划分为不同的社区。这有助于发现具有相似研究兴趣、相似背景或相似专业领域的专家群体。

寻找潜在评委：社区检测算法可以将专家划分为不同的社区，从而识别出一些在相关领域具有潜力的专家。这些专家可能是新兴领域的专家，或者是在该领域内不太活跃但有潜力的专家。通过识别这些潜在评委，可以为项目申请者提供更多选择。

促进专家交流：社区检测算法可以将相似领域或兴趣的专家划分到同一社区中。这可以促进专家之间的交流与合作，在评审过程中提供更深入的专业讨论和评估。

降低冲突和偏见：社区检测算法可以将拥有相似观点和背景的专家划分到同一社区中。通过避免让相互之间存在潜在冲突或偏见的专家同时参与评审，可以提高评审的客观性和公正性。

综上所述，采用图算法的社区检测算法可以帮助项目申请者推荐合适的专家评委，促进专家之间的交流合作，降低冲突和偏见，并识别出一些潜在的评委人选。这可以提高评审的效率和质量，为项目申请者提供更好的支持和指导。
```



##### 电导度量

[电导](https://en.wikipedia.org/wiki/Conductance_(graph))是一个指标，可用于评估社区检测的质量。 社区中节点的关系连接到内部或外部的节点。 电导是指向外部的关系与 的关系总数之比。 电导越低，社区就越“团结”。`C``C``C``C``C`

Yang 和 Leskovec 在论文*“Defining and Evaluating Network Communities based on Ground-truth”*中表明，电导是评估真实世界图的实际社区的一个非常好的指标。

该算法在时间上与图中的关系数量成线性关系。

stream

```
CALL gds.conductance.stream(
  graphName: String,
  configuration: Map
) YIELD
  community: Integer,
  conductance: Float
```

配置

![image-20231106213959838](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231106213959838.png)



##### k-means聚类

K-Means 聚类是一种无监督学习算法，用于解决聚类问题。 它遵循一个简单的过程，即将给定的数据集分类为多个聚类，由参数定义。 Neo4j GDS 库基于节点属性进行聚类，通过参数将浮点数组节点属性作为输入传递。 然后，图中的节点被定位为一维空间中的点（其中是数组属性的长度）。`k``nodeProperty``d``d`

然后，该算法首先选择初始聚类质心，即 -dimensional 数组（有关详细信息，请参阅[下文部分](https://neo4j.com/docs/graph-data-science/current/algorithms/kmeans/#algorithms-kmeans-sampling)）。 质心充当聚类的代表。`k``d`

然后，图中的所有节点计算它们与每个聚类质心的欧几里得距离，并被分配给与它们最小距离的聚类。 完成这些赋值后，每个聚类取分配给它的所有节点（作为点）的平均值，以形成其新的代表性质心（作为一维数组）。`d`

该过程使用新的质心重复，直到结果稳定，即每次迭代只有少数节点更改集群或达到最大迭代次数。

**请注意，K-Means 实现忽略了关系，因为它只关注节点属性。**

有关此算法的详细信息，请参阅：

- https://en.wikipedia.org/wiki/K-means_clustering

**为了使 K-Means 正常工作，所有节点的属性数组必须具有相同数量的元素。此外，它们应仅包含数字，而不包含任何 NaN 值。**

stream

```
CALL gds.kmeans.stream(
  graphName: String,
  configuration: Map
)
YIELD
  nodeId: Integer,
  communityId: Integer,
  distanceFromCentroid: Float,
  silhouette: Float
```

status

```
CALL gds.kmeans.stats(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  communityDistribution: Map,
  centroids: List of List of Float,
  averageDistanceToCentroid: Float,
  averageSilhouette: Float,
  configuration: Map
```

mutatu

```
CALL gds.kmeans.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  mutateMillis: Integer,
  postProcessingMillis: Integer,
  nodePropertiesWritten: Integer,
  communityDistribution: Map,
  centroids: List of List of Float,
  averageDistanceToCentroid: Float,
  averageSilhouette: Float,
  configuration: Map
```

write

```
CALL gds.kmeans.write(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  writeMillis: Integer,
  postProcessingMillis: Integer,
  nodePropertiesWritten: Integer,
  communityDistribution: Map,
  centroids: List of List of Float,
  averageDistanceToCentroid: Float,
  averageSilhouette: Float,
  configuration: Map
```

配置

![image-20231106215413520](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231106215413520.png)



##### 标签传播算法

标签传播算法 （LPA） 是一种用于在图中查找社区的快速算法。 它仅使用网络结构作为指导来检测这些社区，并且不需要预定义的目标函数或有关社区的先验信息。

LPA的工作原理是在整个网络中传播标签，并基于这种标签传播过程形成社区。

该算法背后的直觉是，单个标签可以迅速在密集连接的节点组中占据主导地位，但很难穿过稀疏连接的区域。 标签将被困在密集连接的节点组中，当算法完成时，那些最终具有相同标签的节点可以被视为同一社区的一部分。

该算法的工作原理如下：

- 每个节点都使用唯一的社区标签（标识符）进行初始化。
- 这些标签通过网络传播。
- 在每次传播迭代中，每个节点都会将其标签更新为其邻居的最大数量所属的标签。 纽带是任意但确定地打破的。
- 当每个节点都具有其邻居的多数标签时，LPA 达到收敛。
- 如果达到收敛或用户定义的最大迭代次数，则 LPA 将停止。

随着标签的传播，密集连接的节点组会迅速就唯一标签达成共识。 在传播结束时，只剩下少数标签 - 大多数标签将消失。 在收敛时具有相同社区标签的节点被称为属于同一社区。

LPA 的一个有趣功能是，可以为节点分配初步标签，以缩小生成的解决方案的范围。 这意味着它可以用作寻找社区的半监督方式，我们在其中手动挑选一些初始社区。

有关此算法的详细信息，请参阅：

- [“近线性时间算法检测大规模网络中的群落结构”](https://arxiv.org/pdf/0709.2938.pdf)
- 使用案例：
  - [Twitter 极性分类，通过词法链接和追随者图进行标签传播](https://dl.acm.org/citation.cfm?id=2140465)
  - [基于临床副作用的药物间相互作用标签传播预测](https://www.nature.com/articles/srep12339)
  - [“基于DST维基数据图上标签传播的特征推断”](https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.iwsds2017/papers/IWSDS2017_paper_12.pdf)

stream

```
CALL gds.labelPropagation.stream(
  graphName: String,
  configuration: Map
)
YIELD
    nodeId: Integer,
    communityId: Integer
```

stats

```
CALL gds.labelPropagation.stats(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  communityCount: Integer,
  ranIterations: Integer,
  didConverge: Boolean,
  communityDistribution: Map,
  configuration: Map
```

mutate

```
CALL gds.labelPropagation.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  mutateMillis: Integer,
  postProcessingMillis: Integer,
  nodePropertiesWritten: Integer,
  communityCount: Integer,
  ranIterations: Integer,
  didConverge: Boolean,
  communityDistribution: Map,
  configuration: Map
```

write

```
CALL gds.labelPropagation.write(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  writeMillis: Integer,
  postProcessingMillis: Integer,
  nodePropertiesWritten: Integer,
  communityCount: Integer,
  ranIterations: Integer,
  didConverge: Boolean,
  communityDistribution: Map,
  configuration: Map
```

配置

![image-20231106215747554](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231106215747554.png)

***



#### 4.3相似

##### 节点相似性

节点相似性算法根据一组节点所连接的节点来比较这些节点。 如果两个节点共享许多相同的邻居，则认为它们相似。 节点相似性根据 Jaccard 指标（也称为 Jaccard 相似性分数）或重叠系数（也称为 Szymkiewicz-Simpson 系数）计算成对相似性。

stream

```
CALL gds.nodeSimilarity.stream(
  graphName: String,
  configuration: Map
) YIELD
  node1: Integer,
  node2: Integer,
  similarity: Float
```

stats

```
CALL gds.nodeSimilarity.stats(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  postProcessingMillis: Integer,
  nodesCompared: Integer,
  similarityPairs: Integer,
  similarityDistribution: Map,
  configuration: Map
```

mutate

```
CALL gds.nodeSimilarity.mutate(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  mutateMillis: Integer,
  postProcessingMillis: Integer,
  relationshipsWritten: Integer,
  nodesCompared: Integer,
  similarityDistribution: Map,
  configuration: Map
```

write

```
CALL gds.nodeSimilarity.write(
  graphName: String,
  configuration: Map
)
YIELD
  preProcessingMillis: Integer,
  computeMillis: Integer,
  writeMillis: Integer,
  postProcessingMillis: Integer,
  nodesCompared: Integer,
  relationshipsWritten: Integer,
  similarityDistribution: Map,
  configuration: Map
```

配置

![image-20231108211818946](C:\Users\杨轩宇\AppData\Roaming\Typora\typora-user-images\image-20231108211818946.png)

