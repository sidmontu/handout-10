library(ggplot2)
library(ggthemes)
library(reshape2)

data <- read.csv("rmq_naive.csv",header=F,sep=",")

total <- nrow(data)

pt <- data$V1[1:(total/2)]
qt <- data$V1[((total/2)+1):total]

df <- data.frame(pt=pt,qt=qt)
df$n <- seq(2,nrow(df)+1)

df <- melt(df,id.vars=c("n"))

pdf("rmq_naive.pdf",width=7,height=4)
ggplot(df,aes(x=n,y=value,color=variable)) +
    geom_point() +
    geom_line() +
    scale_x_continuous("N") +
    scale_y_continuous("Runtime x 1000") +
    scale_color_pander() +
    theme_bw()

