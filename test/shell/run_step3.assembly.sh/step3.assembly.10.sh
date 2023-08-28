mkdir -p /opt/project//assembly/Samp10/quast && cd /opt/project//assembly/Samp10/ && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && metaspades.py -1 /opt/project//cleandata/NGS_Samp10_filter_1.fastq.gz -2 /opt/project//cleandata/NGS_Samp10_filter_2.fastq.gz  --nanopore /opt/project//cleandata/ONT_Samp10_filter.fastq.gz -o /opt/project//assembly/Samp10 && quast /opt/project//assembly/Samp10/scaffolds.fasta -o /opt/project//assembly/Samp10/quast --no-plots --no-html && conda deactivate && echo This-Work-is-Completed! && touch /opt/project//shell/run_step3.assembly.sh/step3.assembly.10.sh.Check
