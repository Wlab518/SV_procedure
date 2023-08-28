mkdir -p /opt/project//qc/Samp3 && cd /opt/project//qc/Samp3 && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && metaWRAP read_qc -1 /opt/project//rawdata_10ge/NGS_Samp3_R1.fastq.gz -2 /opt/project//rawdata_10ge/NGS_Samp3_R2.fastq.gz -o /opt/project//qc/Samp3 && seqkit stats /opt/project//qc/Samp3/NGS_Samp3_R1_val_1.fq.gz -a > /opt/project//qc/Samp3/Samp3_R1_val_1.stat && seqkit stats /opt/project//qc/Samp3/NGS_Samp3_R2_val_2.fq.gz -a > /opt/project//qc/Samp3/Samp3_R2_val_2.stat && conda deactivate && ln -sfn /opt/project//rawdata_10ge/ONT_Samp3.fastq.gz /opt/project//qc/Samp3/ONT_Samp3.fastq.gz && echo This-Work-is-Completed! && touch /opt/project//shell/run_step1.qc.sh/step1.qc.03.sh.Check
