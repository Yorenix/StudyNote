import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决中文乱码等问题


def Unweighted_graph():
    """无向无权图"""
    # 定义并画出无向图
    G = nx.path_graph(5)  # 5个节点，一条直线：0-1-2-3-4
    # 添加两条额外的路径
    nx.add_path(G, [0, 5, 2])
    nx.add_path(G, [0, 6, 4])
    plt.title('无向图')
    # 确保图形的坐标轴是打开状态，而不是被隐藏
    plt.axis('on')
    plt.xticks([])
    plt.yticks([])
    # 绘图，with_labels=True：显示标签
    nx.draw(G, with_labels=True)
    plt.show()

    # 计算最短路径
    print('0节点到4节点最短路径: ', nx.shortest_path(G, source=0, target=4))
    p1 = nx.shortest_path(G, source=0)
    print('0节点到所有节点最短路径: ', p1)

    # 计算最短路径长度
    p2 = nx.shortest_path_length(G, source=0, target=2)  # 最短路径长度
    p3 = nx.average_shortest_path_length(G)  # 计算平均最短路径长度
    print('节点0到节点2的最短路径长度:', p2, ' 平均最短路径长度: ', p3)

    # 检测是否有路径
    print('检测节点0到节点2是否有路径', nx.has_path(G, 0, 2))


def Weighted_graph():
    """有权图"""
    G = nx.path_graph(5, create_using=nx.DiGraph())
    plt.title('有向图')
    plt.axis('on')
    plt.xticks([])
    plt.yticks([])
    nx.draw(G, with_labels=True)
    plt.show()

    # 计算加权图最短路径长度和前驱
    # 计算完成后，函数返回两个字典对象：pred和dist。
    # 其中，pred字典存储了从节点0到其他节点的最短路径的前驱节点，dist字典存储了从节点0到其他节点的最短路径长度。
    pred, dist = nx.dijkstra_predecessor_and_distance(G, 0)
    print('\n加权图最短路径长度和前驱: ', pred, dist)

    # 返回G中从源到目标的最短加权路径,要求边权重必须为数值
    print('\nG中从源0到目标4的最短加权路径: ', nx.dijkstra_path(G, 0, 4))
    print('\nG中从源0到目标4的最短加权路径的长度: ', nx.dijkstra_path_length(G, 0, 4))  # 最短路径长度

    # 单源节点最短加权路径和长度。
    length1, path1 = nx.single_source_dijkstra(G, 0)
    print('\n单源节点最短加权路径和长度: ', length1, path1)

    # 下面两条和是前面的分解
    # path2=nx.single_source_dijkstra_path(G,0)
    # length2 = nx.single_source_dijkstra_path_length(G, 0)
    # print('\n', length1,'$', path1,'$',length2,'$',path2)

    # 多源节点最短加权路径和长度。
    path1 = nx.multi_source_dijkstra_path(G, {0, 4})
    length1 = nx.multi_source_dijkstra_path_length(G, {0, 4})
    print('\n多源节点最短加权路径和长度:', path1, length1)

    # 两两节点之间最短加权路径和长度。
    path1 = dict(nx.all_pairs_dijkstra_path(G))
    length1 = dict(nx.all_pairs_dijkstra_path_length(G))
    print('\n两两节点之间最短加权路径: ', path1)
    print('\n两两节点之间最短加权路径长度: ', length1)

    # 双向搜索的迪杰斯特拉
    length, path = nx.bidirectional_dijkstra(G, 0, 4)
    print('\n双向搜索的迪杰斯特拉:', length, path)


