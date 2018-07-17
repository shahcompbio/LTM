options(stringsAsFactors = FALSE)

library(randomForest)

args <- commandArgs(TRUE)

input <- read.csv(args[1])
output <- args[2]
model <- readRDS("/genesis/shahlab/danlai/SC-1041/dlpplus_model_201805311021.rds")

selected <- c('percent_duplicate_reads', 'total_mapped_reads', 'total_duplicate_reads', 'standard_deviation_insert_size', 'MSRSI_non_integerness', 'MBRSI_dispersion_non_integerness', 'MBRSM_dispersion', 'autocorrelation_hmmcopy', 'cv_hmmcopy', 'mad_hmmcopy', 'total_halfiness', 'scaled_halfiness', 'mean_state_mads', 'mean_state_vars', 'breakpoints', 'mean_copy', 'state_mode', 'loglikehood')
if (!all(selected %in% colnames(input))) {
	print("Missing feature column, cannot classify")
	missing <- setdiff(selected, colnames(input))
	stop(missing)
}

input$quality <- predict(model, newdata = input, type = "prob")[, "good"]
input$quality[is.na(input$quality)] <- 0
write.csv(input, file = output, quote = FALSE, row.names = FALSE)
