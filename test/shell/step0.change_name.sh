cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD1_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp1_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp1_R1.fastq.gz -a > NGS_Samp1_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD1_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp1_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp1_R2.fastq.gz -a > NGS_Samp1_R2.stat && ln -sfn /opt/project/data//TD1.f*q.gz /opt/project//rawdata_10ge/ONT_Samp1.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp1.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp1_distribution.txt && mv raeds_distribution.pdf ONT_Samp1_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD2_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp2_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp2_R1.fastq.gz -a > NGS_Samp2_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD2_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp2_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp2_R2.fastq.gz -a > NGS_Samp2_R2.stat && ln -sfn /opt/project/data//TD2.f*q.gz /opt/project//rawdata_10ge/ONT_Samp2.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp2.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp2_distribution.txt && mv raeds_distribution.pdf ONT_Samp2_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD5_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp3_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp3_R1.fastq.gz -a > NGS_Samp3_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD5_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp3_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp3_R2.fastq.gz -a > NGS_Samp3_R2.stat && ln -sfn /opt/project/data//TD5.f*q.gz /opt/project//rawdata_10ge/ONT_Samp3.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp3.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp3_distribution.txt && mv raeds_distribution.pdf ONT_Samp3_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD6_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp4_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp4_R1.fastq.gz -a > NGS_Samp4_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD6_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp4_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp4_R2.fastq.gz -a > NGS_Samp4_R2.stat && ln -sfn /opt/project/data//TD6.f*q.gz /opt/project//rawdata_10ge/ONT_Samp4.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp4.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp4_distribution.txt && mv raeds_distribution.pdf ONT_Samp4_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD7_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp5_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp5_R1.fastq.gz -a > NGS_Samp5_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD7_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp5_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp5_R2.fastq.gz -a > NGS_Samp5_R2.stat && ln -sfn /opt/project/data//TD7.f*q.gz /opt/project//rawdata_10ge/ONT_Samp5.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp5.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp5_distribution.txt && mv raeds_distribution.pdf ONT_Samp5_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD19_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp6_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp6_R1.fastq.gz -a > NGS_Samp6_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD19_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp6_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp6_R2.fastq.gz -a > NGS_Samp6_R2.stat && ln -sfn /opt/project/data//TD19.f*q.gz /opt/project//rawdata_10ge/ONT_Samp6.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp6.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp6_distribution.txt && mv raeds_distribution.pdf ONT_Samp6_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD29_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp7_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp7_R1.fastq.gz -a > NGS_Samp7_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD29_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp7_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp7_R2.fastq.gz -a > NGS_Samp7_R2.stat && ln -sfn /opt/project/data//TD29.f*q.gz /opt/project//rawdata_10ge/ONT_Samp7.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp7.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp7_distribution.txt && mv raeds_distribution.pdf ONT_Samp7_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD59_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp8_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp8_R1.fastq.gz -a > NGS_Samp8_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD59_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp8_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp8_R2.fastq.gz -a > NGS_Samp8_R2.stat && ln -sfn /opt/project/data//TD59.f*q.gz /opt/project//rawdata_10ge/ONT_Samp8.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp8.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp8_distribution.txt && mv raeds_distribution.pdf ONT_Samp8_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD69_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp9_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp9_R1.fastq.gz -a > NGS_Samp9_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD69_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp9_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp9_R2.fastq.gz -a > NGS_Samp9_R2.stat && ln -sfn /opt/project/data//TD69.f*q.gz /opt/project//rawdata_10ge/ONT_Samp9.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp9.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp9_distribution.txt && mv raeds_distribution.pdf ONT_Samp9_distribution.pdf
cd /opt/project//rawdata_10ge && ln -sfn /opt/project/data//META20IMWJ27_TD79_*1.f*q.gz /opt/project//rawdata_10ge/NGS_Samp10_R1.fastq.gz && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && seqkit stats /opt/project//rawdata_10ge/NGS_Samp10_R1.fastq.gz -a > NGS_Samp10_R1.stat && ln -sfn /opt/project/data//META20IMWJ27_TD79_*2.f*q.gz /opt/project//rawdata_10ge/NGS_Samp10_R2.fastq.gz && seqkit stats /opt/project//rawdata_10ge/NGS_Samp10_R2.fastq.gz -a > NGS_Samp10_R2.stat && ln -sfn /opt/project/data//TD79.f*q.gz /opt/project//rawdata_10ge/ONT_Samp10.fastq.gz && conda deactivate && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//static_reads_length.py /opt/project//rawdata_10ge/ONT_Samp10.fastq.gz /opt/project//rawdata_10ge/reads_distribution.txt && Rscript /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//distribution.R && conda deactivate && mv reads_distribution.txt ONT_Samp10_distribution.txt && mv raeds_distribution.pdf ONT_Samp10_distribution.pdf
