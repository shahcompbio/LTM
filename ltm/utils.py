import csv
import yaml
import os
import pandas as pd


def load_config(config_file):
    try:
        with open(config_file) as infile:
            config = yaml.load(infile)

    except IOError:
        raise Exception(
            'Unable to open config file: {0}'.format(config_file))
    return config


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

def get_root(cells_list, out_dir):
    for cell in cells_list:
        if 'SA928' in cell:
            root_txt = os.path.join(out_dir, 'root.txt')
            with open(root_txt, 'w') as outfile:
                outfile.write(cell)
            outfile.close()
            return cell

    raise Exception('No SA928 cells in the copy number matrix.')
