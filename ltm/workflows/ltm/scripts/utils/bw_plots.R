setwd("~/Documents/workspace/LatentTreeModel/output")
library(lattice)
library(plyr)

# *** By methods ***

thing = read.table("all_results.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy_MS ~ as.factor(mut_rate) | as.factor(method), data = thing, horizontal = FALSE)
bwplot(recon_accuracy_RF ~ as.factor(method), data = thing, horizontal = FALSE)
bwplot(recon_accuracy_MMS ~ as.factor(method), data = thing, horizontal = FALSE)
bwplot(family_recall ~ as.factor(method), data = thing, horizontal = FALSE)
bwplot(family_precision ~ as.factor(method), data = thing, horizontal = FALSE)
bwplot(family_correctness ~ as.factor(method), data = thing, horizontal = FALSE)
bwplot(recon_run_time ~ method, data = thing, horizontal = FALSE)

homoplasy_rate = read.table("homoplasy_rate.tsv",header=TRUE,sep="\t") 
homoplasy_rate$method = factor(homoplasy_rate$method,levels = c(1,2,3,4,5),labels = c("RGv1", "RGv2", "CLRG", "MST","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(homoplasy_rate) | as.factor(method), data = homoplasy_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(homoplasy_rate) | as.factor(method), data = homoplasy_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(homoplasy_rate) | as.factor(method), data = homoplasy_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(homoplasy_rate) | as.factor(method), data = homoplasy_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(homoplasy_rate) | as.factor(method), data = homoplasy_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(homoplasy_rate) | as.factor(method), data = homoplasy_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

backmut_rate = read.table("backmut_rate.tsv",header=TRUE,sep="\t") 
backmut_rate$method = factor(backmut_rate$method,levels = c(1,2,3,4,5),labels = c("RGv1", "RGv2", "CLRG", "MST","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(backmut_rate) | as.factor(method), data = backmut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(backmut_rate) | as.factor(method), data = backmut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(backmut_rate) | as.factor(method), data = backmut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(backmut_rate) | as.factor(method), data = backmut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(backmut_rate) | as.factor(method), data = backmut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(backmut_rate) | as.factor(method), data = backmut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

mut_rate = read.table("mut_rate.tsv",header=TRUE,sep="\t") 
mut_rate$method = factor(mut_rate$method,levels = c(1,2,3,4,5),labels = c("RGv1", "RGv2", "CLRG", "MST","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(mut_rate) | as.factor(method), data = mut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(mut_rate) | as.factor(method), data = mut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(mut_rate) | as.factor(method), data = mut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(mut_rate) | as.factor(method), data = mut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(mut_rate) | as.factor(method), data = mut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(mut_rate) | as.factor(method), data = mut_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

percent_asym = read.table("percent_asym.tsv",header=TRUE,sep="\t") 
percent_asym$method = factor(percent_asym$method,levels = c(1,2,3,7,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Parsimony + Edge Contraction","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(percent_asym) | as.factor(method), data = percent_asym, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(percent_asym) | as.factor(method), data = percent_asym, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(percent_asym) | as.factor(method), data = percent_asym, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(percent_asym) | as.factor(method), data = percent_asym, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(percent_asym) | as.factor(method), data = percent_asym, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(percent_asym) | as.factor(method), data = percent_asym, horizontal = FALSE, layout = c(5,1), xlab = list(label="Percent Asymmetric",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

num_pos = read.table("num_pos.tsv",header=TRUE,sep="\t")
num_pos$method = factor(num_pos$method,levels = c(1,2,3,7,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Parsimony + Edge Contraction","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(ancestor_recall ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(ancestor_precision ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(sibling_recall ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(sibling_precision ~ as.factor(num_positions) | as.factor(method), data = num_pos, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Positions",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

dropout_rate = read.table("dropout_rate.tsv",header=TRUE,sep="\t")
dropout_rate$method = factor(dropout_rate$method,levels = c(1,2,3,7,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Parsimony + Edge Contraction","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(ancestor_recall ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(ancestor_precision ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(sibling_recall ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(sibling_precision ~ as.factor(dropout_rate) | as.factor(method), data = dropout_rate, horizontal = FALSE, layout = c(5,1), xlab = list(label="Dropout Rate",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

num_leaf_nodes = read.table("num_nodes.tsv",header=TRUE,sep="\t")
num_leaf_nodes$method = factor(num_leaf_nodes$method,levels = c(1,2,3,7,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Parsimony + Edge Contraction","Neighbour Joining"))
bwplot(recon_accuracy_MS ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy (MS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_RF ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy (RF)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_accuracy_MMS ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy (MMS)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_recall ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Family Recall",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_precision ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Family Precision",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(family_correctness ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Family Correctness",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(ancestor_recall ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(ancestor_precision ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(sibling_recall ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(sibling_precision ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))
bwplot(recon_run_time ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_leaf_nodes, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Runtime (s)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))


num_nodes_all = read.table("num_nodes_all.tsv",header=TRUE,sep="\t")
num_nodes_all$method = factor(num_nodes_all$method,levels = c(1,2,3,4,6),labels = c("RG", "CLRG", "Chow-Liu Tree", "Neighbour Joining", "Mr Bayes"))
bwplot(recon_accuracy ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_all, horizontal = FALSE, layout = c(5,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Reconstruction Accuracy",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

num_nodes_no_bayes = read.table("num_nodes_no_bayes.tsv",header=TRUE,sep="\t")
num_nodes_no_bayes$method = factor(num_nodes_no_bayes$method,levels = c(1,2,3,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Neighbour Joining"))
bwplot(recon_run_time ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_no_bayes, horizontal = FALSE, layout = c(4,1), xlab = list(label="Number of Leaf Nodes",cex=2), ylab = list(label="Runtime (s)",cex=2), scales=list(x=list(cex=1),y=list(cex=1.5)))

percent_obs_tot_fixed = read.table("percent_obs_tot_fixed.tsv",header=TRUE,sep="\t")
percent_obs_tot_fixed$method = factor(percent_obs_tot_fixed$method,levels = c(1,2,3,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Neighbour Joining"))
bwplot(recon_accuracy ~ as.factor(percent_observed) | as.factor(method), data = percent_obs_tot_fixed, horizontal = FALSE, layout = c(4,1), xlab = "Percent Observed (out of 256 leaves)", ylab = "Reconstruction Accuracy")

percent_obs_obs_fixed = read.table("percent_obs_obs_fixed.tsv",header=TRUE,sep="\t")
percent_obs_obs_fixed$method = factor(percent_obs_obs_fixed$method,levels = c(1,2,3,4),labels = c("RG", "CLRG", "Chow-Liu Tree", "Neighbour Joining"))
bwplot(recon_accuracy ~ as.factor(percent_observed) | as.factor(method), data = percent_obs_obs_fixed, horizontal = FALSE, layout = c(4,1), xlab = "Percent Observed (32 observed, total number varied)", ylab = "Reconstruction Accuracy")

defaults = num_muts[num_muts$num_mutations == 4,]
bwplot(recon_accuracy ~ as.factor(num_mutations) | as.factor(method), data = defaults, horizontal = FALSE, layout = c(5,1), xlab = "Number of Mutations", ylab = "Reconstruction Accuracy")
bwplot(ancestor_sensitivity ~ as.factor(num_mutations) | as.factor(method), data = defaults, horizontal = FALSE, layout = c(5,1), xlab = "Number of Mutations", ylab = "Ancestor Sensitivity")
bwplot(ancestor_precision ~ as.factor(num_mutations) | as.factor(method), data = defaults, horizontal = FALSE, layout = c(5,1), xlab = "Number of Mutations", ylab = "Ancestor Precision")
bwplot(sibling_sensitivity ~ as.factor(num_mutations) | as.factor(method), data = defaults, horizontal = FALSE, layout = c(5,1), xlab = "Number of Mutations", ylab = "Sibling Sensitivity")
bwplot(sibling_precision ~ as.factor(num_mutations) | as.factor(method), data = defaults, horizontal = FALSE, layout = c(5,1), xlab = "Number of Mutations", ylab = "Sibling Precision")

bwplot(recon_accuracy ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_all, horizontal = FALSE, layout = c(5,1), xlab = "Number of Leaf Nodes", ylab = "Reconstruction Accuracy")
bwplot(ancestor_sensitivity ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_all, horizontal = FALSE, layout = c(5,1), xlab = "Number of Leaf Nodes", ylab = "Ancestor Sensitivity")
bwplot(ancestor_precision ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_all, horizontal = FALSE, layout = c(5,1), xlab = "Number of Leaf Nodes", ylab = "Ancestor Precision")
bwplot(sibling_sensitivity ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_all, horizontal = FALSE, layout = c(5,1), xlab = "Number of Leaf Nodes", ylab = "Sibling Sensitivity")
bwplot(sibling_precision ~ as.factor(num_leaf_nodes) | as.factor(method), data = num_nodes_all, horizontal = FALSE, layout = c(5,1), xlab = "Number of Leaf Nodes", ylab = "Sibling Precision")



#########################################################################################################################

epsilon_percent_obs_clrg = read.table("CLRG/epsilon_percent_obs.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy ~ factor(epsilon) | factor(percent_observed), data = epsilon_percent_obs, horizontal = FALSE)

epsilon = epsilon_percent_obs[epsilon_percent_obs$percent_observed == 100,]
bwplot(recon_accuracy ~ factor(epsilon), data = epsilon, horizontal = FALSE)

tau = read.table("tau.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy ~ factor(tau), data = tau, horizontal = FALSE)

epsilon = read.table("epsilon_2.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy ~ factor(epsilon), data = epsilon, horizontal = FALSE)

percent_observed_tot_fixed = read.table("percent_observed_tot_fixed.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy ~ factor(percent_observed), data = percent_observed_tot_fixed, horizontal = FALSE)

percent_observed_obs_fixed = read.table("percent_observed_obs_fixed.tsv",header=TRUE,sep="\t")
percent_observed_obs_fixed_small = read.table("percent_observed_obs_fixed_small.tsv",header=TRUE,sep="\t")
percent_observed_obs_fixed_all = rbind(percent_observed_obs_fixed,percent_observed_obs_fixed_small)
bwplot(recon_accuracy ~ factor(percent_observed), data = percent_observed_obs_fixed_all, horizontal = FALSE)

epsilon_num_muts = read.table("epsilon_num_muts.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy ~ factor(epsilon) | factor(num_mutations), data = epsilon_num_muts, horizontal = FALSE)


########## PRESENTATION STUFF ##########

num_samples_clrg = read.table("CLRG/num_samples.tsv",header=TRUE,sep="\t")
num_samples_rg = read.table("RG/num_samples.tsv",header=TRUE,sep="\t")
num_samples = rbind(num_samples_clrg,num_samples_rg)
num_samples$method = factor(num_samples$method, levels=c(1,2), labels=c("RG", "CLRG"))
bwplot(recon_accuracy ~ factor(method) | factor(num_positions), data = num_samples, horizontal = FALSE, layout = c(5,1), do.out = FALSE,
       par.settings = list( box.umbrella=list(col= c("red", "blue")), box.dot=list(col= c("red", "blue")), box.rectangle = list(col= c("red", "blue"))))

num_nodes_clrg = read.table("CLRG/num_nodes.tsv",header=TRUE,sep="\t")
num_nodes_rg = read.table("RG/num_nodes.tsv",header=TRUE,sep="\t")
num_nodes = rbind(num_nodes_clrg,num_nodes_rg)
num_nodes$method = factor(num_nodes$method, levels=c(1,2), labels=c("RG", "CLRG"))
num_nodes = num_nodes[num_nodes$num_nodes != 1023,]
bwplot(recon_accuracy ~ factor(method) | factor(num_nodes), data = num_nodes, horizontal = FALSE, layout = c(7,1), do.out = FALSE,
       par.settings = list( box.umbrella=list(col= c("red", "blue")), box.dot=list(col= c("red", "blue")), box.rectangle = list(col= c("red", "blue"))))
bwplot(recon_run_time + score_run_time ~ factor(method) | factor(num_nodes), data = num_nodes, horizontal = FALSE, layout = c(7,1), do.out = FALSE,
       par.settings = list( box.umbrella=list(col= c("red", "blue")), box.dot=list(col= c("red", "blue")), box.rectangle = list(col= c("red", "blue"))))

percent_asym_clrg = read.table("CLRG/percent_asym.tsv",header=TRUE,sep="\t")
percent_asym_rg = read.table("RG/percent_asym.tsv",header=TRUE,sep="\t")
percent_asym = rbind(percent_asym_clrg,percent_asym_rg)
percent_asym$method = factor(percent_asym$method, levels=c(1,2), labels=c("RG", "CLRG"))
bwplot(recon_accuracy ~ factor(method) | factor(percent_asym), data = percent_asym, horizontal = FALSE, layout = c(10,1), do.out = FALSE,
       par.settings = list( box.umbrella=list(col= c("red", "blue")), box.dot=list(col= c("red", "blue")), box.rectangle = list(col= c("red", "blue"))))

percent_obs_tot_fixed_clrg = read.table("CLRG/percent_obs_tot_fixed.tsv",header=TRUE,sep="\t")
bwplot(recon_accuracy ~ factor(percent_asym), data = percent_obs_tot_fixed_clrg, horizontal = FALSE)

tau_percent_obs_clrg = read.table("CLRG/tau_percent_obs.tsv",header=TRUE,sep="\t")
tau_clrg = tau_percent_obs_clrg[tau_percent_obs_clrg$percent_observed == 100,]

percent_obs_clrg = tau_percent_obs_clrg[tau_percent_obs_clrg$tau == 1,]
percent_obs_rg = read.table("RG/percent_obs.tsv",header=TRUE,sep="\t")
percent_obs = rbind(percent_obs_clrg,percent_obs_rg)
percent_obs$method = factor(percent_obs$method, levels=c(1,2), labels=c("RG", "CLRG"))
bwplot(recon_accuracy ~ factor(method) | factor(percent_observed), data = percent_obs, horizontal = FALSE, layout = c(9,1), do.out = FALSE,
       par.settings = list( box.umbrella=list(col= c("red", "blue")), box.dot=list(col= c("red", "blue")), box.rectangle = list(col= c("red", "blue"))))