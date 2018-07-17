import argparse
import os
import pandas as pd
import subprocess
import numpy as np


def get_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('input_file', help = 'Path to input .csv file.')
	parser.add_argument('sample_id', help = 'Sample ID of the tree.')

	parser.add_argument('--output_dir', help = 'Output directory for the sample', default = 'output/')

	args = parser.parse_args()

	return args


def get_analysis_ploidy(analysis_ploidy):
	if 'autoploidy' in analysis_ploidy:
		return '00'
	elif 'diploid' in analysis_ploidy:
		return '02'
	raise Exception('Unrecognized ploidy: {}'.format(analysis_ploidy))


def get_sftp_ploidy(analysis_ploidy):
	if 'autoploidy' in analysis_ploidy:
		return 'hmmcopy_autoploidy'
	elif 'diploid' in analysis_ploidy:
		return 'hmmcopy_diploid'
	raise Exception('Unrecognized ploidy: {}'.format(analysis_ploidy))


def get_cn_matrix_from_hdf(hmmcopy_hdf_file, ploidy):
	df = get_reads_from_hdf(hmmcopy_hdf_file, ploidy)

	df["bin"] = list(zip(df.chr, df.start, df.end))
	df = df.pivot(index='cell_id', columns='bin', values='state')
	chromosomes = map(str, range(1, 23)) + ['X', 'Y']
	bins = pd.DataFrame(df.columns.values.tolist(),
	                    columns=['chr', 'start', 'end'])
	bins["chr"] = pd.Categorical(bins["chr"], chromosomes)
	bins = bins.sort_values(['start', ])
	bins = [tuple(v) for v in bins.values.tolist()]
	df = df.sort_values(bins, axis=0).T

	dropped_cells = df.columns[df.isna().all()].tolist()

	print 'Dropping {} cells: {}'.format(len(dropped_cells), dropped_cells)

	df = df.loc[:, ~df.isna().all()].astype(int)
	df.columns = df.columns.astype(str)
	df = df.reset_index()

	return df, dropped_cells


def get_quality_from_hdf(hmmcopy_hdf_file, alignment_hdf_file, ploidy, merged_csv):
	hmmcopy_metrics = pd.read_hdf(hmmcopy_hdf_file, '/hmmcopy/metrics/' + ploidy[-1]) # Keep total_mapped_reads from this
	alignment_metrics = pd.read_hdf(alignment_hdf_file, '/alignment/metrics')

	alignment_metrics = alignment_metrics.drop(columns = 'total_mapped_reads')

	merged_df = pd.merge(hmmcopy_metrics, alignment_metrics, how = 'outer', 
		on = ['cell_id', 'row', 'column', 'primer_i5', 'primer_i7', 'img_col', 
			  'sample_type', 'experimental_condition', 'cell_call',
			  'index_i5', 'index_i7'])
	merged_df = merged_df.rename({'log_likelihood': 'loglikehood'}, axis = 'columns')

	merged_df.to_csv(merged_csv)


def classify_metrics(infile, outfile):
	script = 'classify.R'

	cmd = ['Rscript', script, infile, outfile]

	print ' '.join(cmd)

	subprocess.check_call(cmd)


def get_reads_from_hdf(hdf_file, ploidy):
	return pd.read_hdf(hdf_file, '/hmmcopy/reads/' + ploidy[-1])


def main():
	args = get_args()

	output_dir = os.path.join(args.output_dir, args.sample_id)
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)

	# Read contents of Jira ticket table
	df = pd.read_csv(args.input_file, index_col = 0)

	cn_list = []
	for jira_ticket, row in df.iterrows():
		print 'Filtering ticket {}'.format(jira_ticket)

		analysis_ploidy = get_analysis_ploidy(row['analysis_ploidy'])
		sftp_ploidy = get_sftp_ploidy(row['analysis_ploidy'])

		genesis_dir_path = os.path.join('/genesis/shahlab/danlai/SC-803/hmmcopy/merged_output', jira_ticket, analysis_ploidy)
		cn_matrix_file = os.path.join(genesis_dir_path, row['library_id'] + '_cn_matrix.csv')
		all_metrics_summary_file = os.path.join(genesis_dir_path, row['library_id'] + '_all_metrics_summary.csv')
		reads_file = os.path.join(genesis_dir_path, row['library_id'] + '_reads.csv')

		hmmcopy_hdf_file = os.path.join('/projects/sftp/shahlab/singlecell', jira_ticket, sftp_ploidy, row['library_id'] + '_hmmcopy.h5')
		alignment_hdf_file = os.path.join('/projects/sftp/shahlab/singlecell', jira_ticket, 'alignment', row['library_id'] + '_alignment_metrics.h5')

		if os.path.exists(cn_matrix_file):
			cn_df = pd.read_csv(cn_matrix_file, dtype = {'chr': str})
			dropped_cells = None

		elif os.path.exists(hmmcopy_hdf_file):
			cn_df, dropped_cells = get_cn_matrix_from_hdf(hmmcopy_hdf_file, analysis_ploidy)

			merged_csv = os.path.join(output_dir, '{}_all_metrics_summary.csv'.format(jira_ticket))
			all_metrics_summary_file = os.path.join(output_dir, '{}_all_metrics_summary_classified.csv'.format(jira_ticket))

			get_quality_from_hdf(hmmcopy_hdf_file, alignment_hdf_file, analysis_ploidy, merged_csv)
			classify_metrics(merged_csv, all_metrics_summary_file)

			cn_df = cn_df.drop(columns = 'bin')

		else:
			raise Exception('Unable to find results for ticket {}'.format(jira_ticket))

		# Filter out cells with quality < 0.75
		all_metrics_summary_df = pd.read_csv(all_metrics_summary_file)
		if dropped_cells:
			all_metrics_summary_df = all_metrics_summary_df.drop(index = all_metrics_summary_df.loc[all_metrics_summary_df['cell_id'].isin(dropped_cells)].index)
		cn_df = cn_df.drop(columns = all_metrics_summary_df[all_metrics_summary_df['quality'] < 0.75]['cell_id'])
		cn_list.append(cn_df)

	# Concatenate all copy number matrices together
	cn_matrix = pd.concat(cn_list, axis = 1, join = 'outer')
	cn_matrix = cn_matrix.T.drop_duplicates().T # Get rid of any duplicate columns
	cn_matrix = cn_matrix.set_index(['chr', 'start', 'end', 'width'])

	if os.path.exists(reads_file):
		reads_df = pd.read_csv(reads_file)
	else:
		reads_df = get_reads_from_hdf(hmmcopy_hdf_file, analysis_ploidy)

	# Filter out bins with mappability < 0.99 and write to csv file
	i = reads_df.loc[(reads_df['cell_id'] == reads_df.iloc[0]['cell_id']) & (reads_df['map'] >= 0.99)].index
	cn_matrix = cn_matrix.iloc[i]

	cn_matrix_path = os.path.join(output_dir, 'cn_matrix.csv')
	cn_matrix.to_csv(cn_matrix_path)


if __name__ == "__main__":
    main()