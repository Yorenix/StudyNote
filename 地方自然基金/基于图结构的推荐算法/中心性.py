import networkx as nx
import matplotlib.pyplot as plt


def degree_Centrality():
    """
    有向图！！！
    根据拥有的相邻节点的个数推荐重要节点
    """

    G = nx.gn_graph(8)

    print('度中心度:')
    # 计算度中心度
    res = nx.degree_centrality(G)
    # {'Acciaiuoli': 0.07142857142857142, 'Medici': 0.42857142857142855,
    # 'Castellani': 0.21428571428571427, 'Peruzzi': 0.21428571428571427,
    # 'Strozzi': 0.2857142857142857, 'Barbadori': 0.14285714285714285,
    # 'Ridolfi': 0.21428571428571427, 'Tornabuoni': 0.21428571428571427,
    # 'Albizzi': 0.21428571428571427, 'Salviati': 0.14285714285714285,
    # 'Pazzi': 0.07142857142857142, 'Bischeri': 0.21428571428571427,
    # 'Guadagni': 0.2857142857142857, 'Ginori': 0.07142857142857142,
    # 'Lamberteschi': 0.07142857142857142}
    result = sorted(res.items(), key=lambda val: val[1], reverse=True)
    print(result)

    # 计算入度中心度和出度中心度
    in_res = nx.in_degree_centrality(G)
    out_res = nx.out_degree_centrality(G)
    result1 = sorted(in_res.items(), key=lambda val: val[1], reverse=True)
    result2 = sorted(out_res.items(), key=lambda val: val[1], reverse=True)
    print(result1, '\n', result2)

    nx.draw_networkx(G)
    plt.show()


def between_Centrality():
    """
    有向图！！！
    介数中心度
    它衡量了一个节点在网络中连接其他节点最短路径的数量或权重之和，
    反映了节点在信息传递、影响传播等方面的重要性。
    """
    G = nx.gn_graph(8)

    print('介数中心度:')
    node_res = nx.betweenness_centrality(G)
    edge_res = nx.edge_betweenness_centrality(G)
    result1 = sorted(node_res.items(), key=lambda val: val[1], reverse=True)
    result2 = sorted(edge_res.items(), key=lambda val: val[1], reverse=True)
    print(result1)
    print(result2)

    nx.draw_networkx(G)
    plt.show()

def eigenvector_Centrality():
    """
    1 图特征向量中心度
    2 特征向量中心性的值越高，表示该节点在网络中的重要性越高。
      对于大图有一定计算开销
    3 在运算的时候容易报错
      因为模型无法在默认周期内收敛，默认max_iter=100，将该参数调大即可
    """
    G = nx.gn_graph(8)

    print('图特征向量中心度:')
    node_res = nx.eigenvector_centrality(G,max_iter=10000)
    result = sorted(node_res.items(), key=lambda val: val[1], reverse=True)
    print(result)

    nx.draw_networkx(G)
    plt.show()


"""
中心度的衡量还有很多，根据场景再做选择
"""

# degree_Centrality()
# between_Centrality()
eigenvector_Centrality()
