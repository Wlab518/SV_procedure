mkdir -p /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/ && cd /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/ && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp10.bin.15.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp10.bin.15.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp2.bin.1.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp2.bin.1.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp3.bin.6.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp3.bin.6.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp4.bin.37.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp4.bin.37.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp6.bin.15.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/ref_Samp6.bin.15.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp7.bin.26.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp7.bin.26.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp8.bin.22.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp8.bin.22.orig.fa && ln -sfn /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//drep_bins/bins/Samp9.bin.41.orig.fa /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//SVs/s__Phocaeicola_vulgatus/query_Samp9.bin.41.orig.fa && for i in `ls query_*.fa`; do bash /data/liyuejuan/miniconda3//envs/mySVenv_python2/MUMandCo/older_versions/mumandco_v2.4.2.sh -r $(ls ref_*.fa) -q $i -g 4656535 -o $i\_run; if [ -f "transloc_list.txt" ]; then mv transloc_list.txt $i\_transloc_list.txt; fi done && echo This-Work-is-Completed! && touch /data/liyuejuan/miniconda3/envs/mySVenv_python3/SV_procedure/test//shell/run_step8.detect_SVs.sh/step8.detect_SVs.13.sh.Check