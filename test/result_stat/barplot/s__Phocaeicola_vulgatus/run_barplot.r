library(ggplot2)
stat <- read.table(file="/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/barplot/s__Phocaeicola_vulgatus/input.txt",header=T,check.names=FALSE,sep="\t")
stat$sv_type<-factor(stat$sv_type, levels = c("Deletions", "Insertions", "Duplications", "Translocations", "Inversions"))
stat$Samples<-factor(stat$Samples, levels = c("Samp2","Samp3","Samp4","Samp7","Samp8","Samp9","Samp10"))
pdf(file="/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/barplot/s__Phocaeicola_vulgatus/s__Phocaeicola_vulgatus.pdf",width=8,height=7)
ggplot(stat, aes(sv_type, weight = numbers, fill = Samples)) +
  geom_bar(color = "black", width = .9, position = 'dodge') +
  labs( y = 'SV numbers', x = ' Phocaeicola vulgatus') +
  scale_fill_manual(values=c("Samp2"="white", "Samp3"="white", "Samp4"="white", "Samp7"="gray", "Samp8"="gray", "Samp9"="gray", "Samp10"="gray" ))+
  geom_text(aes(label=stat$numbers, y=stat$numbers+0.05), position=position_dodge(0.9), vjust=-0.25) +
  guides(fill=FALSE)+
  theme_bw()+theme(panel.grid =element_blank())
dev.off()
