library(ggplot2)
stat <- read.table(file="/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/barplot/s__ER4_sp000765235/input.txt",header=T,check.names=FALSE,sep="\t")
stat$sv_type<-factor(stat$sv_type, levels = c("Deletions", "Insertions", "Duplications", "Translocations", "Inversions"))
stat$Samples<-factor(stat$Samples, levels = c("Samp1","Samp3","Samp4","Samp6","Samp8"))
pdf(file="/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/barplot/s__ER4_sp000765235/s__ER4_sp000765235.pdf",width=8,height=7)
ggplot(stat, aes(sv_type, weight = numbers, fill = Samples)) +
  geom_bar(color = "black", width = .9, position = 'dodge') +
  labs( y = 'SV numbers', x = ' ER4 sp000765235') +
  scale_fill_manual(values=c("Samp1"="white", "Samp3"="white", "Samp4"="white", "Samp6"="gray", "Samp8"="gray" ))+
  geom_text(aes(label=stat$numbers, y=stat$numbers+0.05), position=position_dodge(0.9), vjust=-0.25) +
  guides(fill=FALSE)+
  theme_bw()+theme(panel.grid =element_blank())
dev.off()
