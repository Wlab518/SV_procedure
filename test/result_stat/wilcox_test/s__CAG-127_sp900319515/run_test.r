adata<-read.table("/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/wilcox_test/s__CAG-127_sp900319515/input.txt",sep="	",header=T)
adata$wilcox.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:6]))==0){return(NA)} else{ wilcox.test(as.numeric(x[2:5]),as.numeric(x[6]),alternative="two.sided",paired=FALSE,conf.int=FALSE)$p.value})
write.table(adata,file="/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/wilcox_test/s__CAG-127_sp900319515/test_result.txt",row.names=F,sep="	")
