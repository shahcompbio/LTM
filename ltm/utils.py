import csv
import yaml
import pandas as pd


def read_bams_file(bams_file):

    bams = pd.read_csv(bams_file, dtype=str)

    for column in ('sample_id', 'tumour', 'normal',):
        if column not in bams.columns:
            raise Exception(
                'input bams_file should contain {}'.format(column))

    sample_ids = list(sorted(bams['sample_id'].unique()))

    if bams.duplicated(['sample_id']).any():
        raise Exception('input bams_file with duplicate sample_id pairs')

    tumour_files = dict()
    normal_files = dict()
    for _, row in bams.iterrows():
        tumour_files[row['sample_id']] = row['tumour']
        normal_files[row['sample_id']] = row['normal']

    return tumour_files, normal_files, sample_ids


def load_config(args):
    try:
        with open(args['config_file']) as infile:
            config = yaml.load(infile)

    except IOError:
        raise Exception(
            'Unable to open config file: {0}'.format(
                args['config_file']))
    return config
