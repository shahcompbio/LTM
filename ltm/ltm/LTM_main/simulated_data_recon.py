import cell_data_generator as cdg
import genotype_ltm_generator as glg
import tree_reconstruct as tr
import sys
import networkx as nx
import itertools
from munkres import Munkres
from collections import OrderedDict
import timeit


class Result:
    def __init__(self, data_settings, recon_settings, sibling_sensitivity, sibling_precision, ancestor_sensitivity, ancestor_precision, recon_accuracy, recon_run_time, score_run_time):
        self.data_settings = data_settings
        self.recon_settings = recon_settings
        self.sibling_sensitivity = sibling_sensitivity
        self.sibling_precision = sibling_precision
        self.ancestor_sensitivity = ancestor_sensitivity
        self.ancestor_precision = ancestor_precision
        self.recon_accuracy = recon_accuracy
        self.recon_run_time = recon_run_time
        self.score_run_time = score_run_time
        
    def get_print_str(self):
        return str(self.recon_settings.method) + '\t' + str(self.recon_settings.tau) + '\t' + str(self.recon_settings.epsilon) + '\t' + str(self.data_settings.seed) + '\t' + " ".join(self.data_settings.alphabet) + '\t' + str(self.data_settings.num_nodes) + '\t' + str(self.data_settings.num_positions) + '\t' + str(self.data_settings.percent_asym) + '\t' + str(self.data_settings.mutation_rate) + '\t' + str(self.data_settings.percent_observed) + '\t' + str(self.sibling_sensitivity) + '\t' + str(self.sibling_precision) + '\t' + str(self.ancestor_sensitivity) + '\t' + str(self.ancestor_precision) + '\t' + str(self.recon_accuracy) + '\t' + str(self.recon_run_time) + '\t' + str(self.score_run_time) + '\n'

def package_result(data_settings, recon_settings, original_tree, observed_vertices, result):
    
    result_tree = result[0]
    recon_run_time = result[1]
    
    # Score
    start = timeit.default_timer()
    
    matching = get_maximum_matching_weight(original_tree, result_tree, observed_vertices)
    weight = matching[0]
    Pr = matching[1]
    Pi = matching[2]
    denom = len(observed_vertices) * (Pr + Pi) - weight # metric from Chowdury et al.
    recon_accuracy = weight / float(denom)
    
    # Calculate percent recovery of sibling relationships between observed vertices
    sibling_pairs_original = get_sibling_pairs(original_tree, observed_vertices)
    sibling_pairs_result = get_sibling_pairs(result_tree, observed_vertices)
    sibling_intersection = set(sibling_pairs_original).intersection(sibling_pairs_result)
    sibling_sensitivity = len(sibling_intersection) / float(len(sibling_pairs_original)) if len(sibling_pairs_original) > 0 else None
    sibling_precision = len(sibling_intersection) / float(len(sibling_pairs_result)) if len(sibling_pairs_result) > 0 else None
    
    # Calculate percent recovery of ancestral relationships between observed vertices
    ancestral_pairs_original = get_ancestral_pairs(original_tree, observed_vertices)
    ancestral_pairs_result = get_ancestral_pairs(result_tree, observed_vertices)
    ancestral_intersection = set(ancestral_pairs_original).intersection(ancestral_pairs_result)
    ancestor_sensitivity = len(ancestral_intersection) / float(len(ancestral_pairs_original)) if len(ancestral_pairs_original) > 0 else None
    ancestor_precision = len(ancestral_intersection) / float(len(ancestral_pairs_result)) if len(ancestral_pairs_result) > 0 else None
    
    stop = timeit.default_timer()
    score_run_time = stop - start
        
    return Result(data_settings, recon_settings, sibling_sensitivity, sibling_precision, ancestor_sensitivity, ancestor_precision, recon_accuracy, recon_run_time, score_run_time)
    
    
def get_maximum_matching_weight(tree1, tree2, observed_vertices):
       
    edges1 = tree1.edges()
    edges2 = tree2.edges()
    
    # Build matrix of weights in bipartite graph
    matrix = list()
    for edge1 in edges1:
        if len(tree1.succ[edge1[1]]) > 0:
            row = list()
            for edge2 in edges2:
                if len(tree2.succ[edge2[1]]) > 0:
                    row.append(calculate_edge_weight(tree1, tree2, edge1, edge2, observed_vertices))
            matrix.append(row)
            
    # Transform the matrix into a cost matrix by negating
    inverse_matrix = list()
    for row in matrix:
        inverse_row = list()
        for cell in row:
            inverse_row.append(-cell)
        inverse_matrix.append(inverse_row)
    
    # Get maximum matching    
    m = Munkres()
    indices = m.compute(inverse_matrix)
    
    # Calculate weight of maximum matching
    total = 0
    for row, column in indices:
        value = matrix[row][column]
        total += value
        
    return (total, len(matrix), len(matrix[0]))
            
def calculate_edge_weight(tree1, tree2, edge1, edge2, observed_vertices):
    
    # Get bipartitions for each tree
    child1 = edge1[1]
    tree1_partA = (nx.descendants(tree1,child1).union(set([child1]))).intersection(observed_vertices)
    
    child2 = edge2[1]
    tree2_partA = (nx.descendants(tree2,child2).union(set([child2]))).intersection(observed_vertices)
    
    # Assign vertices to partitions
    tree1_assignments = OrderedDict((vertex,0) for vertex in observed_vertices)
    tree2_assignments = OrderedDict((vertex,0) for vertex in observed_vertices)
    
    for vertex in tree1_partA:
        tree1_assignments[vertex] = 1
        
    for vertex in tree2_partA:
        tree2_assignments[vertex] = 1
        
    s1 = "".join(map(str, tree1_assignments.values()))
    s2 = "".join(map(str, tree2_assignments.values()))
    s2_alt = ((s2.replace('1', '2')).replace('0', '1')).replace('2', '0')
    
    return max(invhamdist(s1, s2), invhamdist(s1, s2_alt))

def invhamdist(str1, str2):
    matches = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 == ch2:
            matches += 1
    return matches

# Get all edges involving the specified vertices exclusively
def get_edges(tree, vertices):
    edges = list()
    for edge in tree.edges():
        if edge[0] in vertices and edge[1] in vertices:
            edges.append(edge)
    return edges

# Get all sibling pairs involving the specified vertices exclusively
def get_sibling_pairs(tree, vertices):
    sibling_pairs = list()
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if len(tree.pred[vertices[i]].keys()) > 0 and len(tree.pred[vertices[j]].keys()) > 0 and tree.pred[vertices[i]].keys()[0] == tree.pred[vertices[j]].keys()[0]:
                sibling_pairs.append((vertices[i],vertices[j]))
    return sibling_pairs
        
# Get all ancestral pairs involving the specified vertices exclusively
def get_ancestral_pairs(tree, vertices):
    ancestral_pairs = list()
    for v1 in vertices:
        for v2 in vertices:
            if v1 in nx.ancestors(tree, v2):
                ancestral_pairs.append((v1,v2))
    return ancestral_pairs

# *** MAIN ***

if __name__=='__main__':
    
    my_seeds = range(3)
    #my_alphabets = [['0','1'], ['A','B','C']]
    my_alphabets = [['0','1']]
    #my_num_samples = [100, 300, 1000, 3000, 10000]
    my_num_samples = [100] 
    #my_num_nodes = [7,15,31,63,127,256]
    my_num_nodes = [127,256,512,1024]
    #my_percent_asymmetric = [0,10,20,60,70]
    my_percent_asymmetric = [60]
    #my_mutation_rates = [2,5,10,20,25]   
    my_mutation_rates = [10] # can't get any higher than 20
    #my_methods = [Recon_Method.RECURSIVE_GROUPING, Recon_Method.CHOW_LIU_GROUPING]
    my_methods = [tr.Recon_Method.CHOW_LIU_GROUPING]
    #my_taus = [0.6,0.8,1,2,3,5,100]
    my_taus = [2] # sensitive to number of nodes (sort of)
    #my_epsilons = [0.04,0.06,0.08,0.1,0.2,0.3,0.5]
    my_epsilons = [0.3] # sensitive to mutation rate
    #my_tree_types = [cdg.TreeType.BALANCED]
    my_tree_types = [cdg.TreeType.BALANCED]
    #my_percent_observed = [20,40,60,80,100]
    my_percent_observed = [100]
    
    my_results = list()
    run_id = 0
    
    data_configs = list(itertools.product(*[my_seeds,my_alphabets,my_num_samples,my_num_nodes,my_methods,my_percent_asymmetric,my_mutation_rates,my_tree_types,my_percent_observed]))
    
    for data_config in data_configs:
        seed = data_config[0]
        alphabet = data_config[1]
        num_samples = data_config[2]
        num_nodes = data_config[3]
        method = data_config[4]
        percent_asymmetric = data_config[5]
        mutation_rate = data_config[6]
        tree_type = data_config[7]
        percent_observed = data_config[8]
            
        # Generate data
        data_settings = cdg.Data_Settings(seed, alphabet, num_nodes, num_samples, percent_asymmetric, mutation_rate, tree_type, percent_observed)
        data = cdg.generate_cell_data(data_settings)
        tree = data[0]
        position_data = data[1]
        cell_data = data[2]               
        
        # Save data to file
        #cdg.save_cell_data(cell_data, "celldat" + str(run_id))
        #cdg.save_tree(tree, "original_tree" + str(run_id))
        
        # Convert to Genotype LTM
        ltm = glg.get_genotype_ltm(tree, min(tree.node.keys()))
        #nx.write_gml(ltm, "original_ltm" + str(run_id) + ".gml")
                                  
        for tau in my_taus:
            for epsilon in my_epsilons:
                
                # Reconstruct tree
                recon_settings = tr.Recon_Settings(method, tau, epsilon)
                result = tr.reconstruct(recon_settings, position_data, cell_data, data_settings.alphabet)
                my_results.append(package_result(data_settings, recon_settings, ltm, cell_data.keys(), result))
                #nx.write_gml(result[0], "result_ltm" + str(run_id) + ".gml")  
                run_id +=1
                                                            
                    
    # Record all results 
    file_name = sys.argv[1]
    f = open(file_name,'w')
    f.write("method\ttau\tepsilon\tseed\talphabet\tnum_nodes\tnum_positions\tpercent_asym\tmutation_rate\tpercent_observed\tsibling_sensitivity\tsibling_precision\tancestor_sensitivity\tancestor_precision\trecon_accuracy\trecon_run_time\tscore_run_time\n")
    
    if (my_results is not None):
        for result in my_results:
            f.write(result.get_print_str())
    
    f.close()
