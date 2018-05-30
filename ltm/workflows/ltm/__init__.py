import os
import pypeliner
import pypeliner.managed as mgd
import tasks

from scripts import hdfutils
from scripts.LTM_main import ltm
from scripts.Visualization_export import generate_cellscape_inputs


def create_ltm_workflow(cn_matrix,
                        cells_list,
                        output_gml,
                        cnv_annots_csv,
                        cnv_tree_edges_csv,
                        cnv_data_csv,
                        output_rmd,
                        output_hdf,
                        config,
                        ltm_method,
                        root_id):

    workflow = pypeliner.workflow.Workflow()

    workflow.transform(
        name='run_ltm',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=ltm.read_hmm_cn_data,
        args=(
            mgd.InputFile(cn_matrix),
            mgd.OutputFile(output_gml),
            ltm_method,
            cells_list,
        ),
    )

    workflow.transform(
        name='generate_cellscape_inputs',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=generate_cellscape_inputs.main_generate_all,
        args=(
            mgd.InputFile(cn_matrix),
            mgd.OutputFile(cnv_annots_csv),
            mgd.OutputFile(cnv_tree_edges_csv),
            mgd.OutputFile(cnv_data_csv),
            mgd.InputFile(output_gml),
            root_id,
        ),
    )

    workflow.transform(
        name='create_cellscape_rmarkdown',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=tasks.move_cellscape,
        args=(
            mgd.OutputFile(output_rmd),
        ),
    )

    workflow.transform(
        name='merge_csvs_to_hdf5',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
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
