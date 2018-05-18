import csv
import yaml
import pandas as pd


def load_config(args):
    try:
        with open(args['config_file']) as infile:
            config = yaml.load(infile)

    except IOError:
        raise Exception(
            'Unable to open config file: {0}'.format(
                args['config_file']))
    return config


def check_root_id(root_id, cn_matrix):

    cn = pd.read_csv(cn_matrix, nrows=1)

    return root_id in cn.columns
