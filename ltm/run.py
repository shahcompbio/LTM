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

    parser.add_argument('filtered_cells',
                        help='''Path to filtered cells list.''')

    parser.add_argument('config_file',
                        help='''Path to config yaml file''')

    args = vars(parser.parse_args())

    return args


def main():
    args = parse_args()
    config = utils.load_config(args)
    
    pyp = pypeliner.app.Pypeline(config=args)

    workflow = pypeliner.workflow.Workflow()

    copy_number_matrix = args['copy_number_matrix']
    output_dir = args['out_dir']
    filtered_cells = args['filtered_cells']

    output_gml = os.path.join(output_dir, 'tree.gml')

    workflow.subworkflow(
        name='ltm',
        func=ltm.create_ltm_workflow,
        args=(
            mgd.InputFile(copy_number_matrix),
            mgd.InputFile(filtered_cells),
            mgd.OutputFile(output_gml),
            config,
        ),
    )

    pyp.run(workflow)

if __name__ == '__main__':
    main()
