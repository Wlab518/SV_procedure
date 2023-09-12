library(ggplot2)
library(RColorBrewer)
library(ggrepel)
library(aplot)
library(tidyverse)
library(dplyr)

dat<-read.table(file="input.txt",header=T,quote = "",sep="\t")
data<-dat[order(dat$KEGG_level1),]
data$KEGG_level3 <- factor(data$KEGG_level3, levels=data$KEGG_level3[order(data$KEGG_level1, decreasing=FALSE)])
pdf("Bubble_Plot.pdf",width=10,height=10)
p1<-ggplot(data,aes(x=FoldEnrichment,y=KEGG_level3))+
  geom_point(aes(size=GeneNumber,color=-log10(p.adj)),alpha=0.6)+
  scale_size(range=c(1,12))+
  scale_colour_gradient(low="blue",high="red")+
  #scale_color_brewer(palette = "Accent")+
  theme_bw()+
  theme(axis.title.y = element_blank(),axis.text.y=element_blank())+
  geom_text_repel(data = data[data$p.adj<0.05,],aes(label = ID), size = 3, segment.color = "black", show.legend = FALSE)

p2<-ggplot(data,aes(x=x,y=KEGG_level3))+
  geom_tile(aes(fill=KEGG_level1))+
  scale_x_continuous(expand = c(0,0))+
  theme(panel.background = element_blank(),
        axis.ticks = element_blank(),
        axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        #axis.text.y = element_blank(),
        legend.position = "left",
        legend.title = element_blank())+
	ylab("KEGG Pathway")
  #scale_fill_manual(values = c("green","blue","red"))
p1%>%
  insert_left(p2,width = 0.05)
dev.off()

pdf("bar.pdf", width=10,height=10)
ggplot(data,aes(x=GeneNumber,y=KEGG_level3, fill=KEGG_level1))+
	geom_bar(stat="identity", width=0.8)+
	geom_text(aes(label=GeneNumber),size=4, hjust=-0.5)+
	labs(x="Number of genes", y="KEGG Pathway")+
	theme_bw()+
	theme(panel.background = element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),legend.title = element_blank())
dev.off()

pdf("circos.pdf", width=10,height=10)
# Set a number of 'empty bar' to add at the end of each group
empty_bar <- 1
to_add <- data.frame(matrix(NA, empty_bar*nlevels(as.factor(data$KEGG_level1)), ncol(data)))
colnames(to_add) <- colnames(data)
to_add$KEGG_level1 <- rep(levels(as.factor(data$KEGG_level1)), each=empty_bar)
data <- rbind(data, to_add)
data <- data %>% arrange(KEGG_level1)
data$id <- seq(1, nrow(data))
 
# Get the name and the y position of each label
label_data <- data
number_of_bar <- nrow(label_data)
angle <- 90 - 360 * (label_data$id-0.5) /number_of_bar    
label_data$hjust <- ifelse( angle < -90, 1, 0)
label_data$angle <- ifelse(angle < -90, angle+180, angle)

base_data <- data %>% group_by(KEGG_level1) %>% 
  summarize(start=min(id), end=max(id) - empty_bar) %>% 
  rowwise() %>% mutate(title=mean(c(start, end)))

# Make the plot
ggplot(data, aes(x=as.factor(id), y=GeneNumber, fill=KEGG_level1)) + 
  geom_bar(stat="identity", alpha=0.5) +
  ylim(-100,120) +
  theme_minimal() +
  theme(
    legend.position = c(0.5,0.5),
    legend.title = element_blank(),
    axis.text = element_blank(),
    axis.title = element_blank(),
    panel.grid = element_blank(),
    plot.margin = unit(rep(-1,4), "cm") 
  ) +
  coord_polar() +
  geom_text(data=data, aes(x=id, y=GeneNumber+10, label=ID), 
            color="black", fontface="bold",alpha=0.6, size=2.5, 
            angle= label_data$angle, inherit.aes = FALSE )+
  geom_segment(data=data, aes(x = id, y = -5, xend = -1, yend = -5),
              colour = "gray", alpha=0.8, size=0.6 , inherit.aes = FALSE )+
  #geom_label(data=data, aes(x=id, y = -10, label=GeneNumber),alpha=0, size=2.5)
  geom_text(data=data, aes(x=id, y = -10, label=GeneNumber),
            alpha=0.8, colour = "black", size=2.5,fontface="bold", inherit.aes = FALSE)
 
dev.off()

