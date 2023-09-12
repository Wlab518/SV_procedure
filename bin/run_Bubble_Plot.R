#source /software_users/liyuejuan/SV_procedure_script/SV_env.txt
#conda activate R3.6

library(ggplot2)
library(RColorBrewer)
library(ggrepel)
library(aplot)

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
