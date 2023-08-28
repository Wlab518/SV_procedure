mkdir -p /opt/project//qc/Samp9 && cd /opt/project//qc/Samp9 && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && metaWRAP read_qc -1 /opt/project//rawdata_10ge/NGS_Samp9_R1.fastq.gz -2 /opt/project//rawdata_10ge/NGS_Samp9_R2.fastq.gz -o /opt/project//qc/Samp9 && seqkit stats /opt/project//qc/Samp9/NGS_Samp9_R1_val_1.fq.gz -a > /opt/project//qc/Samp9/Samp9_R1_val_1.stat && seqkit stats /opt/project//qc/Samp9/NGS_Samp9_R2_val_2.fq.gz -a > /opt/project//qc/Samp9/Samp9_R2_val_2.stat && conda deactivate && ln -sfn /opt/project//rawdata_10ge/ONT_Samp9.fastq.gz /opt/project//qc/Samp9/ONT_Samp9.fastq.gz && echo This-Work-is-Completed! && touch /opt/project//shell/run_step1.qc.sh/step1.qc.09.sh.Check
