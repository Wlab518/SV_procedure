adata<-read.table("/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/wilcox_test/s__Anaerobutyricum_hallii/input.txt",sep="	",header=T)
adata$wilcox.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:8]))==0){return(NA)} else{ wilcox.test(as.numeric(x[2:5]),as.numeric(x[6:8]),alternative="less",paired=FALSE,conf.int=FALSE)$p.value})
adata$t_test.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:8]))==0){return(NA)} else{ t.test(as.numeric(x[2:5]),as.numeric(x[6:8]),alternative="less",paired=FALSE,conf.int=FALSE)$p.value})
write.table(adata,file="/data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test/result_stat/wilcox_test/s__Anaerobutyricum_hallii/test_result.txt",row.names=F,sep="	")
