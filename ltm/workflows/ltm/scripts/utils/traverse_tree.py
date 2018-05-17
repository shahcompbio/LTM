import os
import sys
import networkx as nx
import argparse



    
def root_tree(G, root_id):

    G2=nx.Graph()
    for ed in G.edges():
        G2.add_edge(ed[0],ed[1])    
    T=nx.dfs_tree(G2, root_id)#, orientation='ignore')
    return T
  

def read_tree(tree_gml_path, root_id):
    unrooted_tree=nx.read_gml(tree_gml_path)
    rooted_tree = root_tree(unrooted_tree, root_id)
    return rooted_tree


def make_clades(unrooted_tree_path, root_id, outfile_path):
    res_dict={}
    outfile=open(outfile_path,'w')
    outfile.write("clade_root"+'\t'+'descendants'+'\n')
    
    rooted_tree = read_tree(unrooted_tree_path, root_id) 
    
    bfs_dict = nx.bfs_successors(rooted_tree, root_id)
    for node,succesors_list in bfs_dict.iteritems():
        outfile.write(node+'\t'+",".join(succesors_list)+'\n')
    outfile.close()
        
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--unrooted_tree_path" ,type=str, help='path to unrooted tree gml')
    parser.add_argument("-r","--root_id" ,type=str, help='root node id')
    parser.add_argument("-o","--results_path" ,type=str, help='path to the results')
    args = parser.parse_args()
    
    make_clades(args.unrooted_tree_path, args.root_id, args.results_path)
    


    

    








    
    
