import os
import pypeliner
import pypeliner.managed as mgd
import tasks


def create_ltm_workflow(cn_matrix, output_gml, output_hdf, config, ltm_method, root_id, filtered_cells=None):

    workflow = pypeliner.workflow.Workflow()

    workflow.transform(
        name='run_ltm',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=tasks.run_ltm,
        args=(
            mgd.InputFile(cn_matrix),
            mgd.OutputFile(output_gml),
            ltm_method,
            filtered_cells,
        ),
    )

    workflow.transform(
        name='generate_cellscape_inputs',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=tasks.generate_cellscape_inputs,
        args=(
            mgd.InputFile(cn_matrix),
            mgd.TempOutputFile('cnv_annots.csv'),
            mgd.TempOutputFile('cnv_tree_edges.csv'),
            mgd.TempOutputFile('cnv_data.csv'),
            mgd.InputFile(output_gml),
            root_id,
        ),
    )

    workflow.transform(
        name='merge_csvs_to_hdf5',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=tasks.concatenate_csvs_to_hdf,
        args=(
            mgd.TempInputFile('cnv_annots.csv'),
            mgd.TempInputFile('cnv_tree_edges.csv'),
            mgd.TempInputFile('cnv_data.csv'),
            mgd.OutputFile(output_hdf),
        ),
    )

    # workflow.transform(
    #     name='run_cellscape',
    #     ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
    #     func=tasks.run_cellscape,
    #     args=(
    #         mgd.TempInputFile('cnv_annots.tsv'),
    #         mgd.TempInputFile('cnv_tree_edges.csv'),
    #         mgd.TempInputFile('cnv_data.csv'),
    #     ),
    # )

    return workflow
