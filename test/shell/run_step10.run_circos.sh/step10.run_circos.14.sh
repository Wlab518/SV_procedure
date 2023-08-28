mkdir -p /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris && cd /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris && cp /opt/project//SVs/s__Mediterraneibacter_lactaris/ref_* /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris && cp /opt/project//SVs/s__Mediterraneibacter_lactaris/*_run_output/*_run.SVs_all.tsv  /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && samtools faidx /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris/ref_* && conda deactivate && ref=`ls ref_*.fa|sed 's/ref_//g'` && cp /opt/project//gene_model/$ref/$ref.gff /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris && awk -F '\t' -v OFS=' ' '{print "chr - "$1,$1,"0 "$2" lgrey"}' /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris/ref_*.fa.fai >  /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris/reference.dat && for t in `ls /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris/*fa_run.SVs_all.tsv`; do out=`echo $t| sed 's/fa_run.SVs_all.tsv/dat/g'`; source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//get_circos_data.py $t ref_*.fa.fai $ref\.gff $out $t\_number.txt; done && ls query_*.dat > tile_input.list && cat ./*_number.txt | sort|uniq | grep -v "Samples" | sed '1i\Samples\tDeletions\tInsertions\tTranslocations\tInversions\tDuplications'> SVs_number_static.txt && rm *_number.txt *fa_run.SVs_all.tsv && cp /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//circos_conf/*.conf ./ && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//get_circos_tile_conf.py tile_input.list /opt/project/sample_info.txt T1 && conda deactivate && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python2 && circos -conf circos.conf && conda deactivate && ls /opt/project//result_stat/circos/s__Mediterraneibacter_lactaris/query_*.dat > sv_file.list && source /data/liyuejuan/miniconda3//etc/profile.d/conda.sh && conda activate mySVenv_python3 && python /data/liyuejuan/miniconda3//envs/mySVenv_python3/SV_procedure/bin//get_SVs_on_gene.py sv_file.list gene.dat SVs_on_gene.txt && conda deactivate && echo This-Work-is-Completed! && touch /opt/project//shell/run_step10.run_circos.sh/step10.run_circos.14.sh.Check
