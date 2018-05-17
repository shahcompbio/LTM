import cell_data_generator as cdg
import tree_reconstruct as tr
import package_result as pr
import graph_utils as gu
import sys
import networkx as nx
from Bio import Phylo


if __name__=='__main__':
    
#     f = open("out.txt",'w')
#     for i in range(1,300):
#         f.write("\texecute cell_dat" + str(i) + ".nex;\n")
#         f.write("\tmcmc;\n")
#         f.write("\tsumt conformat=simple;\n")
#     f.close()
    
    num_results = 240
    my_results = list()
    
    for n in range(num_results):
        
        # Read in original ltm
        ltm = nx.read_gml("mr_bayes/original_ltm" + str(n) + ".gml")
        mapping = dict()
        for node in ltm:
            mapping[node] = int(ltm.node[node]['label'])
        nx.relabel_nodes(ltm, mapping, copy = False)
        
        # Read in settings 
        f = open("mr_bayes/settings" + str(n) + ".txt",'r')
        buf = f.read().splitlines()
        
        seed = buf[0]
        num_leaf_nodes = buf[1]
        num_positions = buf[2]
        num_mutations = buf[3]
        percent_asym = buf[4]
        percent_observed = buf[5]
        
        data_settings = cdg.Data_Settings(seed,num_leaf_nodes,num_positions,num_mutations,percent_asym,percent_observed)
        
        method = buf[6]
        MST_method = buf[7]
        distance_metric = buf[8]
        tau = buf[9]
        epsilon = buf[10]
        
        recon_settings = tr.Recon_Settings(method,MST_method,distance_metric,tau,epsilon)
        
        f.close()      
             
        # Get observed vertices
        f = open("mr_bayes/obs_verts" + str(n) + ".txt")
        vertices = f.read().splitlines()
        root_id = int(vertices[0])
        observed_vertices = map(int, vertices[1:len(vertices)])
        
        # Parse Mr. Bayes result to networkx
        tree = Phylo.parse("mr_bayes/cell_dat" + str(n) + ".nex.con.tre","nexus").next()
        graph = Phylo._utils.to_networkx(tree)
        mapping = dict()
        for node in graph:
            if node.name == None:
                mapping[node] = node
            else:
                mapping[node] = int(node.name)
        nx.relabel_nodes(graph, mapping, copy = False)
        result = (gu.convert_to_directed(graph, root_id), None)
          
        # Package result
        my_results.append(pr.package_result(data_settings, recon_settings, ltm, observed_vertices, result))
        
    # Record all results 
    if not method == tr.Recon_Method.MR_BAYES and not method == tr.Recon_Method.BIT_PHYLO: # REMOVE bit_phylo
        file_name = sys.argv[1]
        f = open(file_name,'w')
        f.write("method\tMST_method\tdistance_metric\ttau\tepsilon\tseed\talphabet\tnum_leaf_nodes\tnum_positions\tpercent_asym\tnum_mutations\tpercent_observed\tsibling_sensitivity\tsibling_precision\tancestor_sensitivity\tancestor_precision\trecon_accuracy\tobserved_total_ratio_original\tobserved_total_ratio\trecon_run_time\tscore_run_time\n")
        
        if (my_results is not None):
            for result in my_results:
                f.write(result.get_print_str())
        
        f.close()
        
    
    