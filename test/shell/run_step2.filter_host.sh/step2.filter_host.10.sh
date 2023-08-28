cd /opt/project//cleandata && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && minimap2 -a /opt/project/GRCh37_latest_genomic.fna.gz.min /opt/project//qc/Samp10/ONT_Samp10.fastq.gz > /opt/project//cleandata/ONT_Samp10.sam && conda deactivate && cat /opt/project//cleandata/ONT_Samp10.sam | awk '{if($4==0){print $0;}}'|awk '{print "@"$1"\n"$10"\n+\n"$11;}' | gzip > /opt/project//cleandata/ONT_Samp10_filter.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py  /opt/project//cleandata/ONT_Samp10_filter.fastq.gz /opt/project//cleandata/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp10_distribution.txt && mv raeds_distribution.pdf ONT_Samp10_distribution.pdf && conda activate mySVenv_python2 && bowtie2 -x /opt/project/GRCh37_latest_genomic.fna.gz -1 /opt/project//qc/Samp10/NGS_Samp10_R1_val_1.fq.gz -2 /opt/project//qc/Samp10/NGS_Samp10_R2_val_2.fq.gz -S /opt/project//cleandata/NGS_Samp10.sam --threads 20 && awk '{if($4==0){print $1;}}' /opt/project//cleandata/NGS_Samp10.sam | uniq> /opt/project//cleandata/Samp10_id.txt && seqkit grep -f /opt/project//cleandata/Samp10_id.txt /opt/project//qc/Samp10/NGS_Samp10_R1_val_1.fq.gz |gzip > /opt/project//cleandata/NGS_Samp10_filter_1.fastq.gz && seqkit grep -f /opt/project//cleandata/Samp10_id.txt /opt/project//qc/Samp10/NGS_Samp10_R2_val_2.fq.gz |gzip > /opt/project//cleandata/NGS_Samp10_filter_2.fastq.gz && seqkit stats /opt/project//cleandata/NGS_Samp10_filter_1.fastq.gz -a > /opt/project//cleandata/NGS_Samp10_filter_1.stat && seqkit stats /opt/project//cleandata/NGS_Samp10_filter_2.fastq.gz -a > /opt/project//cleandata/NGS_Samp10_filter_2.stat && conda deactivate && rm /opt/project//cleandata/ONT_Samp10.sam /opt/project//cleandata/NGS_Samp10.sam /opt/project//cleandata/Samp10_id.txt && echo This-Work-is-Completed! && touch /opt/project//shell/run_step2.filter_host.sh/step2.filter_host.10.sh.Check
