import os
import pypeliner
import pypeliner.managed as mgd

import tasks
from ltm.ltm import hdfutils
from ltm.ltm.LTM_scale import learn_CL_from_distance


def create_ltm_scale_workflow(cn_matrix, 
                        cells_list,
                        output_gml,
                        output_rooted_gml,
                        cnv_annots_csv,
                        cnv_tree_edges_csv,
                        cnv_data_csv,
                        output_rmd,
                        output_hdf,
                        config,
                        root_id,
                        number_jobs):

    workflow = pypeliner.workflow.Workflow()

    # Convert copy number matrix csv file to hdf5 for faster downloading onto compute nodes
    # workflow.transform(
    #     name='cn_matrix_to_hdf5',
    #     ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': 1},
    #     func=hdfutils.convert_csv_to_hdf,
    #     args=(
    #         mgd.InputFile(cn_matrix),
    #         mgd.TempOutputFile('cn_matrix.h5'),
    #         'copy_number_matrix',
    #     ),
    # )

    node_pair_csvs = []
    for job in range(number_jobs):
        node_pair_csvs.append('list_{}.csv'.format(job))

    workflow.transform(
        name='generate_input_csvs',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': 1},
        func=tasks.generate_node_pair_csvs,
        args=(
            cells_list,
            number_jobs,
            [mgd.TempOutputFile(csv) for csv in node_pair_csvs],
        ),
    )

    distance_csvs = []
    for job in range(number_jobs):
        distance_csvs.append('distance_list_{}.csv'.format(job))

    workflow.transform(
        name='calculate_distances',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': config['threads']},
        func=tasks.calculate_distances,
        args=(
            [mgd.TempInputFile(csv) for csv in node_pair_csvs],
            # mgd.TempInputFile('cn_matrix.h5'), #FIXME
            mgd.InputFile(cn_matrix),
            [mgd.TempOutputFile(csv) for csv in distance_csvs],
            config,
        ),
    )

    # Generates a minimum spanning tree
    workflow.transform(
        name='generate_tree',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': 1},
        func=learn_CL_from_distance.learn_CL_from_distance,
        args=(
            [mgd.TempInputFile(csv) for csv in distance_csvs],
            mgd.OutputFile(output_gml),
        ),
    )

    workflow.transform(
        name='generate_cellscape_inputs',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': 1},
        func=tasks.generate_cellscape_inputs,
        args=(
            # mgd.TempInputFile('cn_matrix.h5'), #FIXME
            mgd.InputFile(cn_matrix),
            mgd.OutputFile(cnv_annots_csv),
            mgd.OutputFile(cnv_tree_edges_csv),
            mgd.OutputFile(cnv_data_csv),
            mgd.InputFile(output_gml),
            mgd.OutputFile(output_rooted_gml),
            root_id,
        ),
    )

    tasks.move_cellscape(output_rmd)

    workflow.transform(
        name='create_cellscape_rmarkdown',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': 1},
        func=tasks.move_cellscape,
        args=(
            mgd.OutputFile(output_rmd),
        ),
    )

    workflow.transform(
        name='merge_csvs_to_hdf5',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard'], 'ncpus': 1},
        func=hdfutils.concat_csvs_to_hdf,
        args=(
            [mgd.InputFile(cnv_annots_csv),
            mgd.InputFile(cnv_tree_edges_csv),
            mgd.InputFile(cnv_data_csv)],
            mgd.OutputFile(output_hdf),
            ['annotations', 'edges_list', 'cn_data'],
        ),
    )

    return workflow