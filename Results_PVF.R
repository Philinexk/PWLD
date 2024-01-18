pwld_data <- read_excel("Radboud/Third year/Thesis/PWLD_data.xlsx")
pwld_data$Mean_cluster_size1 <- pwld_data$Mean_cluster_size1-1
manual_data <- read_excel("Radboud/Third year/Thesis/manual_clustering.xlsx")

young_pvf <- filter(manual_data, age < 50)
old_pvf <- filter(manual_data, age >= 50)
young_pwld <- filter(pwld_data, age < 50)
old_pwld <- filter(pwld_data, age >= 50)

#MEAN CLUSTER SIZE 1
mean_young_pvf <- mean(young_pvf[['Mean_cluster_size1']])
iqr_young_pvf <- IQR(young_pvf[['Mean_cluster_size1']])
mean_old_pvf <- mean(old_pvf[['Mean_cluster_size1']])
iqr_old_pvf <- IQR(old_pvf[['Mean_cluster_size1']])
mean_young_pwld <- mean(young_pwld[['Mean_cluster_size1']])
iqr_young_pwld <- IQR(young_pwld[['Mean_cluster_size1']])
mean_old_pwld <- mean(old_pwld[['Mean_cluster_size1']])
iqr_old_pwld <- IQR(old_pwld[['Mean_cluster_size1']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young_pvf, mean_old_pvf, mean_young_pwld, mean_old_pwld),
  IQR = c(iqr_young_pvf, iqr_old_pvf, iqr_young_pwld, iqr_old_pwld)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = c("                            Manual", "", "                            PWLD", ""), 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Cluster Size", 
                   xlab = "Scoring System",
                   ylab = "Cluster size in words")
legend("topright", c("Younger Group", "Older Group"), fill=c("lightblue", "lightgreen"))
# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)

#CLUSTERS1 including single-word clusters
mean_young_pvf <- mean(young_pvf[['Clusters1']])
iqr_young_pvf <- IQR(young_pvf[['Clusters1']])
mean_old_pvf <- mean(old_pvf[['Clusters1']])
iqr_old_pvf <- IQR(old_pvf[['Clusters1']])
mean_young_pwld <- mean(young_pwld[['Clusters1']])
iqr_young_pwld <- IQR(young_pwld[['Clusters1']])
mean_old_pwld <- mean(old_pwld[['Clusters1']])
iqr_old_pwld <- IQR(old_pwld[['Clusters1']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young_pvf, mean_old_pvf, mean_young_pwld, mean_old_pwld),
  IQR = c(iqr_young_pvf, iqr_old_pvf, iqr_young_pwld, iqr_old_pwld)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = c("                            Manual", "", "                            PWLD", ""), 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Number of Clusters including Single Word Clusters", 
                   xlab = "Scoring System",
                   ylab = "Number of Clusters")
legend("topright", c("Younger Group", "Older Group"), fill=c("lightblue", "lightgreen"))
# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)

#CLUSTERS2 excluding single-word clusters
mean_young_pvf <- mean(young_pvf[['Clusters2']])
iqr_young_pvf <- IQR(young_pvf[['Clusters2']])
mean_old_pvf <- mean(old_pvf[['Clusters2']])
iqr_old_pvf <- IQR(old_pvf[['Clusters2']])
mean_young_pwld <- mean(young_pwld[['Clusters2']])
iqr_young_pwld <- IQR(young_pwld[['Clusters2']])
mean_old_pwld <- mean(old_pwld[['Clusters2']])
iqr_old_pwld <- IQR(old_pwld[['Clusters2']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young_pvf, mean_old_pvf, mean_young_pwld, mean_old_pwld),
  IQR = c(iqr_young_pvf, iqr_old_pvf, iqr_young_pwld, iqr_old_pwld)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = c("                            Manual", "", "                            PWLD", ""), 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Number of Clusters excluding Single Word Clusters", 
                   xlab = "Scoring System",
                   ylab = "Number of Clusters")
legend("topright", c("Younger Group", "Older Group"), fill=c("lightblue", "lightgreen"))
# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)

#MAXMIMUM CLUSTER LENGTH
mean_young_pvf <- mean(young_pvf[['maximum_cluster_length']])
iqr_young_pvf <- IQR(young_pvf[['maximum_cluster_length']])
mean_old_pvf <- mean(old_pvf[['maximum_cluster_length']])
iqr_old_pvf <- IQR(old_pvf[['maximum_cluster_length']])
mean_young_pwld <- mean(young_pwld[['maximum_cluster_length']])
iqr_young_pwld <- IQR(young_pwld[['maximum_cluster_length']])
mean_old_pwld <- mean(old_pwld[['maximum_cluster_length']])
iqr_old_pwld <- IQR(old_pwld[['maximum_cluster_length']])

summary_data <- data.frame(
  Group = c("Young", "Old"),
  Mean = c(mean_young_pvf, mean_old_pvf, mean_young_pwld, mean_old_pwld),
  IQR = c(iqr_young_pvf, iqr_old_pvf, iqr_young_pwld, iqr_old_pwld)
)
x_coord <- barplot(height = summary_data$Mean, 
                   names.arg = c("                            Manual", "", "                            PWLD", ""), 
                   ylim = c(0, max(summary_data$Mean) + max(summary_data$IQR)), 
                   col = c("lightblue", "lightgreen"), 
                   beside = TRUE, 
                   main = "Mean Maximum Cluster Length", 
                   xlab = "Scoring System",
                   ylab = "Cluster length in words")
legend("topright", c("Younger Group", "Older Group"), fill=c("lightblue", "lightgreen"))
# Add error bars for IQR
arrows(x0 = x_coord, y0 = summary_data$Mean - summary_data$IQR / 2, 
       x1 = x_coord, y1 = summary_data$Mean + summary_data$IQR / 2, 
       angle = 90, code = 3, length = 0.1)


