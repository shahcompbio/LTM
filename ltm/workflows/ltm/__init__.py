import os
import pypeliner
import pypeliner.managed as mgd
import tasks


def create_ltm_workflow(cn_matrix, filtered_cells, output_gml, config):

    workflow = pypeliner.workflow.Workflow()

    workflow.transform(
        name='run_ltm',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=tasks.run_ltm,
        args=(
            mgd.InputFile(cn_matrix),
            mgd.InputFile(filtered_cells),
            mgd.OutputFile(output_gml),
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
            mgd.InputFile(output_gml)
        ),
    )

    workflow.transform(
        name='run_cellscape',
        ctx={'mem': config['memory']['med'], 'pool_id': config['pools']['standard']},
        func=tasks.run_cellscape,
        args=(
            mgd.TempOutputFile('cnv_annots.tsv'),
            mgd.TempOutputFile('cnv_tree_edges.csv'),
            mgd.TempOutputFile('cnv_data.csv'),
        ),
    )

    return workflow
