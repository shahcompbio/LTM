import os
import sys
import numpy as np
import networkx as nx
import glob
import timeit
import argparse

def learn_CL(cell_data):
    node_ids=cell_data.keys()
    G = nx.Graph()
    start_d=timeit.default_timer()
    for i in range(len(node_ids)):
        G.add_node(node_ids[i])
        for j in range(i+1,len(node_ids)):
            #print cell_data[node_ids[i]]
            G.add_edge(node_ids[i], node_ids[j], weight=calc_MI(cell_data[node_ids[i]],cell_data[node_ids[j]]))
    end_d=timeit.default_timer()
    

    
    start_cl=timeit.default_timer()
    T = nx.minimum_spanning_tree(G)
    end_cl=timeit.default_timer()

    return T

def learn_CL_from_distance(distance_folder, tree_path):
    
    d_files = glob.glob(distance_folder+'/distance_list_*.csv')
    G = nx.Graph()
    
    for file in d_files:
        infile=open(file)
        for line in infile:
            tmp=line.strip().split(',')
            G.add_edge(tmp[0],tmp[1], weight=float(tmp[2]))
        infile.close()

    t1=timeit.default_timer()
    T = nx.minimum_spanning_tree(G)
    t2=timeit.default_timer()

    nx.write_gml(T, tree_path)
    

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-distance_folder", help="path to the folder with distance metrics.")
    parser.add_argument("-tree_path", help="path to the learned tree in gml format.")
    
    args = parser.parse_args()
    distance_folder=args.distance_folder
    tree_path = args.tree_path
    learn_CL_from_distance(distance_folder, tree_path)
    
