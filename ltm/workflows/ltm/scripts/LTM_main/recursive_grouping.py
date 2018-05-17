import networkx as nx
import numpy as np




class Vertex:
    def __init__(self, vid):
        self.vid = vid
        self.children = list()
        
    def add_child(self, child):
        self.children.append(child)

class Partition:
    def __init__(self):
        self.children = list()
        self.parent = None
        
    def set_parent(self, parent):
        self.parent = parent
        
    def add_child(self, child):
        self.children.append(child)
        
    def has_parent(self):
        return self.parent is not None
    
    def is_sibling_group(self):
        return len(self.children) > 1
   
def get_vids(vertices):
    vids = list()
    for vertex in vertices:   
        vids.append(vertex.vid)
    return vids

# Creates a Vertex object for each vertex id
# Returns a dictionary from vertex id to Vertex object
def build_vertices(vertex_ids):
    V = list()
    for vid in vertex_ids:
        V.append(Vertex(vid))
        
    # Load vertices into a dictionary according to vertex id
    V_dict = dict()
    for vertex in V:
        V_dict[vertex.vid] = vertex
        
    return V_dict


# *** RECURSIVE GROUPING LOGIC ***

# D - a dictionary from a pair of vertex ids to the distance between them
# vertex_ids - the ids of the vertices to group
# max_observed_vid - the highest observed vertex id
# new_vid - id to give the first new node
# MODIFIES D and V
def recursive_grouping(D,vertex_ids,max_observed_vid,new_vid,tau = float("inf"),epsilon = None):
    
    V = build_vertices(vertex_ids)
                
    # Kick off recursive grouping
    vertices = recursive_grouping_sub([V[x] for x in vertex_ids],D,V,max_observed_vid,new_vid,tau,epsilon)
    
    # Convert to Graph
    G = nx.DiGraph()
    for vertex in vertices:
        G.add_node(vertex.vid)
        for child in vertex.children:
            G.add_edge(vertex.vid,child)
    
    return G
    
# Y - active set of vertices to group (subset of V.values())
# D - a dictionary from a pair of vertex ids to the distance between them
# V - a dictionary from vertex id to vertex object
# max_observed_vid - the highest observed vertex id
# new_vid - id to give the first new node
# MODIFIES D and V
def recursive_grouping_sub(Y,D,V,max_observed_vid,new_vid,tau,epsilon):
    
    # Compute phi
    phi = get_phi(Y,D,V,tau)
        
    # Get the partitions
    if epsilon is None:
        partitions = get_partitions(Y,D,phi)
    else:
        partitions = get_partitions_relaxed(Y,D,V,max_observed_vid,phi,epsilon)
        
    # Construct the new active set
    Y_new = list()
    Y_leftover = list(Y)
    next_vid = new_vid
    new_nodes = list()
    for partition in partitions:
        
        # Add nodes with no parent or siblings to Y_new
        if not partition.has_parent() and not partition.is_sibling_group():
            Y_new.append(V[partition.children[0]])
            Y_leftover.remove(V[partition.children[0]])
        
        # Create new edges between parent node and its children
        # Add parent node to Y_new
        elif partition.has_parent():
            for child in partition.children:
                V[partition.parent].add_child(child)
            Y_new.append(V[partition.parent])
            Y_leftover.remove(V[partition.parent])
        
        # If this is a sibling group with no parent, make a new vertex h to be the parent
        # Create new edges between h and its children
        # Add h to Y_new and new_nodes
        else:      
            h = Vertex(next_vid)
            for child in partition.children:
                h.add_child(child)
            V[next_vid] = h
            Y_new.append(h)
            new_nodes.append(h)
            next_vid += 1
                        
    # Compute the distance from each new node h to each other node and add to dictionary       
    if epsilon is None:
        set_new_distances(D,V,Y_new,new_vid,phi)
    else:
        set_new_distances_relaxed(D,V,new_nodes,new_vid,phi)
                
    # Return results          
    if len(Y_new) == 1:
        return (Y_leftover + Y_new)
    elif len(Y_new) == 2:
        if Y_new[1].vid > Y_new[0].vid:
            Y_new[1].add_child(Y_new[0].vid)
        else:
            Y_new[0].add_child(Y_new[1].vid)
        return (Y_leftover + Y_new)
    else:
        return (Y_leftover +  recursive_grouping_sub(Y_new,D,V,max_observed_vid,next_vid,tau,epsilon))
    
# Compute phi (as in Choi et al)
# Uses adaptive thresholding on tau
def get_phi(Y,D,V,tau):
    
    phi = dict()
    vids = get_vids(Y)
    
    for i in vids:
        for j in vids:
            if j == i:
                continue                   
            # Require at least three entries in phi for each i,j
            # If there are too few, relax the threshold and try again
            threshold = tau
            phi_count = 0
            while phi_count < min(3,len(V)-2):        
                for k in V:
                    if k == i or k == j:
                        continue
                    if D[(i,k)] < threshold and D[(j,k)] < threshold and (i,j,k) not in phi:
                        phi[(i,j,k)] = D[(i,k)] - D[(j,k)]
                        phi_count += 1
                threshold += 0.1 * tau
    return phi


# *** RELAXED PARTITIONING ***

# Y - vertices to partition
# D - a dictionary from a pair of vertex ids to the distance between them
# V - a dictionary from vertex id to vertex object
# max_observed_vid - the highest observed vertex id
# phi - a dictionary from a triplet of vertices i,j,k to D[(i,k)] - D[(j,k)]
# epsilon - a parameter used to distinguish parent-child from sibling relationships
# RELAXED version
def get_partitions_relaxed(Y,D,V,max_observed_vid,phi,epsilon):
    
    np.set_printoptions(precision=3)

    Y_vids = get_vids(Y)
    phi_ranges = np.empty((len(Y),len(Y))) # as in Matlab code
    phi_ranges[:] = float('inf')
    phi_means = dict()
    index_vid = dict()
    
    # Compute phi mean and phi range for each i,j
    i_index = 0 
    for i in Y_vids:
        index_vid[i_index] = i
        j_index = i_index+1
        for j in Y_vids[j_index:]:
            phis = list()
            for k in V:
                if k == i or k == j or (i,j,k) not in phi:
                    continue
                phis.append(phi[(i,j,k)])
            if len(phis) == 0:
                i = 2      
            phi_ranges[i_index,j_index] = max(phis) - min(phis)
            phi_means[(i,j)] = sum(phis) / float(len(phis))
            phi_means[(j,i)] = -phi_means[(i,j)]
                       
            j_index += 1
        i_index += 1
        
    # Get families by clustering 
    families = k_means_cluster(np.minimum(phi_ranges,np.transpose(phi_ranges))) # as in Matlab code
    
    # Replace indices with actual vertex ids
    for family in families:
        for i in range(len(family)):
            family[i] = index_vid[family[i]]
    
    # Build partitions
    return families_to_partitions(families, D, epsilon, phi_means, max_observed_vid)

# Build partitions from a list of families
def families_to_partitions(families, D, epsilon, phi_means, max_observed_vid):
    
    partitions = list()
    
    # Create a partition for each family
    # Check for parent-child relationships within family and update partition accordingly   
    for family in families:
        partition = Partition()
        
        # First, see if the family contains a hidden node
        contains_hidden = False
        for k in family:
            if k > max_observed_vid:
                contains_hidden = True
                break
        
        # Identify the parent in the family (if there is one)
        # Method was reverse engineered from the Matlab code
        min_parent_score = epsilon * (len(family)-1)
        for k in family: 
            # An observed node cannot be the parent if the family contains a hidden node
            if contains_hidden and k <= max_observed_vid:
                partition.add_child(k)
            else:
                parent_score = 0           
                for i in family:
                    if i != k:       
                        parent_score += abs(phi_means[(k,i)] + D[(k,i)])
                if parent_score < min_parent_score:
                    if partition.has_parent():
                        partition.add_child(partition.parent)
                    partition.set_parent(k)
                    min_parent_score = parent_score
                else:
                    partition.add_child(k)
                                      
        partitions.append(partition)
                                     
    return partitions

# Cluster nodes into families using k-means
# Translated more or less exactly from crummy Matlab code
def k_means_cluster(phi_ranges):
    
    m = phi_ranges.shape[0]
    best_clusters = list()
    
    D = np.matrix(phi_ranges)
    
    # START BOGUS
    minD = D.min(axis = 0)
    thing = minD.tolist()[0]
    minD_indices = [i[0] for i in sorted(enumerate(thing), key=lambda x:x[1], reverse = True)]
    # END BOGUS
    
    for i in range(m):
        D[i,i] = 0     
    max_mean_silh = -float('inf')
     
    # Try different numbers of clusters
    for k in range(2,max(m-1,3)):
        
        # Try five different initial center sets (I made some adjustments here to make the process smarter)
        # Select the first center for each of the five sets
#         np.random.seed(50)
#         initial_centers = np.random.permutation(m-1)[0:5]        
#         for initial_center in initial_centers:
#             centers = list()
#             centers.append(initial_center)
#             
#             # Iteratively add center that is least similar to the other centers
#             for count in range (0,k-1):
#                 mean_diffs = [(val,idx) for (idx,val) in enumerate(np.mean(phi_ranges[:,centers],1))]
#                 eligible_mean_diffs = [diff for diff in mean_diffs if diff[1] not in centers]
#                 val, idx = max(eligible_mean_diffs)
#                 centers.append(idx)
#      
#             prev_centers = list(centers)
#             clusters = list()

        # START TEMPORARY BOGUS
        
        for ite in range(1,4):
            centers = list()
            if ite == 1:
                for i in (range(0,k-1) + [len(minD_indices)-1]):
                    centers.append(i)
            elif ite == 2:
                for i in range(0,k):
                    centers.append(i)
            else:
                for i in np.random.permutation(m-1)[0:k]:
                    centers.append(i)
            
            prev_centers = list(centers)
            clusters = list()
            
        # END TEMPORARY BOGUS
            
            # Try adjusting initial center points until they don't change     
            while True:
                clusters = [[center] for center in centers]
                noncenters = set(range(0,m)).difference(set(centers))
                
                # Assign each non-center to a cluster
                for i in noncenters:
                    idx = np.argmin(D[i,centers])
                    clusters[idx].append(i)
                    
                # Pick a new center for each cluster
                clust_index = 0
                for cluster in clusters:
                    minmaxD = float('inf')
                    for member in cluster:
                        maxD = np.max(D[member,cluster])
                        if maxD < minmaxD:
                            minmaxD = maxD
                            center = member
                    centers[clust_index] = center
                    clust_index += 1
                if not set(centers).difference(set(prev_centers)):
                    break
                else:
                    prev_centers = list(centers)
                    
            mean_silh = compSilhouette(D,clusters)
            
            if mean_silh > max_mean_silh:
                max_mean_silh = mean_silh
                best_clusters = clusters
        
    return best_clusters
        
# Compute mean silhouette for the members of the clusters
def compSilhouette(D,clusters): 
    k = len(clusters)
    meanDcluster = dict()
    maxDcluster = dict()
    clust_indices = range(0,k)
    for clust_index in range(len(clusters)):
        meanDcluster[clust_index] = np.mean(D[:,clusters[clust_index]],1)
        maxDcluster[clust_index] = np.max((D[clusters[clust_index],:])[:,clust_index])
        
    maxa = max(maxDcluster.values())
    silh = list()
    for clust_index in range(len(clusters)):
        numMembers = len(clusters[clust_index])
        for member in clusters[clust_index]:
            if numMembers > 1:
                a = meanDcluster[clust_index][member]
            else:
                a = maxa
            b = np.min([meanDcluster[this_clust_index][member] for this_clust_index in set(clust_indices).difference(set([clust_index]))])
            denom = max(a,b) if max(a,b) > 0 else 1
            silh.append((b-a) / float(denom))
            
    return np.mean(silh)
                        
# Compute the distance from each new node h to each other node and add to dictionary
# MODIFIES D
# RELAXED version
def set_new_distances_relaxed(D,V,new_nodes,new_vid,phi):
    
    # For each new node h...
    for h in new_nodes:            
        # Load ih into dictionary
        for i in h.children:
            # Question: Recursive grouping doesn't require d_ih beyond the scope of this function, so why not save it in a local container instead of D?
            # Answer: Because CLGrouping (which uses recursive grouping) may need d_ih
            # This is a tacky but necessary side-effect
            D[(i,h.vid)] = get_d_ih_relaxed(i,h,V,D,phi)
            D[(h.vid,i)] = D[(i,h.vid)]
                               
        # For each other node l...
        for l in V.values():
            if l.vid != h.vid and l.vid not in h.children:
                if l.vid < new_vid:
                    i_sum = 0
                    for i in h.children:
                        d_ih = D[(i,h.vid)]
                        i_sum += D[(i,l.vid)] - d_ih
                    D[(h.vid,l.vid)] = i_sum / len(h.children)
                    D[(l.vid,h.vid)] = i_sum / len(h.children)
                else:                
                    # Load jl into dictionary
                    for j in l.children:
                        if (j,l) not in D:
                            D[(j,l.vid)] = get_d_ih_relaxed(j,l,V,D,phi)
                            D[(l.vid,j)] = D[(j,l.vid)]
                            
                    i_j_sum = 0
                    for i in h.children:
                        d_ih = D[(i,h.vid)]
                        for j in l.children:
                            d_jl = D[(j,l.vid)]
                            i_j_sum += D[(i,j)] - d_ih - d_jl        
                    D[(h.vid,l.vid)] = i_j_sum / (len(h.children) * len(l.children))
                    D[(l.vid,h.vid)] = i_j_sum / (len(h.children) * len(l.children))
    
# Compute d_ih (as in Choi et al)
# RELAXED version               
def get_d_ih_relaxed(i,h,V,D,phi):
    j_sum = 0
    k_sum = 0
    k_count = 0
    for j in h.children:
        if j == i:
            continue
        j_sum += D[(i,j)]
        for vertex in V.values():
            if vertex.vid == i or vertex.vid == j or (i,j,vertex.vid) not in phi:
                continue
            k_sum += phi[(i,j,vertex.vid)]   
            k_count += 1
    d_ih_nom = j_sum + k_sum / k_count
    d_ih_denom = 2 * (len(h.children) - 1)
    return d_ih_nom / d_ih_denom


# *** REGULAR PARTITIONING ***

# Y - vertices to partition
# D - a dictionary from a pair of vertex ids to the distance between them
# phi - a dictionary from a triplet of vertices i,j,k to D[(i,k)] - D[(j,k)]
# REGULAR version
def get_partitions(Y,D,phi):
    partitions = list()
    node_partition = dict()
    Y_vids = get_vids(Y)
    
    i_index = 0
    for i in Y_vids:
        for j in Y_vids[i_index+1:]:
            
            parent_child_candidate = True
            child_parent_candidate = True
            sibling_group_candidate = True
            
            # Check for relationship between pair
            for k in Y_vids:
                if k == i or k == j:
                    continue;
                if phi[(i,j,k)] != D[(i,j)]:
                    child_parent_candidate = False
                if phi[(i,j,k)] != -D[(i,j)]:
                    parent_child_candidate = False
                
                if sibling_group_candidate:
                    for k_prime in Y_vids:
                        if k_prime == i or k_prime == j or k_prime == k:
                            continue
                        if phi[(i,j,k)] != phi[(i,j,k_prime)] or phi[(i,j,k)] <= -D[(i,j)] or phi[(i,j,k)] >= D[(i,j)]:
                            sibling_group_candidate = False
                            break
                            
                if not child_parent_candidate and not parent_child_candidate and not sibling_group_candidate:
                    break
            
            # Update partition (or make a new one) accordingly        
            if parent_child_candidate:
                parent_part = node_partition.get(i)
                child_part = node_partition.get(j)
                if parent_part is None or child_part is None:
                    if parent_part is not None:
                        partitions[parent_part].add_child(j)
                        node_partition[j] = parent_part
                    elif child_part is not None:
                        partitions[child_part].set_parent(i)
                        node_partition[i] = child_part
                    else:
                        partition = Partition()
                        partition.set_parent(i)
                        partition.add_child(j)       
                        partitions.append(partition)
                        node_partition[j] = len(partitions) - 1
                        node_partition[i] = len(partitions) - 1
                
            elif child_parent_candidate:
                parent_part = node_partition.get(j)
                child_part = node_partition.get(i)
                if parent_part is None or child_part is None:
                    if parent_part is not None:
                        partitions[parent_part].add_child(i)
                        node_partition[i] = parent_part
                    elif child_part is not None:
                        partitions[child_part].set_parent(j)
                        node_partition[j] = child_part
                    else:
                        partition = Partition()
                        partition.set_parent(j)
                        partition.add_child(i)       
                        partitions.append(partition)
                        node_partition[i] = len(partitions) - 1
                        node_partition[j] = len(partitions) - 1              
            
            elif sibling_group_candidate:
                sib1_part = node_partition.get(i)
                sib2_part = node_partition.get(j)
                if sib1_part is None or sib2_part is None:
                    if sib1_part is not None:
                        partitions[sib1_part].add_child(j)
                        node_partition[j] = sib1_part
                    elif sib2_part is not None:
                        partitions[sib2_part].add_child(i)
                        node_partition[i] = sib2_part
                    else:
                        partition = Partition()
                        partition.add_child(i)
                        partition.add_child(j)     
                        partitions.append(partition)
                        node_partition[i] = len(partitions) - 1
                        node_partition[j] = len(partitions) - 1
                    
        if node_partition.get(i) is None:
            partition = Partition()
            partition.add_child(i) 
            partitions.append(partition)
            node_partition[i] = len(partitions) - 1
        
        i_index += 1
                             
    return partitions
    
# Compute the distance from each new node h to each other node in Y_new and add to dictionary
# MODIFIES D
# REGULAR version
def set_new_distances(D,Y,Y_new,new_vid,phi):
    for h in Y_new:
        if h.vid >= new_vid:
            i = h.children[0]
            d_ih = get_d_ih(h,Y,D,phi)
            for l in Y_new:
                if l.vid != h.vid:
                    if l.vid < new_vid:
                        D[(h.vid,l.vid)] = D[(i,l.vid)] - d_ih
                        D[(l.vid,h.vid)] = D[(i,l.vid)] - d_ih
                    else:
                        k = l.children[0]
                        d_kl = get_d_ih(l,Y,D,phi)        
                        D[(h.vid,l.vid)] = D[(i,k)] - d_ih - d_kl
                        D[(l.vid,h.vid)] = D[(i,k)] - d_ih - d_kl
                        
# Compute d_ih (as in Choi et al)
# REGULAR version              
def get_d_ih(h,Y,D,phi):
    i = h.children[0]
    j = h.children[1]
    k = i
    for vertex in Y:
        if vertex.vid == i or vertex.vid == j:
            continue
        k = vertex.vid
        break
    return 0.5 * (D[(i,j)] + phi[(i,j,k)])




