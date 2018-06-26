import networkx as nx
import random
import math
import Queue


# *** TREE STRUCTURE ***

# Defines the tree types (i.e. topologies) that this script can build
# All binary topologies unless otherwise specified
class TreeType:
    BALANCED = 1

# Function to build a tree given the number of nodes and a TreeType
def build_tree(ttype, num_nodes):
    
    if (ttype == TreeType.BALANCED):  
        return nx.bfs_tree(nx.balanced_tree(2, math.ceil(math.log(num_nodes+1,2)) - 1),0)
    

                
             
# *** TREE PARAMETERS ***

# Randomly selects a subset of nodes to be asymmetric
def set_asymmetry(tree, percent_asym):
    
    for node in tree.nodes():
        tree.node[node]['asym'] = False
        
    if (percent_asym > 0):
        
        # Create list of node_ids to sample asymmetric nodes from
        node_ids = list(tree.nodes())
        
        # Remove leaf nodes from sampling list
        for node in tree.nodes():
            if (len(tree.successors(node)) == 0):
                node_ids.remove(node)
                
        # How many asymmetric nodes?
        num_asym = int(round(len(node_ids) * (float(percent_asym) / 100)))
                
        # Select the asymmetric nodes
        asym_nodes = random.sample(node_ids,num_asym)
        for node in asym_nodes:
            tree.node[node]['asym'] = True    

# Observe a subset of leaves and prune the tree and dictionary accordingly
# MODIFIES tree and cell_data           
def observe_subset(tree, cell_data, percent_observed):
    
    # Select which leaf nodes are observed 
    leaves = get_leaves(tree)
    observed = dict.fromkeys(leaves, False)
    num_observed = int(round(len(leaves) * (float(percent_observed) / 100)))
    observed_leaves = random.sample(leaves,num_observed)
    for leaf in observed_leaves:
        observed[leaf] = True
    
    # Prune the tree
    leaf_parents = get_leaf_parents(tree)
    for parent in leaf_parents:
        grandparent = tree.pred[parent].keys()[0] if len(tree.pred[parent]) > 0 else None
        child1 = tree.succ[parent].keys()[0]
        child2 = tree.succ[parent].keys()[1]
        if not observed[child1] and not observed[child2]:
            cell_data.pop(child1)
            cell_data.pop(child2)
            tree.remove_node(parent)
            tree.remove_node(child1)
            tree.remove_node(child2)
            if not grandparent is None:  
                greatgrandparent = tree.pred[grandparent].keys()[0] if len(tree.pred[grandparent]) > 0 else None
                parent_sibling = tree.succ[grandparent].keys()[0]
                tree.remove_node(grandparent)
                if not greatgrandparent is None:
                    tree.add_edge(greatgrandparent, parent_sibling)
        elif not observed[child1] or not observed[child2]:
            observed_child = child1 if observed[child1] else child2
            unobserved_child = child1 if observed_child == child2 else child2
            cell_data.pop(unobserved_child)
            tree.remove_node(parent)
            tree.remove_node(unobserved_child)
            if not grandparent is None:
                tree.add_edge(grandparent,observed_child)
        
def get_leaves(tree):
    leaves = list()
    for node in tree:
        if len(tree.succ[node]) == 0:
            leaves.append(node)
    return leaves
    
def get_leaf_parents(tree):
    leaf_parents = list()
    for node in tree:
        if len(tree.succ[node]) > 0 and len(tree.succ[tree.succ[node].keys()[0]]) == 0:
            leaf_parents.append(node)
    return leaf_parents

# Randomly splits the probability space over an alphabet
def rand_dist(alphabet, mutation_rate = None, pred_val = None):
    
    dist = dict()
    upper_bound = 0
    alphabet_new = list(alphabet)
    
    if (not mutation_rate is None):
        upper_bound = 100-mutation_rate
        dist[pred_val] = float(upper_bound)/100.0
        alphabet_new.remove(pred_val)
    
    bounds = [random.randint(0,100-upper_bound) for r in range(len(alphabet_new)-1)]
    bounds.sort()
    bounds.append(100-upper_bound)
    bounds = [float(x)/100.0 for x in bounds]
    
    i = 0
    prevbound = 0
    for a in alphabet_new:
        dist[a] = bounds[i] - prevbound
        prevbound = bounds[i]
        i += 1     
    return dist

# Randomly splits the conditional probability space over an alphabet
def rand_cond_dist(alphabet, mutation_rate):
    cond_dist = dict()
    for a in alphabet:
        cond_dist[a] = rand_dist(alphabet, mutation_rate, a)
    return cond_dist
            

# *** DATA GENERATION ***

# Settings for data generation
# percent_asym is the percent of ELIGIBLE leaves that are asymmetric
class Data_Settings:
    def __init__(self, seed, alphabet, num_nodes, num_positions, percent_asym, mutation_rate, tree_type, percent_observed):
        self.seed = seed
        self.alphabet = alphabet
        self.num_nodes = num_nodes
        self.num_positions = num_positions
        self.percent_asym = percent_asym
        self.mutation_rate = mutation_rate
        self.tree_type = tree_type
        self.percent_observed = percent_observed
     
def generate_cell_data(data_settings):
    
    random.seed(data_settings.seed)
    
    # Construct the tree and the probabilities
    tree = build_tree(data_settings.tree_type, data_settings.num_nodes)
    set_asymmetry(tree, data_settings.percent_asym)
    tree.graph['dist'] = rand_dist(data_settings.alphabet)
    tree.graph['cond_dist'] = rand_cond_dist(data_settings.alphabet, data_settings.mutation_rate)
    
    # Get cell data
    cell_data = dict()
    root_seq = generate_root_sequence(tree, data_settings.num_positions, cell_data)
    generate_succ_sequences(tree, 0, root_seq, cell_data)
    
    # Observe a subset of leaves and prune the tree and dictionary accordingly
    observe_subset(tree, cell_data, data_settings.percent_observed)
    
    # Get data for each position (aka sample)
    samples = dict()
    for i in range(data_settings.num_positions):
        samples[i] = ([d[i] for d in cell_data.values()])
     
    return (tree,samples,cell_data)

# Generates a sequence for the root node
def generate_root_sequence(tree, num_positions, dictionary):
    root_seq = ""
    dist = tree.graph['dist']
    for i in range(num_positions):
        rand = random.random()
        cumprob = 0
        for key in dist:
            if rand < (cumprob + dist[key]):
                root_seq += key
                break    
            else:
                cumprob += dist[key]
    return root_seq
    
# Recursively generates sequences for node_id's successors
# Adds sequences for leaf nodes to dictionary
# MODIFIES dictionary
def generate_succ_sequences(tree, node_id, pred_seq, dictionary):
  
    # Record data for observed leaf nodes only
    if len(tree.succ[node_id]) == 0:
        dictionary[node_id] = pred_seq
    
    else:
        dist = tree.graph['dist']
        cond_dist = tree.graph['cond_dist']
        
        # Generate a copy of the sequence
        copy_seq = ""
        for i in range(len(pred_seq)):
            rand = random.random()
            cumprob = 0
            for key in dist:
                if rand < (cumprob + cond_dist[pred_seq[i]][key]):
                    copy_seq += key
                    break    
                else:
                    cumprob += cond_dist[pred_seq[i]][key]
                    
        # Set child sequences
        child1_seq = ""
        child2_seq = ""
        
        # Asymmetric case - all mutations go to one child
        if tree.node[node_id]['asym']:
            child1_seq = copy_seq
            child2_seq = pred_seq
            
        # Symmetric case - mutations get split up
        else:      
            for i in range(len(pred_seq)):
                rand = random.random()
                if (rand < 0.5):
                    child1_seq += pred_seq[i]
                    child2_seq += copy_seq[i]
                else:
                    child1_seq += copy_seq[i]
                    child2_seq += pred_seq[i]
            
        # Generate sequences for each of the children's descendants   
        
        # Two children
        if (len(tree.succ[node_id]) > 1):
            child1 = tree.succ[node_id].keys()[0]
            child2 = tree.succ[node_id].keys()[1]
            generate_succ_sequences(tree, child1, child1_seq, dictionary)   
            generate_succ_sequences(tree, child2, child2_seq,  dictionary)
            
        # Only one child - we need to randomly select one of the sequences to assign to it
        else: 
            child = tree.succ[node_id].keys()[0]
            rand = random.random()
            if rand < 0.5:
                child_seq = child1_seq
                tree.node[node_id]['child_identical'] = False
            else:
                child_seq = child2_seq
                tree.node[node_id]['child_identical'] = True
            generate_succ_sequences(tree, child, child_seq, dictionary)
    
    
# *** SAVE DATA ***

def save_tree(tree, file_name):
    
    g = tree.copy()
    g.graph['cond_dist'] = 1
    g.graph['dist'] = 1
    nx.write_gml(g, file_name + ".gml")
     
    f = open(file_name + ".tsv",'w')
     
    # Create header string
    header_string = "Node ID\tParent\tAsymmetric"
         
    # Get node strings
    node_string = get_node_string(tree, 0)
    f.write(header_string + "\n" + node_string)
     
    f.close()
    
# Gets string containing details of node_id its successors
def get_node_string(tree, node_id):
     
    parent_string = "NA" if node_id == 0 else str(tree.predecessors(node_id)[0])
    node_string = str(node_id) + "\t" + parent_string + "\t" + str(tree.node[node_id]['asym'])
             
    for succ in tree.succ[node_id]:
        node_string += "\n" + get_node_string(tree, succ)
     
    return node_string

def save_cell_data(cell_data, file_name):
     
    f = open(file_name + ".tsv",'w')
      
    for cell in cell_data:
        f.write(str(cell) + ":\t")
        for position in cell_data[cell]:
            f.write(str(position) + "\t")
        f.write("\n")
 
    f.close()


# *** DEPRECATED ***

# def save_tree(tree, file_name):
#     
#     f = open(file_name + ".tsv",'w')
#     
#     # Create header string
#     header_string = "Node ID\tParent\tLatent"
#     alphabet = tree.node[0]["marg_dist"].keys()
#     for a in alphabet:
#         for b in alphabet:
#             header_string += "\t" + b + "|" + a
#     for a in alphabet:
#         header_string += "\t" + a
#         
#     node_string = get_node_string(tree, 0, len(alphabet))
#     f.write(header_string + "\n" + node_string)
#     
#     f.close()
# 
# # Gets string containing details of node_id its successors
# def get_node_string(tree, node_id, alphabet_size):
#     
#     parent_string = "NA" if node_id == 0 else str(tree.predecessors(node_id)[0])
#     node_string = str(node_id) + "\t" + parent_string + "\t" + str(tree.node[node_id]['latent'])
#     
#     if (node_id != 0):
#         cond_dist = tree.node[node_id]['cond_dist']
#         for key in cond_dist:
#             this_dist = cond_dist[key]
#             for this_key in this_dist:
#                 node_string += "\t" + str(this_dist[this_key])
#     else:
#         for i in range(0,alphabet_size ** 2):
#             node_string += "\tNA"
#             
#     marg_dist = tree.node[node_id]['marg_dist']
#     for key in marg_dist:
#         node_string += "\t" + str(marg_dist[key])
#             
#     for succ in tree.succ[node_id]:
#         node_string += "\n" + get_node_string(tree, succ, alphabet_size)
#     
#     return node_string
#   

#     elif (ttype == TreeType.SPARSE):
#         G = nx.DiGraph()
#         node_queue = Queue.Queue()
#         G.add_node(0)
#         node_queue.put(0)
#         node_count = 1
#         while node_count < num_nodes:
#             
#             # If queue is empty and we still haven't met our quota, 
#             # add all leaves to queue and try again
#             if node_queue.empty():
#                 for node in G:
#                     if (len(G.succ[node]) == 0):
#                         node_queue.put(node)
#                         
#             current_node_id = node_queue.get()
#             
#             # Roll for first child
#             rand1 = random.random()
#             if (rand1 < density):
#                 node_count += 1
#                 child_id = node_count
#                 G.add_node(child_id)
#                 G.add_edge(current_node_id, child_id)
#                 node_queue.put(child_id)
#                 
#             # Roll for second child
#             rand2 = random.random()
#             if (rand2 < density and node_count < num_nodes):
#                 node_count += 1
#                 child_id = node_count
#                 G.add_node(child_id)
#                 G.add_edge(current_node_id, child_id)
#                 node_queue.put(child_id)
#                 
#         return G
#     
# def collapse_hidden_edges(G,node_id):
#     
#     children = G.succ[node_id].keys()
#     if (node_id > 0 and len(children) == 1):
#         if (len(G.succ[children[0]]) > 0):
#             parent = G.pred[node_id].keys()[0]
#             G.remove_edge(parent,node_id)
#             G.add_edge(parent,children[0])
#             G.remove_node(node_id)
#     for child in children:
#         collapse_hidden_edges(G,child)  