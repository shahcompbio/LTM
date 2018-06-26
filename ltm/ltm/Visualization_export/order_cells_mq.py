import os
import sys
import numpy as np
import networkx as nx
from sklearn.metrics import mutual_info_score
import sklearn
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

def read_cn_file(cn_matrix_path):
    data_dict={}
    data = np.genfromtxt(cn_matrix_path, delimiter=",", skip_header=1)
    infile=open(cn_matrix_path)
    cell_ids=infile.readline().strip().split(',')
    for j in range(len(cell_ids)):
        data_dict[cell_ids[j]] = data[:,j].astype(int)
    
    infile.close()
    return data_dict
    
    
def get_mean_cn(tree, source, data_dict):
    descendants_list=list(nx.descendants(tree,source))
    if len(descendants_list)==0:
        mean_cn=data_dict[source]
    else:
        mean_cn=data_dict[descendants_list[0]]
        for desc in descendants_list[1:]:
            mean_cn+=data_dict[desc]
        mean_cn=mean_cn/len(descendants_list)
    return mean_cn



def calc_euc(x, y):
    mi = sklearn.metrics.pairwise.pairwise_distances(x, y, metric='euclidean')
    return mi

def calc_MI(x, y):
    bins=len(x)/10
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    #print mi
    return mi


def sort_clades(cns_dict,ancestor_id):    
    sorted_points = sorted(cns_dict.keys(), key=lambda e: calc_MI(cns_dict[ancestor_id], cns_dict[e]), reverse=True)
    j=sorted_points.index(ancestor_id)
    del(sorted_points[j])
    return sorted_points
    
    
def traverse_tree(tree,root_id, data_dict, outfile_path):
    res_dict={}
    outfile=open(outfile_path,'w')
    bfs_dict = nx.bfs_successors(tree, root_id)
    for node,succesors_list in bfs_dict.iteritems():
        tmp_mean_cn_dict={}
        #print 'Traversing node '+node
        for n in succesors_list:
            tmp_mean_cn_dict[n]=get_mean_cn(tree, n, data_dict)
        tmp_mean_cn_dict[node]=data_dict[node]
        sorted_node_ids = sort_clades(tmp_mean_cn_dict,node)
        res_dict[node]=sorted_node_ids
        succ=",".join(sorted_node_ids)
        outfile.write(node+'\t'+ succ+'\n')
    outfile.close()
    

    return res_dict

def make_ordered_list(unrooted_tree_path, root_id, cn_matrix_path, outfile_path):
    data_dict = read_cn_file(cn_matrix_path)
    tree = read_tree(unrooted_tree_path, root_id)    
    res_dict = traverse_tree(tree,root_id, data_dict,outfile_path)    
    

if __name__=='__main__':    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--unrooted_tree_path" ,type=str, help='path to tree gml')
    parser.add_argument("-r","--root_id" ,type=str, help='root node id')
    parser.add_argument("-c","--cn_matrix_path" ,type=str, help='path to the copy numbers')
    parser.add_argument("-o","--results_path" ,type=str, help='path to the results')
    
    args = parser.parse_args()
    make_ordered_list(args.unrooted_tree_path, args.root_id, args.cn_matrix_path, args.results_path)








    
    
