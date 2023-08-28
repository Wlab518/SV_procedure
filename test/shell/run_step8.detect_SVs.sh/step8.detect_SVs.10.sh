mkdir -p /opt/project//SVs/s__Mediterraneibacter_lactaris/ && cd /opt/project//SVs/s__Mediterraneibacter_lactaris/ && ln -sfn /opt/project//drep_bins/bins/Samp1.bin.24.orig.fa /opt/project//SVs/s__Mediterraneibacter_lactaris/query_Samp1.bin.24.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp2.bin.53.orig.fa /opt/project//SVs/s__Mediterraneibacter_lactaris/query_Samp2.bin.53.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp3.bin.5.orig.fa /opt/project//SVs/s__Mediterraneibacter_lactaris/ref_Samp3.bin.5.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp4.bin.18.orig.fa /opt/project//SVs/s__Mediterraneibacter_lactaris/query_Samp4.bin.18.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp5.bin.25.orig.fa /opt/project//SVs/s__Mediterraneibacter_lactaris/query_Samp5.bin.25.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp9.bin.33.orig.fa /opt/project//SVs/s__Mediterraneibacter_lactaris/query_Samp9.bin.33.orig.fa && for i in `ls query_*.fa`; do bash /data/liyuejuan/miniconda3//envs/mySVenv_python2/MUMandCo/older_versions/mumandco_v2.4.2.sh -r $(ls ref_*.fa) -q $i -g 2446199 -o $i\_run; if [ -f "transloc_list.txt" ]; then mv transloc_list.txt $i\_transloc_list.txt; fi done && echo This-Work-is-Completed! && touch /opt/project//shell/run_step8.detect_SVs.sh/step8.detect_SVs.10.sh.Check
