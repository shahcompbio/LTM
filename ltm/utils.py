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


def get_cells_list(filtered_cells, cn_matrix):
    # Returns a list of cells to be analyzed
    # Ignore chr, start, end and width column headers
    cn = pd.read_csv(cn_matrix, nrows=1).columns.values.tolist()[4:]

    if filtered_cells:
        infile = open(filtered_cells)
        l = infile.readlines()
        cells_list = []
        for k in range(len(l)):
            cell = l[k].strip()
            if cell in cn:
                cells_list.append(l[k].strip())
        infile.close()
        return cells_list
    else:
        return cn
