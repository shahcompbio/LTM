import os
import argparse
import utils
import pypeliner
import pypeliner.managed as mgd
from workflows import ltm, ltm_scale


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    pypeliner.app.add_arguments(parser)

    parser.add_argument('copy_number_matrix',
                        help='''Path to copy number matrix (csv file).''')

    parser.add_argument('out_dir',
                        help='''Path to output files.''')

    parser.add_argument('root_id',
                        help='''ID of the cell to use as root of the tree.''')

    parser.add_argument('--config_file',
                        help='''Path to config yaml file.''',
                        default=os.path.join(os.path.realpath(os.path.dirname(__file__)), '../config/ltm.yaml'))

    parser.add_argument('--filtered_cells',
                        help='''Path to filtered cells list.''',
                        default=None)

    parser.add_argument('--ltm_method',
                        help='''LTM learning method (Chow Liu grouping or recursive grouping).''',
                        choices=['CLG', 'RG'],
                        default='CLG')

    parser.add_argument('--scale',
                        help='''Use scaled minimum spanning tree method.''',
                        action='store_true')

    parser.add_argument('--number_of_jobs',
                        help='''Number of jobs to submit for distance calculation for scaled method.''',
                        default=10,
                        type=int)

    args = vars(parser.parse_args())

    return args


def main():
    args = parse_args()
    config = utils.load_config(args)
    
    pyp = pypeliner.app.Pypeline(config=args)

    workflow = pypeliner.workflow.Workflow()

    if not utils.check_root_id(args['root_id'], args['copy_number_matrix']):
        raise Exception('Root id {root_id} is not a cell in the copy number matrix.'.format(root_id=args['root_id']))

    cells_list = utils.get_cells_list(args['filtered_cells'], args['copy_number_matrix'])

    output_gml = os.path.join(args['out_dir'], 'tree.gml')

    # Outputs required for visualization with cellscape
    cnv_annots_csv = os.path.join(args['out_dir'], 'cnv_annots.csv')
    cnv_tree_edges_csv = os.path.join(args['out_dir'], 'cnv_tree_edges.csv')
    cnv_data_csv = os.path.join(args['out_dir'], 'cnv_data.csv')
    output_rmd = os.path.join(args['out_dir'], 'cellscape.Rmd')
    output_hdf = os.path.join(args['out_dir'], 'cellscape_inputs.h5')

    if args['scale']:
        print 'Running LTM scale'
        workflow.subworkflow(
            name='ltm_scale',
            func=ltm_scale.create_ltm_scale_workflow,
            args=(
                mgd.InputFile(args['copy_number_matrix']),
                cells_list,
                mgd.OutputFile(output_gml),
                mgd.OutputFile(cnv_annots_csv),
                mgd.OutputFile(cnv_tree_edges_csv),
                mgd.OutputFile(cnv_data_csv),
                mgd.OutputFile(output_rmd),
                mgd.OutputFile(output_hdf),
                config,
                args['root_id'],
                args['number_of_jobs'],
            ),
        )
    else:
        print 'Running LTM'
        workflow.subworkflow(
            name='ltm',
            func=ltm.create_ltm_workflow,
            args=(
                mgd.InputFile(args['copy_number_matrix']),
                cells_list,
                mgd.OutputFile(output_gml),
                mgd.OutputFile(cnv_annots_csv),
                mgd.OutputFile(cnv_tree_edges_csv),
                mgd.OutputFile(cnv_data_csv),
                mgd.OutputFile(output_rmd),
                mgd.OutputFile(output_hdf),
                config,
                args['ltm_method'],
                args['root_id'],
            ),
        )

    pyp.run(workflow)

if __name__ == '__main__':
    main()
