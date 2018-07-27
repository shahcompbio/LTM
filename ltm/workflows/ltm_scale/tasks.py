import os
import shutil
import pypeliner
import multiprocessing
import subprocess
from scipy.special import comb
from pypeliner_utils import helpers

from ltm import ltm

ltm_directory = os.path.realpath(os.path.dirname(ltm.__file__))


def generate_node_pair_csvs(cells_list, desired_job_no, node_pair_csvs):
    total_edges = comb(len(cells_list), 2)
    edg_per_node = int(total_edges / float(desired_job_no))

    tmp_counter = 0
    global_counter = 0
    file_counter = 1

    outfile = open(node_pair_csvs[0], 'w')

    for i in range(len(cells_list)):
        for j in range(i + 1, len(cells_list)):
            outfile.write(cells_list[i] + ',' + cells_list[j] + '\n')

            tmp_counter += 1
            global_counter += 1

            if tmp_counter == edg_per_node and global_counter < total_edges and file_counter < desired_job_no:
                tmp_counter = 0
                outfile.close()

                outfile = open(node_pair_csvs[file_counter], 'w')
                file_counter += 1

            if global_counter == total_edges:
                outfile.close()


def _calculate_distances_worker(node_pair_csv, outfile, cn_matrix):
    script = os.path.join(ltm_directory, 'LTM_scale','calculate_distance.py')

    cmd = ['python', script, '-input_file', node_pair_csv,
            '-output_path', outfile, '-data_path', cn_matrix]

    # pypeliner.commandline.execute(*cmd)
    # subprocess.check_call(cmd)
    helpers.run_cmd(cmd)


def calculate_distances(node_pair_csvs, cn_matrix, outfiles, config):
    count = config.get('threads', multiprocessing.cpu_count())
    pool = multiprocessing.Pool(processes=count)

    tasks = []

    for job in zip(node_pair_csvs, outfiles):
        node_pair_csv = job[0]
        outfile = job[1]

        task = pool.apply_async(_calculate_distances_worker, 
                                args=(node_pair_csv, outfile, cn_matrix))

        tasks.append(task)

    pool.close()
    pool.join()

    [task.get() for task in tasks]


## VISUALIZATION ##

def generate_cellscape_inputs(cn_matrix, annotations, edges_list, cn_data, tree_gml, rooted_tree_gml, root_id):
    script = os.path.join(ltm_directory, 'Visualization_export', 'generate_cellscape_inputs.py')

    cmd = ['python', script, 
            '--path_to_data', cn_matrix,
            '--path_to_annotations', annotations,
            '--path_to_edges_list', edges_list,
            '--path_to_cn_data', cn_data,
            '--path_to_tree', tree_gml,
            '--path_to_rooted_tree', rooted_tree_gml,
            '--root_id', root_id]

    pypeliner.commandline.execute(*cmd)


def move_cellscape(outfile):
    cellscape_rmarkdown = os.path.join(ltm_directory, 'cellscape.Rmd')

    shutil.copy(cellscape_rmarkdown, outfile)
