import networkx as nx
import matplotlib.pyplot as plt
import random

# 生成一个杠铃图，m1表示铃部节点数量，m2表示杠杆节点数量
G = nx.barbell_graph(5, 4)
# 图形可视化
nx.draw_networkx(G)
plt.show()


def random_walk(G, path_length, alpha, start=None):
    """
    实现一个截取随机游走
    G是我们要研究的图
    path_length：随机游走的长度
    alpha：每次游走从start点开始的概率
    start：随机游走的起始点
    """
    if start is None:
        # 如果没有设置起始点，那么我们就在图中随机选择一个
        # list(G.nodes):将获取杠铃图G的节点列表，并将其转换为一个可迭代对象的列表
        # random.sample()函数将从这个列表中随机选择一个节点
        # k=1表示要选择的节点数量为1
        path = random.sample(list(G.nodes), 1)
    else:
        path = [start]
    while len(path) < path_length:  # 如果没有到达我们需要的随机游走长度
        cur_node = path[-1]  # 下一轮随机游走的起点
        # G.adj[cur_node]用于获取图G中与当前节点(cur_node)相邻的节点（邻居节点）及其边，返回一个包含邻居节点的字典
        if len(list(G.adj[cur_node])) > 0:  # 如果这个“起点”还有相邻点的话
            if random.random() >= alpha:
                path.extend(
                    random.sample(list(G.adj[cur_node]), 1))
            else:  # 一定概率跳到起点
                path.append(path[0])
        else:
            break
    return path


print(random_walk(G, 10, 0.1))
# [3, 3, 4, 5, 6, 5, 4, 1, 3, 2]
