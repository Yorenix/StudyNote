import networkx as nx
import matplotlib.pyplot as plt

"""
1. 构建用户-物品关系图：将用户和物品作为节点，用户对物品的行为（如购买、评分等）作为边连接用户和物品。
2. 计算用户之间的相似度：对于每对用户，计算它们之间共同拥有的邻居节点数量，即共同邻居的数量。共同邻居越多，说明两个用户在兴趣方面越相似。
3. 推荐物品给用户：对于目标用户，选择与其相似度最高的K个用户，找到这些用户拥有但目标用户没有行为的物品，将这些物品推荐给目标用户。
"""

# 生成空手道图
G = nx.karate_club_graph()

# 转换节点标签以便画图
labels = {}
for node in G.nodes():
    labels[node] = str(node)
nx.draw(G, labels=labels)
plt.show()

# 查找11号节点邻居
print(list(G.neighbors(11)))
# 查找33号节点的邻居
print(list(G.neighbors(33)))

# 查找0号节点和33号节点的共同邻居
print(list(nx.common_neighbors(G, 0, 33)))
