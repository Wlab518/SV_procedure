#BiocManager::install('clusterProfiler')
library(clusterProfiler)

#载入背景文件
kegg_anno <- read.delim("kegg.annotate.ko.rlt", colClasses = 'character')
#载入目标基因列表
gene_select <- read.delim("foreground_genes.txt", stringsAsFactors = FALSE)$query_name
#KEGG富集分析
kegg_rich <- enricher(gene = gene_select,
                      TERM2GENE = kegg_anno[c("KO_number","query_name")],
                      TERM2NAME = kegg_anno[c("KO_number", "pathway")],
                      pvalueCutoff = 1,
                      pAdjustMethod = 'BH',#"holm", "hochberg", "hommel", "bonferroni", "BH", "BY", "fdr", "none"
                      qvalueCutoff = 1,
		      minGSSize = 10, 
                      maxGSSize = 1000
                      )

write.table(as.data.frame(kegg_rich),"kegg_enrich.txt",sep="\t",row.names =F,quote=F)

#可视化
#barplot(kegg_rich,showCategory=20,title="TOP 20 of KEGG Enrichment")
#dotplot(kegg_rich,title="Enrichment KEGG_dot")

#查看特定通路图
#hsa04750 <- pathview(gene.data = geneList,pathway.id = "hsa04750", species = "hsa",limit = list(gene=max(abs(geneList)), cpd=1))

