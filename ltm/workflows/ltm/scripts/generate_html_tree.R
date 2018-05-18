args <- commandArgs(TRUE)

# library(devtools)

# Update path below
# devtools::install('/Users/hfarahani/Google Drive/Work_synched/SCP_paper/cellscape/inst/extdata')

# source("https://bioconductor.org/biocLite.R")
# biocLite("cellscape")

options(error=traceback)

library(cellscape)

sc_annot_file <- args[1]
tree_edges_file <- args[2]
cnv_data_file <- args[3]

cnv_data <- read.csv(cnv_data_file)
sc_annot <- read.csv(sc_annot_file, sep="\t")
tree_edges <- read.csv(tree_edges_file)

clone_colours <- data.frame(clone_id = c("0","1","2"), colour = c("7fc97f", "beaed4", "fdc086"))

cellscape(cnv_data=cnv_data, tree_edges=tree_edges, sc_annot=sc_annot, width=1900, height=1200, show_warnings=TRUE, clone_colours=clone_colours)
