import os
import argparse
import glob
from subprocess import call

path = os.getcwd()

def main(infile, sfile):

    ###################1.barplot#####################
    with open(infile,'r') as f:
        file_list = [line.strip().split('\t') for line in f.readlines()]
    
    data_dict = {}
    for i in file_list[1:]:
        data_dict.setdefault(i[0], []).extend(i[1:])

    with open(sfile,'r') as f1:
        strain_list = [line.strip() for line in f1.readlines()]
    for strain in strain_list:
        stat_dict = {}
        color_dict = {}
        samp_list = []
        index_list = {}
        for samp in data_dict.keys():
            #outp = os.system('$(readlink -f {0}/SVs/{1}/query_{2}.*_run_output/query_*_run.summary.txt)'.format(path, strain, samp))
            #outp = os.path.abspath('{0}/SVs/{1}/query_{2}.*_run_output/query_*_run.summary.txt'.format(path, strain, samp))
            outp = glob.glob(r'{0}/SVs/{1}/query_{2}.*_run_output/query_*_run.summary.txt'.format(path, strain, samp))
            if outp:
                samp_list.append(samp)
                color_dict.setdefault(data_dict[samp][-1], []).append(samp)
                with open(outp[0],'r') as g:
                    indata = [line.strip().split('\t') for line in g.readlines()]
                for t in indata[1:]:
                    if t == ['']:
                        pass
                    else:
                        stat_dict.setdefault(samp + '-' + t[0], []).append(t[1])
                        stat_dict.setdefault(samp + '-' + t[0], []).append(data_dict[samp][-1])

        call('mkdir -p {0}/result_stat/barplot/{1}'.format(path, strain), shell=True)
        with open('{0}/result_stat/barplot/{1}/input.txt'.format(path, strain),'w') as o:
            o.write("Samples" + '\t' + "numbers" + '\t' + "sv_type" + '\t' + "group" + '\n')
            for key, val in stat_dict.items():
                if key.split('-')[1] != "Total_SVs":
                    o.write(key.split('-')[0] + '\t' + val[0] + '\t' + key.split('-')[1] + '\t' + val[1] + '\n')
        with open('{0}/result_stat/barplot/{1}/run_barplot.r'.format(path, strain),'w') as o1:
            o1.write('library(ggplot2)\n')
            o1.write('library(ggpubr)\n')
            o1.write('stat <- read.table(file="{0}/result_stat/barplot/{1}/input.txt",header=T,check.names=FALSE,sep="\\t")\n'.format(path, strain))
            o1.write('stat$sv_type<-factor(stat$sv_type, levels = c("Deletions", "Insertions", "Duplications", "Translocations", "Inversions"))\n')
            o1.write('stat$Samples<-factor(stat$Samples, levels = c("')
            smp_list = []
            for lis in color_dict.values():
                for sap in lis:
                    smp_list.append(sap)
            o1.write('{}'.format('","'.join(smp_list)))
            o1.write('"))\n')
            o1.write('pdf(file="{0}/result_stat/barplot/{1}/{1}.pdf",width=8,height=7)\n'.format(path, strain))
            o1.write('ggplot(stat, aes(x = sv_type, y = numbers, fill = group, color = "black")) +\n')
            o1.write('  stat_summary(fun = "mean", geom = "bar", alpha = .7, position = position_dodge(0.95)) +\n')
            o1.write('  stat_summary(fun = "mean", geom = "point", position = position_dodge(0.95), size = 1) +\n')
            o1.write('  stat_summary(fun.data = "mean_cl_normal", geom = "errorbar", position = position_dodge(0.95), width = .2) +\n')
            o1.write('  labs( y = \'SV numbers\', x = \'{0}\') +\n'.format(strain.replace("s__", " ").replace("_", " ")))
            #o1.write(coord_cartesian(ylim = c(0, 25))+\n')
            #o1.write('  scale_fill_brewer(palette = "Set3")+\n')
            o1.write('  scale_fill_manual(values=c("white", "gray")) +\n')
            o1.write('  scale_color_manual(values=c("black")) +\n')
            #o1.write('  geom_text(aes(label=stat$numbers, y=stat$numbers+0.05), position=position_dodge(0.9), vjust=-0.25) +\n')
            #o1.write('  annotate(geom="text", x=1, y=7, label="reference")+\n')
            o1.write('  guides(color=\'none\') +\n')
            o1.write('  theme_bw()+theme(panel.grid =element_blank())\n')
            o1.write('dev.off()\n')

        ###################2.wilcox#####################
        call('mkdir -p {0}/result_stat/wilcox_test/{1}'.format(path, strain), shell=True)
        table_dict = {}
        with open('{0}/result_stat/wilcox_test/{1}/input.txt'.format(path, strain),'w') as o2:
            #print(samp_list, stat_dict)
            o2.write("X" + '\t' + '\t'.join(samp_list) + '\n')
            for smp in samp_list:
                k = 0
                for key, val in stat_dict.items():
                    if key.split("-")[0] == smp:
                        k += 1
                        gro = val[1]
                        if k == 1:
                            if gro not in index_list.keys():
                                index_list[gro] = 0
                        table_dict.setdefault(key.split("-")[1], []).append(val[0])
                index_list[gro] = index_list[gro] + 1    
            for k, v in table_dict.items():
                if k == "Total_SVs":
                    pass
                else:
                    o2.write(k + '\t' + '\t'.join(v) + '\n')
        with open('{0}/result_stat/wilcox_test/{1}/run_test.r'.format(path, strain),'w') as o3:
            index = list(index_list.values())
            o3.write('adata<-read.table("{0}/result_stat/wilcox_test/{1}/input.txt",sep="	",header=T)\n'.format(path, strain))
            if index[0]+1 == 2:
                o3.write('adata$wilcox.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:{0}]))==0){{return(NA)}} else{{ wilcox.test(as.numeric(x[2]),as.numeric(x[{1}:{0}]),alternative="two.sided",paired=FALSE,conf.int=FALSE)$p.value}})\n'.format(str(index[0]+index[1]+1), str(index[0]+2)))
            elif index[0]+2 == index[0]+index[1]+1:
                o3.write('adata$wilcox.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:{0}]))==0){{return(NA)}} else{{ wilcox.test(as.numeric(x[2:{1}]),as.numeric(x[{0}]),alternative="two.sided",paired=FALSE,conf.int=FALSE)$p.value}})\n'.format(str(index[0]+index[1]+1), str(index[0]+1)))
            else:
                o3.write('adata$wilcox.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:{0}]))==0){{return(NA)}} else{{ wilcox.test(as.numeric(x[2:{1}]),as.numeric(x[{2}:{0}]),alternative="two.sided",paired=FALSE,conf.int=FALSE)$p.value}})\n'.format(str(index[0]+index[1]+1), str(index[0]+1), str(index[0]+2)))
                o3.write('adata$t_test.pvalue <- apply(adata,1,function(x) if(sum(as.numeric(x[2:{0}]))==0){{return(NA)}} else{{ t.test(as.numeric(x[2:{1}]),as.numeric(x[{2}:{0}]),alternative="two.sided",paired=FALSE,conf.int=FALSE)$p.value}})\n'.format(str(index[0]+index[1]+1), str(index[0]+1), str(index[0]+2)))
            o3.write('write.table(adata,file="{0}/result_stat/wilcox_test/{1}/test_result.txt",row.names=F,sep="	")\n'.format(path, strain))


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="run procedure",
        epilog="Example: python get_barplot_wilcox_script.py sample_info.txt bacterial_strain.list")
    parser.add_argument('infile', help='input file: sample_info.txt')
    parser.add_argument('sfile', help='output file: bacterial_strain.list')
    args = parser.parse_args()

    main(args.infile, args.sfile)
