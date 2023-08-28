cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD7_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp5_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp5_R1.fastq.gz -a > NGS_Samp5_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD7_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp5_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp5_R2.fastq.gz -a > NGS_Samp5_R2.stat && ln -sfn /opt/project/data//TD7.f*q.gz /opt/project//rawdata_10ge/ONT_Samp5.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp5.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp5_distribution.txt && mv raeds_distribution.pdf ONT_Samp5_distribution.pdf && echo This-Work-is-Completed! && touch /opt/project//shell/run_step0.change_name.sh/step0.change_name.05.sh.Check
