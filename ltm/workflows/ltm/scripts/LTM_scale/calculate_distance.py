import numpy as np
import networkx as nx
import timeit
from sklearn.metrics import mutual_info_score
import sklearn
import argparse
import string


def convert_n_alpha_cn(inar):
    num2alpha = dict(zip(range(0, 27), string.ascii_lowercase))
    
    s=''
    for n in inar:
        t=int(n)
        s+=num2alpha[t]
    return s


def breakpoint_conevert(bps_list, pre_cns):
    res_list=[]
    for i in range(len(pre_cns)):
        if i in bps_list:
            res_list.append(pre_cns[i])
    return res_list




def calc_MI(x, y):
    bins=len(x)/10
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return -mi


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
    
    print "total time for distance calculation "+str(end_d-start_d)
    
    start_cl=timeit.default_timer()
    T = nx.minimum_spanning_tree(G)
    end_cl=timeit.default_timer()
    print "total time for CL only "+str(end_cl-start_cl)
    return T

def calculate_distance(cell_data, infile_path, outfile_path):
    outfile=open(outfile_path,'w')
    pairs=set([])
    infile=open(infile_path)
    for line in infile:
        #print line
        tmp=line.strip().split(',')
        t1=timeit.default_timer()
        weight = calc_MI(cell_data[tmp[0]],cell_data[tmp[1]])
        t2=timeit.default_timer()
        outfile.write(tmp[0]+','+tmp[1]+','+str(weight)+','+str(t2-t1)+'\n')
    outfile.close()
    infile.close()
        
        

def find_symbole_number(infile_path):
    
    alphabets_set=set([])
    infile=open(infile_path)
    l=infile.readlines()
    for line in l[1:]:
        tmp=line.strip().split(',')
        for t in tmp:
            alphabets_set.add(int(t))
    infile.close()
    max_cn=max(alphabets_set)
    return max_cn


def break_points_finder(infile_path):
    data = np.genfromtxt(infile_path, delimiter=",", skip_header=1)
    print "max CN "+str(np.amax(data))
    # find breakpoint
    bps_set=set([])
    for j in range(data.shape[1]):
        for i in range(1,data.shape[0]):
            if data[i,j]!=data[i-1,j]:
                bps_set.add(i)
    bps_set.add(0)
    bps_list=list(bps_set)

    return bps_list

def with_break_point_correction_read_input_np(data_path, infile_path):
    


    
    bps_list= break_points_finder(data_path)

    cell_data={}
    
    ###### read list of filtered cells
    cells_set=set([])
    cells_file=open(infile_path)
    for line in cells_file:
        tmp=line.strip().split(',')
        cells_set.add(tmp[0])
        cells_set.add(tmp[1])
    
    #######
    
    data = np.genfromtxt(data_path, delimiter=",", skip_header=1)
    infile=open(data_path)
    cell_ids=infile.readline().strip().split(',')[4:]

    for cell_id in cell_ids:
        #cell_data[i]=convert_n_alpha_cn(data[:,i])
        j=cell_ids.index(cell_id)
        if cell_id in cells_set:
            #cell_data[i]=breakpoint_conevert(bps_list, data[:,j])
            cell_data[cell_id]=breakpoint_conevert(bps_list, data[:,j+4])

        
    return cell_data

def read_input_np(data_path, infile_path):
    

    #bps_list= break_points_finder(data_path)

    cell_data={}
    
    ###### read list of filtered cells
    cells_set=set([])
    cells_file=open(infile_path)
    for line in cells_file:
        tmp=line.strip().split(',')
        cells_set.add(tmp[0])
        cells_set.add(tmp[1])
    
    #######
    
    data = np.genfromtxt(data_path, delimiter=",", skip_header=1)
    infile=open(data_path)
    cell_ids=infile.readline().strip().split(',')[4:]

    for cell_id in cell_ids:
        #cell_data[i]=convert_n_alpha_cn(data[:,i])
        j=cell_ids.index(cell_id)
        if cell_id in cells_set:
            #cell_data[i]=breakpoint_conevert(bps_list, data[:,j])
            cell_data[cell_id]=data[:,j+4]

    return cell_data

def read_hmm_cn_data(data_path, outfile_path, infile_path):
    
    
    cell_data = read_input_np(data_path, infile_path)
    #cell_data = read_input_np(infile_path, filtered_cells_path)

    CL_start = timeit.default_timer()
    calculate_distance(cell_data, infile_path, outfile_path)
    CL_end = timeit.default_timer()
    
    print "total time "+str(CL_end-CL_start)
    

if __name__=='__main__':
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_file", help="path to the edges lists folder.")
    parser.add_argument("-output_path", help="Path to the results.")
    parser.add_argument("-data_path", help="Path to the  cn data.")
    #data_path='/Users/hfarahani/shahlab_root/hfarahani/mg_derakht/data/combined_deep_hTERT_nur_CL/all_cn_matrix.csv'
    #data_path='/genesis/shahlab/hfarahani/mg_derakht/data/SSlh_data/raw_data/merged_all.csv'
    args = parser.parse_args()
    input_file=args.input_file
    output_path=args.output_path
    data_path=args.data_path
    
    read_hmm_cn_data(data_path, output_path, input_file)
    
    
    
    
    
    