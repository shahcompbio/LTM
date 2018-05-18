import os
import argparse
import utils
import pypeliner
import pypeliner.managed as mgd
from workflows import ltm


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    pypeliner.app.add_arguments(parser)

    parser.add_argument('copy_number_matrix',
                        help='''Path to copy number matrix (csv file).''')

    parser.add_argument('out_dir',
                        help='''Path to output files.''')

    parser.add_argument('root_id',
                        help='''ID of the cell to use as root of the tree.''')

    parser.add_argument('--ltm_method',
                        help='''LTM learning method (Chow Liu grouping or recursive grouping).''',
                        choices=['CLG', 'RG'],
                        default='CLG')

    parser.add_argument('--config_file',
                        help='''Path to config yaml file.''',
                        default='ltm/config/grch37/shahlab/local_ltm.yaml')

    parser.add_argument('--filtered_cells',
                        help='''Path to filtered cells list.''',
                        default=None)

    args = vars(parser.parse_args())

    return args


def main():
    args = parse_args()
    config = utils.load_config(args)
    
    pyp = pypeliner.app.Pypeline(config=args)

    workflow = pypeliner.workflow.Workflow()

    filtered_cells = args['filtered_cells']

    if not utils.check_root_id(args['root_id'], args['copy_number_matrix']):
        raise Exception('Root id {root_id} is not a cell in the copy number matrix.'.format(root_id=args['root_id']))

    output_gml = os.path.join(args['out_dir'], 'tree.gml')

    if args['filtered_cells']:
        workflow.subworkflow(
            name='ltm',
            func=ltm.create_ltm_workflow,
            args=(
                mgd.InputFile(args['copy_number_matrix']),
                mgd.OutputFile(output_gml),
                config,
                args['ltm_method'],
                args['root_id'],
                mgd.InputFile(args['filtered_cells']),
            ),
        )
    else:
        workflow.subworkflow(
            name='ltm',
            func=ltm.create_ltm_workflow,
            args=(
                mgd.InputFile(args['copy_number_matrix']),
                mgd.OutputFile(output_gml),
                config,
                args['ltm_method'],
                args['root_id'],
            ),
        )

    pyp.run(workflow)

if __name__ == '__main__':
    main()
