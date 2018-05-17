args <- commandArgs(TRUE)

library(devtools)

# Update path below
# devtools::install('/Users/hfarahani/Google Drive/Work_synched/SCP_paper/cellscape/inst/extdata')

library(cellscape)

cnv_data_file <- args[1]
sc_annot_file <- args[2]
tree_edges_file <- args[3]

# cnv_data <- read.csv(system.file("extdata", "cnv_data.csv", package = "cellscape"))
cnv_data <- read.csv(cnv_data_file)
# sc_annot <- read.csv(system.file("extdata", "cnv_annots.tsv", package = "cellscape"), sep="\t")
sc_annot <- read.csv(sc_annot_file, sep="\t")
# tree_edges <- read.csv(system.file("extdata", "cnv_tree_edges.csv", package = "cellscape"))
tree_edges <- read.csv(tree_edges_file)

#clone_colours <- data.frame( clone_id = c("TOV2295","OV2295(2)","OV2295"), colour = c("7fc97f", "beaed4", "fdc086"))
clone_colours <- data.frame(clone_id = c("0","1","2"), colour = c("7fc97f", "beaed4", "fdc086"))
col <- unlist(strsplit(str, ", "))
#clone_colours <- data.frame( clone_id = c(paste0("C", 1:11), "0"), colour = c( "#a6cee3" ,"#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c" ,"#fdbf6f", "#ff7f00" ,"#cab2d6" ,"#6a3d9a", "#ffff99" ,"#c0c0c0"))
#clone_colours <- data.frame( clone_id = c(paste0("X", 2:6), "-A"), colour = c( "#a6cee3" ,"#1f78b4", "#b2df8a", "#33a02c", "#fb9a99" ,"#c0c0c0"))
cellscape(cnv_data=cnv_data, tree_edges=tree_edges, sc_annot=sc_annot, width=1900, height=1200, show_warnings=TRUE, clone_colours=clone_colours)
