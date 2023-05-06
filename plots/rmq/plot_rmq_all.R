library(ggplot2)
library(ggthemes)
library(reshape2)
library(scales)

EPSILON <- 1e-9

data_simple <- read.csv("rmq_simple.csv",header=F,sep=",")
data_naive <- read.csv("rmq_naive.csv",header=F,sep=",")
data_block <- read.csv("rmq_block.csv",header=F,sep=",")

to_correct_df <- function(data) {
    total <- nrow(data)
    pt <- data$V1[1:(total/2)]
    qt <- data$V1[((total/2)+1):total]

    df <- data.frame(pt=pt,qt=qt)
    df$n <- seq(2,nrow(df)+1)

    df <- melt(df,id.vars=c("n"))
    df
}

data_simple <- to_correct_df(data_simple)
data_naive <- to_correct_df(data_naive)
data_block <- to_correct_df(data_block)

data_simple$type <- "Simple"
data_naive$type <- "Naive"
data_block$type <- "Block"

df <- merge(data_simple, data_naive, by=c("n", "variable"))
df <- df[, c(1,2,3,5)]
colnames(df) <- c("n", "variable", "Simple", "Naive")
df <- merge(df, data_block, by=c("n", "variable"))
df <- df[, c(1,2,3,4,5)]
colnames(df) <- c("n", "complexity", "Simple", "Naive", "Block")
df <- melt(df, id.vars=c("n", "complexity"))
df$complexity <- as.character(df$complexity)
df$complexity[df$complexity == "pt"] <- "p(N)"
df$complexity[df$complexity == "qt"] <- "q(N)"

pdf("rmq_all.pdf",width=12,height=7)
ggplot(df,aes(x=n,y=value*1000,shape=variable,color=complexity)) +
    geom_point(size=2) +
    geom_line() +
    scale_x_continuous("N") +
    scale_y_continuous("Runtime (ms)", trans=scales::pseudo_log_trans(base = 10)) +
    theme(axis.title=element_text(),axis.title.y=theme_bw()$axis.title.y) +
	scale_color_pander() +
	theme_minimal() +
  	theme(
		legend.position="top",
		legend.title=element_blank(),
		# legend.background = element_rect(fill="gray90"),
		legend.key=element_blank(),
		legend.key.width=unit(0.5,"cm"),
		legend.key.height=unit(0.5,"cm"),
		axis.text.x=element_text(size=14,angle=0,hjust=0.5,vjust=0),
		axis.text.y=element_text(size=14,angle=0,hjust=1),
		axis.title.x = element_text(size=20,angle=0,hjust=.5,vjust=0,face="plain"),
        axis.title.y = element_text(size=20,hjust=.5,vjust=.5,face="plain"),
        # panel.background = element_blank(),
        # panel.grid.major = element_blank(), 
        # panel.grid.minor = element_blank(),
        axis.line = element_line(colour = "black"),
        panel.border = element_rect(colour = "black", fill=NA),
		legend.text=element_text(size=14)) +
	guides(
		color=guide_legend(ncol=4,nrow=1),
		shape=guide_legend(ncol=4,nrow=1)
	) +
	theme(axis.line = element_line(color = 'black'))

