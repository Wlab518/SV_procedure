mkdir -p /opt/project//SVs/s__Gemmiger_formicilis/ && cd /opt/project//SVs/s__Gemmiger_formicilis/ && ln -sfn /opt/project//drep_bins/bins/Samp1.bin.23.orig.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp1.bin.23.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp10.bin.47.orig.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp10.bin.47.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp2.bin.39.strict.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp2.bin.39.strict.fa && ln -sfn /opt/project//drep_bins/bins/Samp3.bin.15.strict.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp3.bin.15.strict.fa && ln -sfn /opt/project//drep_bins/bins/Samp4.bin.27.orig.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp4.bin.27.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp5.bin.18.orig.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp5.bin.18.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp8.bin.32.orig.fa /opt/project//SVs/s__Gemmiger_formicilis/ref_Samp8.bin.32.orig.fa && ln -sfn /opt/project//drep_bins/bins/Samp9.bin.27.orig.fa /opt/project//SVs/s__Gemmiger_formicilis/query_Samp9.bin.27.orig.fa && for i in `ls query_*.fa`; do bash /data/liyuejuan/miniconda3//envs/mySVenv_python2/MUMandCo/older_versions/mumandco_v2.4.2.sh -r $(ls ref_*.fa) -q $i -g 2958337 -o $i\_run; if [ -f "transloc_list.txt" ]; then mv transloc_list.txt $i\_transloc_list.txt; fi done && echo This-Work-is-Completed! && touch /opt/project//shell/run_step8.detect_SVs.sh/step8.detect_SVs.06.sh.Check
