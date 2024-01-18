library(tidyverse)
library(dslabs)
library(tibble)
library(ggbeeswarm)
library(readxl)
library(dplyr)
library(ggplot2)
library(ppcor)
library(tibble)
library(ggbeeswarm)
library(readxl)
library(dplyr)
library(car)
library('corrr')
library(ggcorrplot)
library("FactoMineR")
library("dgof")
library(stargazer)
mean_sd <- function(x){ return (list(ymin=mean(x) -sd(x),y=mean(x), ymax=mean(x))+sd(x))}
qrange <- function(r){return(function(x) list(ymin=quantile(x,(100-r)/200), y=quantile(x,.5), ymax=quantile(x,1-(100-r)/200)))}

manual_data <- read_excel("Radboud/Third year/Thesis/Manual_data.xlsx")
pwld_data <- read_excel("Radboud/Third year/Thesis/PWLD_data.xlsx")
pwld_data$Mean_cluster_size1 <- pwld_data$Mean_cluster_size1-1

data = manual_data #choose one of the two data sets

young <- filter(data, age < 50)
old <- filter(data, age >= 50)

ggplot(PVF_cluster_data, aes(x = Correct_words, y="", color = age >= 50)) +
  geom_quasirandom() +
  labs(x = "Words", y="", color = "Age Groups") +
  scale_color_manual(values = c("FALSE" = "blue", "TRUE" = "green"), 
                     labels = c("FALSE" = "Younger Group","TRUE" = "Older Group")) +
  theme_minimal()

mean(young[['Correct_words']])
sd(young[['Correct_words']])
mean(old[['Correct_words']])
sd(old[['Correct_words']])

#Bootstrap distribution performance (Correct_words)
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['Correct_words']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['Correct_words']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['Correct_words']])
xbar_old <- mean(old[['Correct_words']])
old['Correct_words'] <- old[['Correct_words']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#Mean Cluster Size
mean_young <- mean(young[['Mean_cluster_size1']])
iqr_young <- IQR(young[['Mean_cluster_size1']])
mean_old <- mean(old[['Mean_cluster_size1']])
iqr_old <- IQR(old[['Mean_cluster_size1']])

mean_young
sd(young[['Mean_cluster_size1']])
mean_old
sd(old[['Mean_cluster_size1']])

#Bootstrap distribution Mean_cluster_size1
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['Mean_cluster_size1']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['Mean_cluster_size1']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['Mean_cluster_size1']])
xbar_old <- mean(old[['Mean_cluster_size1']])
old['Mean_cluster_size1'] <- old[['Mean_cluster_size1']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#NUMBER OF CLUSTERS including single-word clusters
#Clusters1
mean_young <- mean(young[['Clusters1']])
iqr_young <- IQR(young[['Clusters1']])
mean_old <- mean(old[['Clusters1']])
iqr_old <- IQR(old[['Clusters1']])

mean_young
sd(young[['Clusters1']])
mean_old
sd(old[['Clusters1']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young, mean_old),
  IQR = c(iqr_young, iqr_old)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = summary_data$Group, 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Number of Clusters including Single Word Clusters", 
                   xlab = "Groups",
                   ylab = "Number of Clusters")

# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)
#Bootstrap distribution Percentage of Clusters (Clusters1)
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['Clusters1']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['Clusters1']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['Clusters1']])
xbar_old <- mean(old[['Clusters1']])
old['Clusters1'] <- old[['Clusters1']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#Clusters2 excluding single-word clusters
mean_young <- mean(young[['Clusters2']])
iqr_young <- IQR(young[['Clusters2']])
mean_old <- mean(old[['Clusters2']])
iqr_old <- IQR(old[['Clusters2']])

mean_young
sd(young[['Clusters2']])
mean_old
sd(old[['Clusters2']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young, mean_old),
  IQR = c(iqr_young, iqr_old)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = summary_data$Group, 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Number of Clusters excluding Single Word Clusters", 
                   xlab = "Groups",
                   ylab = "Number of Clusters")

# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)
#Bootstrap distribution Percentage of Clusters (Clusters2)
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['Clusters2']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['Clusters2']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['Clusters2']])
xbar_old <- mean(old[['Clusters2']])
old['Clusters2'] <- old[['Clusters2']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#MAXIMUM CLUSTER LENGTH
mean_young <- mean(young[['maximum_cluster_length']])
iqr_young <- IQR(young[['maximum_cluster_length']])
mean_old <- mean(old[['maximum_cluster_length']])
iqr_old <- IQR(old[['maximum_cluster_length']])

mean_young
sd(young[['maximum_cluster_length']])
mean_old
sd(old[['maximum_cluster_length']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young, mean_old),
  IQR = c(iqr_young, iqr_old)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = summary_data$Group, 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Maximum Cluster Length", 
                   xlab = "Groups",
                   ylab = "Words")

# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)
#Bootstrap distribution maximum_cluster_length
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['maximum_cluster_length']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['maximum_cluster_length']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['maximum_cluster_length']])
xbar_old <- mean(old[['maximum_cluster_length']])
old['maximum_cluster_length'] <- old[['maximum_cluster_length']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#Strategy
mean_y1 <- mean(young[['Percentage_words1']])
iqr_y1 <- IQR(young[['Percentage_words1']])
mean_o1 <- mean(old[['Percentage_words1']])
iqr_o1 <- IQR(old[['Percentage_words1']])

mean_y2 <- mean(young[['Percentage_words2']])
iqr_y2 <- IQR(young[['Percentage_words2']])
mean_o2 <- mean(old[['Percentage_words2']])
iqr_o2 <- IQR(old[['Percentage_words2']])

mean_y3 <- mean(young[['Percentage_words3']])
iqr_y3 <- IQR(young[['Percentage_words3']])
mean_o3 <- mean(old[['Percentage_words3']])
iqr_o3 <- IQR(old[['Percentage_words3']])

mean_y4 <- mean(young[['Percentage_words4']])
iqr_y4 <- IQR(young[['Percentage_words4']])
mean_o4 <- mean(old[['Percentage_words4']])
iqr_o4 <- IQR(old[['Percentage_words4']])

mean_y5 <- mean(young[['Percentage_words5']])
iqr_y5 <- IQR(young[['Percentage_words5']])
mean_o5 <- mean(old[['Percentage_words5']])
iqr_o5 <- IQR(old[['Percentage_words5']])

mean_y6 <- mean(young[['Percentage_words6']])
iqr_y6 <- IQR(young[['Percentage_words6']])
mean_o6 <- mean(old[['Percentage_words6']])
iqr_o6 <- IQR(old[['Percentage_words6']])

mean_y7 <- mean(young[['Percentage_words7']])
iqr_y7 <- IQR(young[['Percentage_words7']])
mean_o7 <- mean(old[['Percentage_words7']])
iqr_o7 <- IQR(old[['Percentage_words7']])

summary_data <- data.frame(
  Group = c("Young", "Old", "Young", "Old", "Young", "Old", "Young", "Old", "Young", "Old" , "Young", "Old", "Young", "Old"),
  Mean = c(mean_y1, mean_o1, mean_y2, mean_o2, mean_y3, mean_o3, mean_y4, mean_o4, mean_y5, mean_o5, mean_y6, mean_o6, mean_y7, mean_o7),
  IQR = c(iqr_y1, iqr_o1, iqr_y2, iqr_o2, iqr_y3, iqr_o3, iqr_y4, iqr_o4, iqr_y5, iqr_o5, iqr_y6, iqr_o6, iqr_y7, iqr_o7)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = c("          1", "", "          2", "", "          3", "", "          4", "", "          5", "", "          6", "", '          7', ''), 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Percentage of Words in Each Cluster", 
                   xlab = "Cluster size in words",
                   ylab = "Percentage of words")
# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)
legend("topright", legend = c("Younger group", "Older group"), fill = c("lightblue", "lightgreen"))

PVF_cluster_data$small_clusters <- (PVF_cluster_data$Percentage_words1 + PVF_cluster_data$Percentage_words2)
PVF_cluster_data$medium_clusters <- (PVF_cluster_data$Percentage_words3 + PVF_cluster_data$Percentage_words4)
PVF_cluster_data$large_clusters <- (PVF_cluster_data$Percentage_words5 + PVF_cluster_data$Percentage_words6 + PVF_cluster_data$Percentage7)
young <- filter(PVF_cluster_data, age < 50)
old <- filter(PVF_cluster_data, age >= 50)
view(PVF_cluster_data)

#Bootstrap distribution small_clusters
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['small_clusters']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['small_clusters']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['small_clusters']])
xbar_old <- mean(old[['small_clusters']])
old['small_clusters'] <- old[['small_clusters']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#Bootstrap distribution medium_clusters
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['medium_clusters']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['medium_clusters']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['medium_clusters']])
xbar_old <- mean(old[['medium_clusters']])
old['medium_clusters'] <- old[['medium_clusters']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

#Bootstrap distribution large_clusters
sample_young <- function(){ return(
  slice_sample(young,n=nrow(young),replace=TRUE)[['large_clusters']]) }
sample_old <- function(){ return( 
  slice_sample(old,n=nrow(old),replace=TRUE)[['large_clusters']]) }
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
qrange(95)(bs_dist$d_in_means)
#Null-hypothesis testing:
# mean scores are set to be equal for both age groups
xbar_young <-mean(young[['large_clusters']])
xbar_old <- mean(old[['large_clusters']])
old['large_clusters'] <- old[['large_clusters']]-xbar_old+xbar_young
#null hypothesis distribution
bs_dist <- tibble( d_in_means=replicate( 2000, mean( sample_young() ) - mean( sample_old() ) ) )
bs_dist[['extreme']] <- bs_dist[['d_in_means']] >= abs(xbar_young-xbar_old) |
  bs_dist[['d_in_means']] <= - abs(xbar_young-xbar_old)
p_value <- sum(bs_dist[['extreme']])/2000
p_value

# correlation number of correct words with number of clusters including single-word clusters
correlation_result <- cor.test(data[['Correct_words']], data[['Clusters2']])
print(paste0("Correlation (r): ", signif(correlation_result$estimate, 2)))
print(paste0("p-value: ", format(correlation_result$p.value, scientific = TRUE)))

# correlation number of correct words with number of clusters excluding single-word clusters
correlation_result <- cor.test(data[['Correct_words']], data[['Clusters2']])
print(paste0("Correlation (r): ", signif(correlation_result$estimate, 2)))
print(paste0("p-value: ", format(correlation_result$p.value, scientific = TRUE)))
