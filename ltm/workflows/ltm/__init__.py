import os
import pypeliner
import pypeliner.managed as mgd
import tasks


def create_ltm_workflow(cn_matrix, output_gml, config, ltm_method, root_id, filtered_cells=None):

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
            mgd.TempOutputFile('cnv_annots.tsv'),
            mgd.TempOutputFile('cnv_tree_edges.csv'),
            mgd.TempOutputFile('cnv_data.csv'),
            mgd.InputFile(output_gml),
            root_id,
        ),
    )

    # TODO: merge CSVs into HDF5

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
