import chow_liu_trees as CLT
import recursive_grouping as rg
import networkx as nx


# MODIFIES D
def chow_liu_grouping(D,samples,vertex_ids,tau = float("inf"),epsilon = None):
    
    # Get the Chow Liu tree
    T = CLT.build_chow_liu_tree(samples,vertex_ids)
    
    # Identify the internal nodes
    internal_nodes = list()
    for node in T:
        if len(T.neighbors(node)) > 1:
            internal_nodes.append(node)
            
    # Perform recursive grouping on each internal node
    max_observed_vid = vertex_ids[-1] # Max id among observed vertices
    max_all_vid = max_observed_vid # Max id among all vertices
    for internal_node in internal_nodes:
           
        # Get neighbors of internal_node
        neighbors = T.neighbors(internal_node)
        
        # Compute any missing distances and add to D_new
        update_dictionary(D, neighbors, internal_node, max_observed_vid)
            
        # Remove edges inside neighborhood
        remove_edges(T, internal_node)
        
        # Perform recursive grouping on neighborhood
        graph_new = rg.recursive_grouping(D, (neighbors + [internal_node]), max_observed_vid, max_all_vid + 1, tau, epsilon)
        
        # Add new nodes and edges
        update_graph(T, graph_new, max_all_vid)
        
        # Update max_all_vid
        max_all_vid = sorted(T)[-1]
        
    return convert_to_directed(T)

# Computes missing distances within neighborhood and adds them to D (Choi et al pg 21)
# MODIFIES D        
def update_dictionary(D, nbd, internal_node, max_observed_vid):
    for neighbor1 in nbd:
        if neighbor1 > max_observed_vid:
            # Neighbor1 is a hidden node that was added in a previous iteration
            # Use the internal node to calculate distances
            for neighbor2 in nbd:
                if (neighbor1 != neighbor2):
                    D[(neighbor1,neighbor2)] = D[neighbor1,internal_node] + D[internal_node,neighbor2]
                    D[(neighbor2,neighbor1)] = D[(neighbor1,neighbor2)]

# Remove all edges involving node
# MODIFIES graph
def remove_edges(graph, node):
    for neighbor in graph.neighbors(node):
        graph.remove_edge(node,neighbor)

# Add new nodes and edges from new_graph to graph
# MODIFIES graph
def update_graph(graph, graph_new, max_all_vid):
    for node in graph_new:
        if node > max_all_vid:
            graph.add_node(node)
        for edge in graph_new.edge[node]:
            graph.add_edge(node,edge,parent = node)
            
def convert_to_directed(graph):
    di_graph = nx.DiGraph()
    for node in graph:
        di_graph.add_node(node)
    for edge in graph.edges():
        if graph[edge[0]][edge[1]]['parent'] == edge[0]:
            di_graph.add_edge(edge[0],edge[1])
        else:
            di_graph.add_edge(edge[1],edge[0])
    return di_graph
        
        
        
        
    
            