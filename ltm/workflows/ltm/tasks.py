import os
import pypeliner

scripts_directory = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'scripts')


def run_ltm(cn_matrix, filtered_cells, output_gml):
    script = os.path.join(scripts_directory, 'LTM_main', 'ltm.py')

    cmd = ['python', script, '-infile_path', cn_matrix, '-res_path', output_gml,
            '-method', 'CLG', '-filtered_cells_path', filtered_cells]

    pypeliner.commandline.execute(*cmd)


def generate_cellscape_inputs(cn_matrix, annotations, edges_list, cn_data, tree_gml):
    script = os.path.join(scripts_directory, 'Visualization_export', 'generate_cellescape_inputs.py')

    cmd = ['python', script, 
            '--path_to_data', cn_matrix,
            '--path_to_annotations', annotations,
            '--path_to_edges_list', edges_list,
            '--path_to_cn_data', cn_data
            '--path_to_tree', tree_gml
            '--root_id', 'test']

    pypeliner.commandline.execute(*cmd)


def run_cellscape(cn_data, annotations, edges_list):
    script = os.path.join(scripts_directory, 'generate_html_tree.R')

    cmd = ['Rscript', script, cn_data, annotations, edges_list]

    pypeliner.commandline.execute(*cmd)
