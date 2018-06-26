import networkx as nx

def get_genotype_ltm(cell_tree, root_id):
    
    # Build connected components graph
    CC_graph = nx.Graph()
    build_cc_graph(cell_tree, root_id, CC_graph)

    # Build Genotype graph
    genotype_Graph = nx.DiGraph()
    zero_len_connected_comp = nx.connected_components(CC_graph)
    cc_nodes_set = zero_len_node_finder(zero_len_connected_comp)
    G_leaves_it = (n for n,d in cell_tree.out_degree_iter() if d==0)
    G_leaves = list(G_leaves_it)
    for e in cell_tree.edges():
        mapped_tail = map_vertex(e[0],cc_nodes_set,zero_len_connected_comp,G_leaves,cell_tree)
        mapped_head = map_vertex(e[1],cc_nodes_set,zero_len_connected_comp,G_leaves,cell_tree)
        
        if mapped_tail != mapped_head:
            genotype_Graph.add_edge(mapped_tail, mapped_head)
    
    return genotype_Graph
    
# Recursively build connected component graph for node_id and its successors
# MODIFIES CC_graph 
def build_cc_graph(tree, node_id, CC_graph):
    
    if tree.node[node_id]['asym']:
        if len(tree.succ[node_id]) > 1: # Node is asymmetric and has two children - second child will be identical         
            CC_graph.add_edge(node_id,tree.succ[node_id].keys()[1])
        elif tree.node[node_id]['child_identical']: # Node is asymmetric and has one child - it may or may not be identical
            CC_graph.add_edge(node_id,tree.succ[node_id].keys()[0])
    for child in tree.succ[node_id]:
        build_cc_graph(tree, child, CC_graph)
 
    
# *** COPIED VERBATIM FROM HOSSEIN ***

# Maps a node to a connected component of the zero length edge graph
def map_vertex(node,cc_nodes_set,zero_len_connected_comp,G_leaves,G):
    
    if node not in cc_nodes_set:
        mapped_node=node   
    else:
        node_cc,leaves_in_component = node_connected_component_finder(zero_len_connected_comp,G_leaves,node)
        
        if len(leaves_in_component) == 1:
            mapped_node=list(leaves_in_component)[0]
        
        if len(leaves_in_component) == 0:
            mapped_node=min(node_cc)

        if len(leaves_in_component) > 1:
            if node not in leaves_in_component:
                if len(G.pred[min(node_cc)].keys())>0:
                    mapped_node=G.pred[min(node_cc)].keys()[0]
                else:
                    mapped_node=min(node_cc)
            else:
                mapped_node=node
    return mapped_node

# Gets all nodes that are part of a connected component
def zero_len_node_finder(CC_list):
    res_set=set([])
    for cc in CC_list:
        for v in cc:
            res_set.add(v)
    return res_set

# Returns the connected component of zero length edges that a node belongs to
def node_connected_component_finder(zero_len_connected_comp,G_leaves,node): 
    for c in zero_len_connected_comp:
        if node in c:
            ans=c
    leaves_in_component=set(ans).intersection(set(G_leaves))
    return ans,leaves_in_component
