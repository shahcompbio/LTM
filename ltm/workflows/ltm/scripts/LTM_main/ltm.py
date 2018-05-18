
import tree_reconstruct as tr
import networkx as nx
import csv
import sys
import os
import argparse
import numpy as np
import string

 


def find_symboles(data_folder):
    # find the set of symbols for CN from HMMCopy data
    symbols_set = set([])
    for file in os.listdir(data_folder):
        if file.find('corrected_reads')!=-1:
            infile=open(data_folder+'/'+file)
            l=infile.readlines()
            length=len(l[0].strip().split(','))
            if length==15:
                for i in range(1,len(l)):
                    CN=l[i].strip().split(',')[-1]
                    if CN!='NA' and CN!='Inf':
                        symbols_set.add(CN)
                    if CN=='NA':
                        symbols_set.add('0')
                    if CN=='Inf':
                        symbols_set.add('15')
            infile.close()
    
    symbols_list = list(symbols_set)
    return symbols_list
    
    


def convert_num_to_alphabet(n):
    import string
    for x, y in zip(range(1, 27), string.ascii_lowercase):
        print(x, y)



    
def convert_n_alpha_cn(inar):
    num2alpha = dict(zip(range(0, 27), string.ascii_lowercase))
    
    s=''
    for n in inar:
        t=int(n)
        s+=num2alpha[t]
    return s




def break_points_finder(infile_path):
    data = np.genfromtxt(infile_path, delimiter=",", skip_header=1)
    # print "max CN "+str(np.amax(data))
    # find breakpoint
    bps_set=set([])
    for j in range(data.shape[1]):
        for i in range(1,data.shape[0]):
            if data[i,j]!=data[i-1,j]:
                bps_set.add(i)
    bps_set.add(0)
    bps_list=list(bps_set)

    return bps_list

def breakpoint_conevert(bps_list, pre_cns):
    res_list=[]
    for i in range(len(pre_cns)):
        if i in bps_list:
            res_list.append(pre_cns[i])
    return res_list
        

def read_input_np(infile_path, filtered_cells_path):
    
    cell_id_to_name = {}
    cell_id=0
    
    bps_list= break_points_finder(infile_path)

    cell_data={}
    
    ###### read list of filtered cells
    filtered_cells_set=set([])

    if filtered_cells_path != 'None':
        filtered_file=open(filtered_cells_path)
        l=filtered_file.readlines()
        for i in range(0,len(l)):
            filtered_cells_set.add(l[i].strip())
        filtered_file.close()
    #######
    
    data = np.genfromtxt(infile_path, delimiter=",", skip_header=1)
    infile=open(infile_path)
    cell_ids=infile.readline().strip().split(',')[4:]
    i=0
    for cell_id in cell_ids:
        #cell_data[i]=convert_n_alpha_cn(data[:,i])
        j=cell_ids.index(cell_id)
        if not filtered_cells_set or (filtered_cells_set and cell_id in filtered_cells_set):
            cell_data[i]=convert_n_alpha_cn(breakpoint_conevert(bps_list, data[:,j+4]))
            cell_id_to_name[i]=cell_ids[j]
        i+=1
    
    position_data = dict()
    for i in range(len(cell_data.values()[0])):
        position_data[i] = ([d[i] for d in cell_data.values()])
    
    return cell_data,position_data,cell_id_to_name

def find_symbole_number(infile_path):
    
    alphabets_set=set([])
    infile=open(infile_path)
    l=infile.readlines()
    for line in l[1:]:
        tmp=line.strip().split(',')[4:]
        for t in tmp:
            alphabets_set.add(int(t))
    infile.close()
    max_cn=max(alphabets_set)
    return max_cn



def read_hmm_cn_data(infile_path, res_path, LTM_method, filtered_cells_path):
    

    max_cn=find_symbole_number(infile_path)
    
    all_symbols_list=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w']
    symbols_list=all_symbols_list[0:max_cn+1]
    
    
    if LTM_method=='CLG':
        method=tr.Recon_Method.CHOW_LIU_GROUPING
    if LTM_method=='RG':
        method=tr.Recon_Method.RECURSIVE_GROUPING
    
    
    tau = 3
    epsilon = 0.08

    root_id = 0 
    
    cell_data,position_data,cell_id_to_name = read_input_np(infile_path, filtered_cells_path)
    
    recon_settings = tr.Recon_Settings(method, tau, epsilon)

    result = tr.reconstruct(recon_settings, position_data, cell_data, symbols_list)#, root_id, 0, False)
    nx.relabel_nodes(result[0], cell_id_to_name, copy = False)
    nx.write_gml(result[0], res_path)
    
    
       
if __name__=='__main__':
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-infile_path", help="path to the data folder.")
    parser.add_argument("-res_path", help="Path to the results.")
    parser.add_argument("-method", help="LTM learning method, CLG or RG.")
    parser.add_argument("-filtered_cells_path", help="Path to list of the filtered cells.")
    
    args = parser.parse_args()
    infile_path=args.infile_path
    res_path=args.res_path
    method=args.method
    filtered_cells_path=args.filtered_cells_path
    
    read_hmm_cn_data(infile_path, res_path, method, filtered_cells_path)
    
    
    
    
    
    