## Running LTM Pipeline

The pipeline generates a GML tree and an HDF5 file with inputs that can be used for cellscape.

### Installing:

```
conda install --file conda_packages.txt
python setup.py install
```

### Running with test data:

```
ltm ltm/test_data/cn_matrix.csv output/ltm/ SA604X6XB01979-A95722A-R15-C40 ltm/config/ltm.yaml
```

The pipeline takes in: 
* a CSV file of copy numbers for a list of cells,
* the path to the output directory,
* the ID of the cell to be used as the root of the tree, and
* the path to the config YAMl file that specifies the pools and their memory

Optionally, it can take in:
* `--ltm_method`: method used for learning (CLG or RG)
* `--filtered_cells`: text file of cells to analyze
