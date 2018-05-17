setwd("~/Documents/workspace/LatentTreeModel/output")
setwd("~/Documents/workspace/LatentTreeModel/output/RG")
setwd("~/Documents/workspace/LatentTreeModel/output/CLRG_all_dists")
setwd("~/Documents/workspace/LatentTreeModel/output/CLRG_local_dists")
library(reshape)
library(lattice)

percent_asym = read.table("percent_asym.tsv",header=TRUE,sep="\t")
percent_asym[percent_asym == "None"] <- NA
percent_asym_ag <- aggregate(recon_accuracy ~ percent_asym, data = percent_asym, mean, na.rm = TRUE, na.action = na.pass)
percent_asym_plot = melt(percent_asym_ag,id=c("percent_asym"))
xyplot(value ~ percent_asym | variable, data=percent_asym_plot, 
       type = "o",
       main = list(label="Performance by Percent Asymmetric",cex=1.5),
       xlab = list(label="Percent Asymmetric",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.05,1.1))
       ))

percent_observed = read.table("percent_observed.tsv",header=TRUE,sep="\t")
percent_observed[percent_observed == "None"] <- NA
percent_observed_ag <- aggregate(recon_accuracy ~ percent_observed, data = percent_observed, mean, na.rm = TRUE, na.action = na.pass)
percent_observed_plot = melt(percent_observed_ag,id=c("percent_observed"))
xyplot(value ~ percent_observed | variable, data=percent_observed_plot, 
       type = "o",
       main = list(label="Performance by Percent Observed",cex=1.5),
       xlab = list(label="Percent Observed",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.05,1.1))
       ))

num_samples = read.table("num_samples.tsv",header=TRUE,sep="\t")
num_samples[num_samples == "None"] <- NA
num_samples_ag <- aggregate(recon_accuracy ~ num_positions, data = num_samples, mean, na.rm = TRUE, na.action = na.pass)
num_samples_plot = melt(num_samples_ag,id=c("num_positions"))
xyplot(value ~ num_positions | variable, data=num_samples_plot, 
       type = "o",
       main = list(label="Performance by Number of Positions",cex=1.5),
       xlab = list(label="Number of Positions",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.05,1.1))
       ))

num_nodes = read.table("num_nodes_2.tsv",header=TRUE,sep="\t")
num_nodes[num_nodes == "None"] <- NA
num_nodes_ag <- aggregate(recon_accuracy ~ num_nodes, data = num_nodes, mean, na.rm = TRUE, na.action = na.pass)
num_nodes_plot = melt(num_nodes_ag,id=c("num_nodes"))
xyplot(value ~ num_nodes | variable, data=num_nodes_plot, 
       type = "o",
       main = list(label="Performance by Number of Nodes",cex=1.5),
       xlab = list(label="Number of Nodes",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

mut_rate = read.table("mut_rate.tsv",header=TRUE,sep="\t")
mut_rate[mut_rate == "None"] <- NA
mut_rate_ag <- aggregate(recon_accuracy ~ mutation_rate, data = mut_rate, mean, na.rm = TRUE, na.action = na.pass)
mut_rate_plot = melt(mut_rate_ag,id=c("mutation_rate"))
xyplot(value ~ mutation_rate | variable, data=mut_rate_plot, 
       type = "o",
       main = list(label="Performance by Mutation Rate",cex=1.5),
       xlab = list(label="Mutation Rate",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

epsilon = read.table("epsilon.tsv",header=TRUE,sep="\t")
epsilon[epsilon == "None"] <- NA
epsilon_ag <- aggregate(recon_accuracy ~ epsilon, data = epsilon, mean, na.rm = TRUE, na.action = na.pass)
epsilon_plot = melt(epsilon_ag,id=c("epsilon"))
xyplot(value ~ epsilon | variable, data=epsilon_plot, 
       type = "o",
       main = list(label="Performance by Epsilon",cex=1.5),
       xlab = list(label="Epsilon",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

tau = read.table("tau.tsv",header=TRUE,sep="\t")
tau[tau == "None"] <- NA
tau_ag <- aggregate(recon_accuracy ~ tau, data = tau, mean, na.rm = TRUE, na.action = na.pass)
tau_plot = melt(tau_ag,id=c("tau"))
xyplot(value ~ as.factor(tau) | variable, data=tau_plot, 
       type = "o",
       main = list(label="Performance by Tau",cex=1.5),
       xlab = list(label="Tau",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

###########################################

tau_numnodes = read.table("tau_numnodes.tsv",header=TRUE,sep="\t")
tau_numnodes[tau_numnodes == "None"] <- NA
tau_numnodes_ag <- aggregate(recon_accuracy ~ tau + num_nodes, data = tau_numnodes, mean, na.rm = TRUE, na.action = na.pass)
tau_numnodes_plot = melt(tau_numnodes_ag,id=c("tau","num_nodes"))
xyplot(value ~ num_nodes | variable, group = tau, data=tau_numnodes_plot, 
       type = "o", auto.key=list(space = "right", columns=1, title="Tau", cex.title=1.25),
       main = list(label="Performance by Number of Nodes + Tau",cex=1.5),
       xlab = list(label="Number of Nodes",cex=1.25), ylab = "",,
       scales=list(
         y=list(limits=c(.05,1.1))
       ))

tau_mutrate = read.table("tau_mutrate.tsv",header=TRUE,sep="\t")
tau_mutrate[tau_mutrate == "None"] <- NA
tau_mutrate_ag <- aggregate(recon_accuracy ~ tau + mutation_rate, data = tau_mutrate, mean, na.rm = TRUE, na.action = na.pass)
tau_mutrate_plot = melt(tau_mutrate_ag,id=c("tau","mutation_rate"))
xyplot(value ~ mutation_rate | variable, group = tau, data=tau_mutrate_plot, 
       type = "o", auto.key=list(space = "right", columns=1, title="Tau", cex.title=1.25),
       main = list(label="Performance by Mutation Rate + Tau",cex=1.5),
       xlab = list(label="Mutation Rate",cex=1.25), ylab = "",
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

epsilon_mutrate = read.table("epsilon_mutrate.tsv",header=TRUE,sep="\t")
epsilon_mutrate[epsilon_mutrate == "None"] <- NA
epsilon_mutrate_ag <- aggregate(recon_accuracy ~ epsilon + mutation_rate, data = epsilon_mutrate, mean, na.rm = TRUE, na.action = na.pass)
epsilon_mutrate_plot = melt(epsilon_mutrate_ag,id=c("epsilon","mutation_rate"))
xyplot(value ~ mutation_rate | variable, group = epsilon, data=epsilon_mutrate_plot, 
       type = "o", auto.key=list(space = "right", columns=1, title="Epsilon", cex.title=1.25),
       main = list(label="Performance by Mutation Rate + Epsilon",cex=1.5),
       xlab = list(label="Mutation Rate",cex=1.25), ylab = "",,
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

epsilon_percent_observed = read.table("epsilon_percent_observed.tsv",header=TRUE,sep="\t")
epsilon_percent_observed[epsilon_percent_observed == "None"] <- NA
epsilon_percent_observed_ag <- aggregate(recon_accuracy ~ epsilon + percent_observed, data = epsilon_percent_observed, mean, na.rm = TRUE, na.action = na.pass)
epsilon_percent_observed_plot = melt(epsilon_percent_observed_ag,id=c("epsilon","percent_observed"))
xyplot(value ~ percent_observed | variable, group = epsilon, data=epsilon_percent_observed_plot, 
       type = "o", auto.key=list(space = "right", columns=1, title="Epsilon", cex.title=1.25),
       main = list(label="Performance by Percent Observed + Epsilon",cex=1.5),
       xlab = list(label="Percent Observed",cex=1.25), ylab = "",,
       scales=list(
         y=list(limits=c(.1,1.1))
       ))

###########################################

# Numnodes runtime
num_nodes_rt = read.table("rt_numnodes.tsv",header=TRUE,sep="\t")
num_nodes_rt_ag <- aggregate(run_time ~ num_nodes, data = num_nodes_rt, mean)
xyplot(run_time ~ factor(num_nodes), data=num_nodes_rt_ag, 
       type = "o",
       main = list(label="Runtime by Number of Nodes",cex=1.5),
       xlab = list(label="Number of Nodes",cex=1.25), ylab = "Runtime (seconds)")


tau = read.table("tau_test.tsv",header=TRUE,sep="\t")
tau_ag <- aggregate(cbind(sibling_sensitivity,sibling_precision,ancestor_sensitivity,ancestor_precision) ~ tau, data = tau, mean, na.rm = TRUE, na.action = na.pass)
tau_plot = melt(tau_ag,id=c("tau"))
xyplot(value ~ tau | variable, data=tau_plot, 
       type = "o", layout = c(4,1),
       main = list(label="Performance by Tau",cex=1.5),
       xlab = list(label="Tau",cex=1.25), ylab = "")
