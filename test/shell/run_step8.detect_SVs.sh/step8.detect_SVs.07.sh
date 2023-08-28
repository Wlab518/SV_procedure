mkdir -p /opt/project//SVs/s__CAG-127_sp900319515/ && cd /opt/project//SVs/s__CAG-127_sp900319515/ && ln -sfn /opt/project//drep_bins/bins/Samp1.bin.14.orig.fa /opt/project//SVs/s__CAG-127_sp900319515/query_Samp1.bin.14.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp10.bin.6.orig.fa /opt/project//SVs/s__CAG-127_sp900319515/query_Samp10.bin.6.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp2.bin.27.orig.fa /opt/project//SVs/s__CAG-127_sp900319515/query_Samp2.bin.27.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp3.bin.44.orig.fa /opt/project//SVs/s__CAG-127_sp900319515/query_Samp3.bin.44.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp4.bin.28.orig.fa /opt/project//SVs/s__CAG-127_sp900319515/query_Samp4.bin.28.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp5.bin.32.orig.fa /opt/project//SVs/s__CAG-127_sp900319515/ref_Samp5.bin.32.orig.fa && for i in `ls query_*.fa`; do bash /data/liyuejuan/miniconda3//envs/mySVenv_python2/MUMandCo/older_versions/mumandco_v2.4.2.sh -r $(ls ref_*.fa) -q $i -g 2769075 -o $i\_run; if [ -f "transloc_list.txt" ]; then mv transloc_list.txt $i\_transloc_list.txt; fi done && echo This-Work-is-Completed! && touch /opt/project//shell/run_step8.detect_SVs.sh/step8.detect_SVs.07.sh.Check
