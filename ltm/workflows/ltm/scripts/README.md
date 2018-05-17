# LTM
Given an adjacency matrix containing information about chromosome copy numbers in different cells, generate a tree in GML format.

# Dependencies
- networkx=1.11
- pandas
- scipy

# How to run
## < 1000 cells
For fewer than 1000 cells, run LTM_main/ltm.py:

```
python ltm.py -infile_path ../test_data/cn_matrix.csv -res_path ../test_data/test.gml -method CLG -filtered_cells_path ../test_data/filtered_cells.csv
```

An example adjacency matrix is provided in test_data/cn_matrix.csv, and test_data/filtered_cells.csv is simply a list that allows the user to indicate a subset of cells for the script to look at; this allows you to generate different trees from the same adjacency matrix.

## ≥ 1000 cells
For 1000 cells or more, we would like to parallelize the task. First, run LTM_scale/generate_cluster_tasks.py:

```
python generate_cluster_tasks.py -filtered_cells /shahlab/sochan/ltm_2/test_data/filtered_cells.csv -chopped_files /shahlab/sochan/ltm_2/test_data/chopped_files -cluster_jobs /shahlab/sochan/ltm_2/test_data/cluster_jobs -dist_scr /shahlab/sochan/ltm_2/LTM_scale/calculate_distance.py -dist_files /shahlab/sochan/ltm_2/test_data/dist_files -desired_job_no 10 -cn_data /shahlab/sochan/ltm_2/test_data/cn_matrix.csv
```

This results in a series of shell scripts that contain the jobs to be run on the cluster. Supply the absolute paths in all cases here. Go to test_data/cluster_jobs and change the permissions so that the file can be run:

```
chmod 755 *.sh
```

Now, we can submit the jobs by simply running submit_all.sh in the same directory. The result will be a series of distance files in test_data/dist_files. Now we run LTM_scale/learn_CL_from_distance.py:

```
python learn_CL_from_distance.py -distance_folder ../test_data/dist_files -tree_path ../test_data/test.gml
```


# Visualization
The output of the previous section, regardless of the number of cells, should be a tree in GML format. Now we can create the input for CellScape by running Visualization_export/generate_cellescape_inputs.py:

```
python generate_cellescape_inputs.py -d ../test_data/cn_matrix.csv -o ../test_data/viz -t ../test_data/test.gml -r SA604X6XB01979-A95722A-R04-C48
```

The output should be three files, need to be copied or moved to cellscape/inst/extdata:
- cnv_annots.tsv
- cnv_data.read_csv
- cnv_tree_edges.csv

Note: CellScape is incompatible with the latest version of R. At the moment, we know that it works with R 3.0.0 for sure. In your .bashrc or .bash_profile, add:

```
export PATH="/gsc/software/linux-x86_64-centos5/R-3.0.0/bin:$PATH"
```

Finally, the last step is to open generate_html_tree.R, set line 4 in the code to your your own cellscape/inst/extdata directory, and run the script.
