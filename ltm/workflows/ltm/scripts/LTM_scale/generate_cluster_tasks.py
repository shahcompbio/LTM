import os
import sys
import glob
import argparse
from scipy.special import comb

def generate_cluster_job(cluster_jobs_root,chopped_files_path, script_path, distance_files_path, cn_data):
    chopped_files=glob.glob(chopped_files_path+'/list*')

    for file_path in chopped_files:
        file=file_path.split('/')[-1]
        print file
        if file[0:4]=='list':
            outfile=open(cluster_jobs_root+'/dist_job_'+file.split('.')[0]+'.sh','w')
            outfile.write('#$ -S /bin/sh'+'\n')
            outfile.write('#$ -r n'+'\n')
            outfile.write('#$ -N j_'+file.split('.')[0]+'\n')
            outfile.write('#$ -l h_rt=10:01:00'+'\n')
            outfile.write('#$ -l s_rt=10:00:00'+'\n')
            outfile.write('#$ -l h_vmem=8G'+'\n')
            outfile.write('#$ -e '+cluster_jobs_root+'/error_'+file.split('.')[0]+'.txt'+'\n')
            outfile.write('#$ -o '+cluster_jobs_root+'/output_'+file.split('.')[0]+'.txt'+'\n')
            outfile.write('export PATH="/shahlab/hfarahani/Softwares/anaconda/bin:$PATH"'+'\n')
            outfile.write('python '+script_path+' -input_file '+chopped_files_path+'/'+file+' -output_path '+distance_files_path+'/distance_'+file.split('.')[0]+'.csv -data_path '+cn_data)
            outfile.close()

def make_cluster_submit_script(cluster_jobs_root):
    lines_list=['#!/bin/bash']
    for file_path in glob.glob(cluster_jobs_root+'/dist*sh'):
        print file_path
        lines_list.append('qsub -hard -q shahlab.q -l shah_io=1 '+file_path)
    outfile=open(cluster_jobs_root+'/submit_all.sh','w')
    for line in lines_list:
        outfile.write(line+'\n')
    outfile.close()



def generate_inputfiles(filtered_cells_path, outfiles_path, desired_job_no):
    infile=open(filtered_cells_path)
    l=infile.readlines()
    cells_list=[]
    for k in range(len(l)):
        cells_list.append(l[k].strip())
    infile.close()

    total_edges= comb(len(cells_list),2)
    print "total edges "+str(total_edges)
    edg_per_node=int(total_edges/float(desired_job_no))
    print "edg_per_node "+str(edg_per_node)

    tmp_counter=0
    global_counter=0

    outfile=open(outfiles_path+'/list_'+str(global_counter)+'.csv','w')

    for i in range(len(cells_list)):
        for j in range(i+1,len(cells_list)):
            outfile.write(cells_list[i]+','+cells_list[j]+'\n')

            tmp_counter+=1
            global_counter+=1

            if tmp_counter==edg_per_node and global_counter<total_edges:
                tmp_counter=0
                outfile.close()
                outfile=open(outfiles_path+'/list_'+str(global_counter+1)+'.csv','w')

            if global_counter==total_edges:
                outfile.close()





def make_scripts(filtered_cells, chopped_files, cluster_jobs, dist_scr, dist_files, desired_job_no, cn_data):

    # makde necessary folders
    os.makedirs(chopped_files)
    os.makedirs(cluster_jobs)
    os.makedirs(dist_files)

    # make the chopped files
    generate_inputfiles(filtered_cells, chopped_files, desired_job_no)

    # make jobs for cluster nodes
    generate_cluster_job(cluster_jobs, chopped_files, dist_scr, dist_files, cn_data)

    make_cluster_submit_script(cluster_jobs)



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-filtered_cells", help="path to the filtered cells.")
    parser.add_argument("-chopped_files", help="path to the folder that will contains the chopped files.")
    parser.add_argument("-cluster_jobs", help="path to the folder containing the cluster jobs.")
    parser.add_argument("-dist_scr", help="path to calculate_distance.py.")
    parser.add_argument("-dist_files", help="path to folder that will contain the distance files.")
    # parser.add_argument("-submit_all", help="path to the script for submitting all jobs.")
    parser.add_argument("-desired_job_no", help="desired number of jobs.")
    parser.add_argument("-cn_data", help="path to CN data.")

    args = parser.parse_args()
    filtered_cells=args.filtered_cells
    chopped_files=args.chopped_files
    cluster_jobs=args.cluster_jobs
    dist_scr=args.dist_scr
    dist_files=args.dist_files
    # submit_all=args.submit_all
    desired_job_no=args.desired_job_no
    cn_data=args.cn_data

    make_scripts(filtered_cells, chopped_files, cluster_jobs, dist_scr, dist_files, desired_job_no,cn_data)
