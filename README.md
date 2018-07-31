## Running LTM Pipeline

The pipeline runs the latent tree model (LTM) algorithm on a copy number matrix to generate a tree.

### Installation:

```
conda install --file conda_packages.txt
python setup.py install
```

The LTM pipeline also requires the installation of pypeliner and pypeliner utils:

```
git clone https://bitbucket.org/dranew/pypeliner.git
cd pypeliner
python setup.py install

git clone https://svn.bcgsc.ca/bitbucket/scm/pp/pypeliner_utils.git
cd pypeliner_utils
python setup.py install
```

### Preprocessing the data:

The LTM pipeline is usually run with data generated from multiple runs of the single cell pipeline.
The outputs of the single cell pipeline need to be processed before it can be used as input for the LTM pipeline.
This is done by running `generate_ltm_inputs.py` as follows:

```
python generate_ltm_inputs.py SA535.csv SA535
```

In the example above, `SA535.csv` is a .csv file of all single cell analysis objects that make up the tree for the given sample ID and `SA535` is the sample ID of the tree.
For example, `SA535.csv` would contain the following:

```
jira_ticket,library_id,analysis_ploidy
SC-893,A96165B,autoploidy
SC-787,A95732A,autoploidy
SC-856,A95736A,autoploidy
```

* `jira_ticket` is the *Jira ticket number* of each constituent single cell analysis
* `library_id` is the *DLP library ID* associated with the single cell analysis
* `analysis_ploidy` is the *ploidy* of the single cell analysis to be used in the tree

Optionally, the flag `--output_dir` can be used to specify the output directory for the sample. The default value is `./output/`.

The script looks for a copy number matrix in `/genesis/shahlab/danlai/SC-803/hmmcopy/merged_output/<jira_ticket>/<analysis_ploidy>/<library_id>_cn_matrix.csv` and a metrics summary file in `/genesis/shahlab/danlai/SC-803/hmmcopy/merged_output/<jira_ticket>/<analysis_ploidy>/<library_id>_all_metrics_summary.csv`.
If a copy number matrix does not exist for the Jira ticket, the script will generate one.
To do this, it looks for the files `/projects/sftp/shahlab/singlecell/<jira_ticket>/hmmcopy_<analysis_ploidy>/<library_id>_hmmcopy.h5` and `/projects/sftp/shahlab/singlecell/<jira_ticket>/alignment/<library_id>_alignment_metrics.h5`.
It then uses a classifier to generate the file `<output_dir>/<jira_ticket>_all_metrics_summary_classified.csv`.

The script must be run from a location that can see the single cell pipeline results in SFTP (`/projects/sftp/`)

The metrics summary file is the used to filter for cells with quality >= 0.75.
The copy number matrices are then merged and filtered for bins with mappability >= 0.99. The resulting copy number matrix is then written to a .csv file in the output directory.


### Running the LTM pipeline:

```
ltm ltm/test_data/cn_matrix.csv output/ltm/
```

The first argument is the path to the copy number matrix file that was generated during preprocessing, and the second is the path to the output directory.

Optional arguments are:
* `--root_id`: ID of the cell to be used as the root of the tree. Default: the first SA928 cell
* `--config_file`: path to the configuration file to be used for the pipeline. Default: `config/ltm.yaml`
* `--filtered_cells`: text file of cells to analyze. Default: all cells are analyzed
* `--ltm_method`: method used for learning (CLG or RG). Default: CLG
* `--scale`: use the scaled minimum spanning tree method. Default: false
* `--number_of_jobs`: if the scaled method is used, the number of jobs to submit to the cluster. Default: 10

To run the pipeline locally,
```
ltm ltm/test_data/cn_matrix.csv output/ltm/ --loglevel DEBUG --submit local
```

To submit the pipeline to the job queue,
```
ltm ltm/test_data/cn_matrix.csv output/ltm/ --loglevel DEBUG --submit asyncqsub --nativespec ' -hard -q shahlab.q -P shahlab_high -V -l h_vmem={mem}G -pe ncpus {ncpus}'
```

