mkdir -p /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//assembly/Samp5/quast && cd /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//assembly/Samp5/ && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && metaspades.py -1 /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//cleandata/NGS_Samp5_filter_1.fastq.gz -2 /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//cleandata/NGS_Samp5_filter_2.fastq.gz  --nanopore /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//cleandata/ONT_Samp5_filter.fastq.gz -o /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//assembly/Samp5 && quast /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//assembly/Samp5/scaffolds.fasta -o /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//assembly/Samp5/quast --no-plots --no-html && conda deactivate && echo This-Work-is-Completed! && touch /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//shell/run_step3.assembly.sh/step3.assembly.05.sh.Check