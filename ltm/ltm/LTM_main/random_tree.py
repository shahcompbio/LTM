import networkx as nx
import math
import random


# *** TREE STRUCTURE ***

# Defines the tree types (i.e. topologies) that this script can build
# All binary topologies unless otherwise specified
class TreeType:
    BALANCED = 1

# Function to build a tree given the number of nodes and a TreeType
def build_tree(ttype, num_nodes, percent_latent = 0):
    
    if (ttype == TreeType.BALANCED):  
        tree = nx.bfs_tree(nx.balanced_tree(2, math.ceil(math.log(num_nodes+1,2)) - 1),0)
        set_latency(tree, percent_latent)
        return tree

# Randomly selects a subset of nodes to be latent
def set_latency(tree, percent_latent):
    
    for node in tree.nodes():
        tree.node[node]['latent'] = False
        
    if (percent_latent > 0):
        
        # How many latent nodes?
        num_latent = int(round(len(tree.node) * (float(percent_latent) / 100)))
        
        # Create list of node_ids to sample latent nodes from
        node_ids = range(0,len(tree.node))
        
        # Remove nodes that cannot be latent nodes from sampling list (leaf nodes and nodes with < 3 neighbors)
        for node in tree.nodes():
            num_succs = len(tree.successors(node))
            num_preds = len(tree.predecessors(node))
            if (num_succs == 0 or num_succs + num_preds < 3):
                node_ids.remove(node)
                
        # Select the latent nodes
        latent_nodes = random.sample(node_ids,num_latent)
        for node in latent_nodes:
            tree.node[node]['latent'] = True


# *** TREE PARAMETERS ***
                  
# Recursively assigns probability distributions to node_id and its successors
# stay_rate - lower bound on the probability of keeping the same value between generations (e.g. 0|0)
def set_dists(tree, node_id, alphabet, stay_rate = None):
    if (node_id == 0): # Root node does not have a conditional distribution
        tree.node[node_id]['marg_dist'] = rand_dist(alphabet)
    else:     
        tree.node[node_id]['cond_dist'] = rand_cond_dist(alphabet, stay_rate)
        tree.node[node_id]['marg_dist'] = get_marginal_dist(tree, node_id, alphabet)
    for succ in tree.succ[node_id]:
        set_dists(tree, succ, alphabet, stay_rate)
        
# Randomly splits the probability space over an alphabet
def rand_dist(alphabet, stay_rate = None, pred_val = None):
    
    dist = dict()
    upper_bound = 0
    alphabet_new = list(alphabet)
    
    if (not stay_rate is None):
        upper_bound = random.randint(stay_rate,100)
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
def rand_cond_dist(alphabet, stay_rate):
    cond_dist = dict()
    for a in alphabet:
        cond_dist[a] = rand_dist(alphabet, stay_rate, a)
    return cond_dist
        
# Returns the marginal distribution for a node
# Assumes marginal distribution for predecessor has been calculated
def get_marginal_dist(tree, node_id, alphabet):
    marg_dist = dict()
    pred_id = tree.pred[node_id].keys()[0]
    pred_dist = tree.node[pred_id]['marg_dist']
    for a in alphabet:
        tot = 0
        for b in alphabet:
            tot += pred_dist[b] * tree.node[node_id]['cond_dist'][b][a]
        marg_dist[a] = tot
    return marg_dist
        
# Assign weights (based on mutual information) to edges
def set_weights(tree, alphabet):
    for edge in tree.edges():
        u = edge[0]
        v = edge[1]
        tree.edge[u][v]['weight'] = -mut_info(tree, alphabet, u, v)

# Compute mutual information for two nodes
# Assumes v is child of u
def mut_info(tree, alphabet, u, v):
    marg_dists_u = tree.node[u]['marg_dist']
    marg_dists_v = tree.node[v]['marg_dist']
    cond_dists_v = tree.node[v]['cond_dist']
    tot = 0
    for a in alphabet:            
        p_ua = marg_dists_u[a]
        for b in alphabet:
            p_vb = marg_dists_v[b]
            p_ua_vb = p_ua * cond_dists_v[a][b]
            if (p_ua > 0 and p_vb > 0 and p_ua_vb > 0):
                tot += p_ua_vb * math.log(p_ua_vb / (p_ua * p_vb))
    return tot
            
      
# *** SAMPLE FROM TREE ***

# Recursively samples from node_id and its successors
# At each node, symbol x is emitted with probability P( node_id = x | pred(node_id) = pred_val )
def sample_from_tree(tree, node_id, pred_val = None):
    samples = dict()
    if (node_id == 0):
        dists = tree.node[node_id]['marg_dist']
    else:
        dists = tree.node[node_id]['cond_dist'][pred_val]
    rand = random.random()
    cumprob = 0
    for key in dists:
        if rand < (cumprob + dists[key]):
            if (tree.node[node_id]['latent'] == False): # Record sampled value if node is not latent
                samples[node_id] = key
            for succ in tree.succ[node_id]:
                subs = sample_from_tree(tree, succ, key)
                samples.update(subs)
            break    
        else:
            cumprob += dists[key]
    return samples


