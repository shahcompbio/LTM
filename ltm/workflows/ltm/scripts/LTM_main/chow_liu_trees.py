import numpy as N, networkx as nx
from collections import defaultdict



def marginal_distribution(X, u):
    """
    Return the marginal distribution for the u'th features of the data points, X.
    """
    values = defaultdict(float)
    s = 1. / len(X)
    for x in X:
        values[x[u]] += s
    return values



def marginal_pair_distribution(X, u, v):
    """
    Return the marginal distribution for the u'th and v'th features of the data points, X.
    """
    if u > v:
        u, v = v, u
    values = defaultdict(float)
    s = 1. / len(X)
    for x in X:
        values[(x[u], x[v])] += s
    return values



def calculate_mutual_information(X, u, v):
    """
    X are the data points.
    u and v are the indices of the features to calculate the mutual information for.
    """
    if u > v:
        u, v = v, u
    marginal_u = marginal_distribution(X, u)
    marginal_v = marginal_distribution(X, v)
    marginal_uv = marginal_pair_distribution(X, u, v)
    I = 0.
    for x_u, p_x_u in marginal_u.iteritems():
        for x_v, p_x_v in marginal_v.iteritems():
            if (x_u, x_v) in marginal_uv:
                p_x_uv = marginal_uv[(x_u, x_v)]
                I += p_x_uv * (N.log(p_x_uv) - N.log(p_x_u) - N.log(p_x_v))
    return I

# Emily introduced slight modifications here to handle node ids
def build_chow_liu_tree(X, node_ids):
    """
    Build a Chow-Liu tree from the data, X. n is the number of features. The weight on each edge is
    the negative of the mutual information between those features. The tree is returned as a networkx
    object.
    """
    G = nx.Graph()
    for i in range(len(node_ids)):
        G.add_node(node_ids[i])
        for j in range(i+1,len(node_ids)):
            G.add_edge(node_ids[i], node_ids[j], weight=-calculate_mutual_information(X, i, j))
    T = nx.minimum_spanning_tree(G)
    return T
            


if '__main__' == __name__:
    X = ['AACC','AAGC','AAGC','GCTC','ACCT']

    #print marginal_pair_distribution(X, 2, 3)
    print calculate_mutual_information(X, 2, 3)
#     import doctest
#     doctest.testmod()