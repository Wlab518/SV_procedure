# -*- coding: UTF-8 -*-
import argparse
import configparser
import subprocess
import os
import gzip
import sys
import time
import glob
import math
import operator
import multiprocessing
#from urllib.request import urlopen
#from pdfminer.pdfparser import PDFParser, PDFDocument
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.pdfdevice import PDFDevice
#from pdfminer.converter import PDFPageAggregator
#from pdfminer.layout import LTTextBoxHorizontal, LAParams

#print('Number of CPUs in the system: {}'.format(os.cpu_count()))
#cwdpath = os.getcwd()


def main(ifile):
    
    ###############################check and read config.ini###################################
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    con = configparser.ConfigParser()
    con.read(os.path.join(BASE_DIR, ifile), encoding = "utf-8")

    ##normal software path
    script_path = '/opt/conda/SV_procedure/bin/'
    mumandco = '/opt/conda/envs/mySVenv_python2/MUMandCo/older_versions/mumandco_v2.4.2.sh'
    conda = '/opt/conda/SV_procedure/SV_env.txt'
    opera_ms = '/opt/conda/envs/mySVenv_python3/OPERA-MS/OPERA-MS.pl'
    annotate = '/opt/conda/envs/mySVenv_python2/lib/python2.7/site-packages/kobas/scripts/annotate.py'

    ##database path
    checkmdb = con.items("database")[0][1]
    gtdbtk = con.items("database")[1][1]
    seq_pep = con.items("database")[2][1]
    sqlite3 = con.items("database")[3][1]
    #ko_db = '/opt/conda/envs/mySVenv_python2/db/ko'
    #ko_pep = miniconda + '/envs/mySVenv_python2/db/kegg/seq_pep/ko.pep.fasta'


    datapath = con.items("fastq")[0][1]
    infotable = con.items("fastq")[1][1]
    genome = con.items("filter_host")[0][1]
    bowtie2_threads = con.items("filter_host")[1][1]

    method = con.items("assembly")[0][1]
    kmer= con.items("assembly")[1][1]
    assembly_threads = con.items("assembly")[2][1]
    binning = con.items("binning")
    binning_dict = dict(binning)
    dereplicated_bin = con.items("dereplicated_bin")
    derepl_dict = dict(dereplicated_bin)
    circos_group = con.items("circos")[0][1]
    sv_loc = con.items("sv")[0][1]
    par = con.items("par")
    par_dict = dict(par)
    path = par_dict["outdir"]
    threads = par_dict["multiprocessing"]

    subprocess.call('mkdir -p {}/shell'.format(path), shell=True, executable='/bin/bash')
    #change the database paths
    subprocess.call('sed -i \'s/""/"{}"/g\' /opt/conda/envs/mySVenv_python2/lib/python2.7/site-packages/checkm/DATA_CONFIG'.format(checkmdb.replace("/", "\/")), shell=True, executable='/bin/bash')
    subprocess.call('sed -i \'s/""/"{}"/g\' /opt/conda/lib/python3.1/site-packages/checkm/DATA_CONFIG'.format(checkmdb.replace("/", "\/")), shell=True, executable='/bin/bash') 
    subprocess.call('sed -i \'s/=$/={}/g\' /opt/conda/etc/conda/activate.d/gtdbtk.sh'.format(gtdbtk.replace("/", "\/")), shell=True, executable='/bin/bash')
  #########################copy rawdata from rawdatapath and change names##################
    with open('{}'.format(infotable)) as f:
        file_list = [line.strip().split('\t') for line in f.readlines()]
    
    data_dict = {}
    for i in file_list[1:]:
        data_dict.setdefault(i[0], []).extend(i[1:])
    sample_num = len(data_dict.keys())
    group_name = []
    for val in data_dict.values():
        group_name.append(val[-1])
    group_num = len(list(set(group_name)))
    with open('{}/shell/step0.change_name.sh'.format(path), 'w') as r0:  
        for ids, names in data_dict.items():
            r0.write('mkdir -p {0}/rawdata_{1}ge/{2} && '.format(path, sample_num, ids))
            r0.write('cd {0}/rawdata_{1}ge/{2} && '.format(path, sample_num, ids))
            r0.write('ln -sfn {0}/{1}_*1.f*q.gz {2}/rawdata_{3}ge/{4}/NGS_{4}_R1.fastq.gz && '.format(datapath, names[0], path, sample_num, ids))
            r0.write('source {0} && conda activate mySVenv_python2 && seqkit stats {1}/rawdata_{2}ge/{3}/NGS_{3}_R1.fastq.gz -a > NGS_{3}_R1.stat && '.format(conda, path, sample_num, ids))
            r0.write('ln -sfn {0}/{1}_*2.f*q.gz {2}/rawdata_{3}ge/{4}/NGS_{4}_R2.fastq.gz && '.format(datapath, names[0], path, sample_num, ids))
            r0.write('seqkit stats {0}/rawdata_{1}ge/{2}/NGS_{2}_R2.fastq.gz -a > NGS_{2}_R2.stat && '.format(path, sample_num, ids))
            r0.write('ln -sfn {0}/{1}.f*q.gz {2}/rawdata_{3}ge/{4}/ONT_{4}.fastq.gz && conda deactivate && '.format(datapath, names[1], path, sample_num, ids))
            r0.write('source {4} && conda activate mySVenv_python3 && python {0}/static_reads_length.py {1}/rawdata_{2}ge/{3}/ONT_{3}.fastq.gz {1}/rawdata_{2}ge/{3}/reads_distribution.txt && '.format(script_path, path, sample_num, ids, conda))
            r0.write('R --slave --no-restore --file={0}/distribution.R && conda deactivate && '.format(script_path)) 
            r0.write('mv reads_distribution.txt ONT_{0}_distribution.txt && mv raeds_distribution.pdf ONT_{0}_distribution.pdf\n'.format(ids))
    run_script('{}/shell/step0.change_name.sh'.format(path), int(threads))
    os.chdir(path)
    
    ###########################quality control for NGS data by metawrap#####################
    with open('{}/shell/step1.qc.sh'.format(path), 'w') as r:     
        for samp, dat in data_dict.items():
            r.write('mkdir -p {0}/qc/{1} && cd {0}/qc/{1} && '.format(path, samp))
            r.write('source {3} && conda activate mySVenv_python2 && cp {0}/rawdata_{1}ge/{2}/NGS_{2}_R1.fastq.gz {0}/qc/{2}/NGS_{2}_1.fastq.gz && cp {0}/rawdata_{1}ge/{2}/NGS_{2}_R2.fastq.gz {0}/qc/{2}/NGS_{2}_2.fastq.gz && gunzip {0}/qc/{2}/NGS_{2}_*.fastq.gz && metaWRAP read_qc -1 {0}/qc/{2}/NGS_{2}_1.fastq -2 {0}/qc/{2}/NGS_{2}_2.fastq -o {0}/qc/{2} --skip-bmtagger && rm {0}/qc/{2}/NGS_{2}_* && mv {0}/qc/{2}/final_pure_reads_1.fastq {0}/qc/{2}/NGS_{2}_R1_val_1.fq && gzip {0}/qc/{2}/NGS_{2}_R1_val_1.fq && mv {0}/qc/{2}/final_pure_reads_2.fastq {0}/qc/{2}/NGS_{2}_R2_val_2.fq && gzip {0}/qc/{2}/NGS_{2}_R2_val_2.fq && '.format(path, sample_num, samp, conda))
            r.write('seqkit stats {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz -a > {0}/qc/{1}/{1}_R1_val_1.stat && '.format(path, samp))
            r.write('seqkit stats {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz -a > {0}/qc/{1}/{1}_R2_val_2.stat && conda deactivate && '.format(path, samp))
            r.write('ln -sfn {0}/rawdata_{1}ge/{2}/ONT_{2}.fastq.gz {0}/qc/{2}/ONT_{2}.fastq.gz\n'.format(path, sample_num, samp))   
    run_script('{}/shell/step1.qc.sh'.format(path), int(threads))
    os.chdir(path)

    if genome == "none":
        pass
    else:
        #########################filter host genome for all data by minimap2#####################
        if os.path.exists('{}.1.bt2'.format(genome)): 
            pass
        else:
            subprocess.call('source {2} && conda activate mySVenv_python2 && bowtie2-build --threads {1} {0} {0} && conda deactivate'.format(genome, bowtie2_threads, conda), shell=True, executable='/bin/bash')
        if os.path.exists('{}.min'.format(genome)):
            pass
        else:
            subprocess.call('source {1} && conda activate mySVenv_python2 && minimap2 -d {0}.min {0} && conda deactivate'.format(genome, conda), shell=True, executable='/bin/bash')
        with open('{}/shell/step2.filter_host.sh'.format(path), 'w') as r1: 
            for samp in data_dict.keys():
                r1.write('mkdir -p {0}/cleandata/{2} && cd {0}/cleandata/{2} && source {1} && conda activate mySVenv_python2 && '.format(path, conda, samp))
                r1.write('minimap2 -a {0}.min {1}/qc/{2}/ONT_{2}.fastq.gz > {1}/cleandata/{2}/ONT_{2}.sam && conda deactivate && '.format(genome, path, samp))
                r1.write('cat {0}/cleandata/{1}/ONT_{1}.sam | awk \'{{if($4==0){{print $0;}}}}\'|awk \'{{print "@"$1"\\n"$10"\\n+\\n"$11;}}\' | gzip > {0}/cleandata/{1}/ONT_{1}_filter.fastq.gz && '.format(path, samp))
                r1.write('source {0} && conda activate mySVenv_python3 && python {1}/static_reads_length.py  {2}/cleandata/{3}/ONT_{3}_filter.fastq.gz {2}/cleandata/{3}/reads_distribution.txt && '.format(conda, script_path, path, samp))
                r1.write('R --slave --no-restore --file={0}/distribution.R && conda deactivate && '.format(script_path))
                r1.write('mv reads_distribution.txt ONT_{0}_distribution.txt && mv raeds_distribution.pdf ONT_{0}_distribution.pdf && '.format(samp))
                r1.write('source {4} && conda activate mySVenv_python2 && bowtie2 -x {2} -1 {3}/qc/{1}/NGS_{1}_R1_val_1.fq.gz -2 {3}/qc/{1}/NGS_{1}_R2_val_2.fq.gz -S {3}/cleandata/{1}/NGS_{1}.sam --threads {0} '.format(bowtie2_threads, samp, genome, path, conda))
                r1.write('&& awk \'{{if($4==0){{print $1;}}}}\' {0}/cleandata/{1}/NGS_{1}.sam | uniq> {0}/cleandata/{1}/{1}_id.txt '.format(path, samp))
                r1.write('&& seqkit grep -f {0}/cleandata/{1}/{1}_id.txt {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz |gzip > {0}/cleandata/{1}/NGS_{1}_filter_1.fastq.gz '.format(path, samp))
                r1.write('&& seqkit grep -f {0}/cleandata/{1}/{1}_id.txt {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz |gzip > {0}/cleandata/{1}/NGS_{1}_filter_2.fastq.gz '.format(path, samp))
                r1.write('&& seqkit stats {0}/cleandata/{1}/NGS_{1}_filter_1.fastq.gz -a > {0}/cleandata/{1}/NGS_{1}_filter_1.stat '.format(path, samp))
                r1.write('&& seqkit stats {0}/cleandata/{1}/NGS_{1}_filter_2.fastq.gz -a > {0}/cleandata/{1}/NGS_{1}_filter_2.stat && conda deactivate '.format(path, samp))
                r1.write('&& rm {0}/cleandata/{1}/ONT_{1}.sam {0}/cleandata/{1}/NGS_{1}.sam {0}/cleandata/{1}/{1}_id.txt\n'.format(path, samp))
        run_script('{}/shell/step2.filter_host.sh'.format(path), int(threads))
        os.chdir(path)

    ################################assembly by metaspades############################
    with open('{}/shell/step3.assembly.sh'.format(path), 'w') as r2:
        for samp in data_dict.keys():
            r2.write('mkdir -p {0}/assembly/{1}/quast && cd {0}/assembly/{1}/ '.format(path, samp))
            if genome == "none":
                if method == "Flye":
                    r2.write('&& source {3} && conda activate mySVenv_python2 && flye --nano-raw {0}/qc/{1}/ONT_{1}.fastq.gz --meta  --out-dir {0}/assembly/{1}/ --threads {2} && quast {0}/assembly/{1}/assembly.fasta -o {0}/assembly/{1}/quast --no-plots --no-html && conda deactivate && mv {0}/assembly/{1}/assembly.fasta {0}/assembly/{1}/scaffolds.fasta\n'.format(path, samp, assembly_threads, conda))
                elif method == "OPERA-MS":
                    if kmer == "default":
                        r2.write('&& source {2} && conda activate mySVenv_python3 && ln -sfn {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz {0}/assembly/{1}/NGS_{1}_R1.fastq.gz && ln -sfn {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz {0}/assembly/{1}/NGS_{1}_R2.fastq.gz && gzip -cd {0}/qc/{1}/ONT_{1}.fastq.gz > {0}/assembly/{1}/ONT_{1}.fastq && perl {3} --short-read1 {0}/assembly/{1}/NGS_{1}_R1.fastq.gz --short-read2 {0}/assembly/{1}/NGS_{1}_R2.fastq.gz --long-read {0}/assembly/{1}/ONT_{1}.fastq --out-dir {0}/assembly/{1}/ --no-ref-clustering --no-strain-clustering --num-processors {4} && conda deactivate && mv {0}/assembly/{1}/contigs.fasta {0}/assembly/{1}/scaffolds.fasta\n'.format(path, samp, conda, opera_ms, assembly_threads))
                    else:
                        r2.write('&& source {2} && conda activate mySVenv_python3 && ln -sfn {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz {0}/assembly/{1}/NGS_{1}_R1.fastq.gz && ln -sfn {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz {0}/assembly/{1}/NGS_{1}_R2.fastq.gz && gzip -cd {0}/qc/{1}/ONT_{1}.fastq.gz > {0}/assembly/{1}/ONT_{1}.fastq && perl {3} --short-read1 {0}/assembly/{1}/NGS_{1}_R1.fastq.gz --short-read2 {0}/assembly/{1}/NGS_{1}_R2.fastq.gz --long-read {0}/assembly/{1}/ONT_{1}.fastq --out-dir {0}/assembly/{1}/ --kmer-size {4} --no-ref-clustering --no-strain-clustering --num-processors {5} && conda deactivate && mv {0}/assembly/{1}/contigs.fasta {0}/assembly/{1}/scaffolds.fasta\n'.format(path, samp, conda, opera_ms, str(kmer), assembly_threads))
                else:
                    if kmer == "default":
                        r2.write('&& source {2} && conda activate mySVenv_python2 && metaspades.py -1 {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz -2  {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz --nanopore {0}/qc/{1}/ONT_{1}.fastq.gz -o {0}/assembly/{1} && quast {0}/assembly/{1}/scaffolds.fasta -o {0}/assembly/{1}/quast --no-plots --no-html && conda deactivate\n'.format(path, samp, conda)) 
                    else:
                        r2.write('&& source {3} && conda activate mySVenv_python2 && metaspades.py -1 {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz -2  {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz --nanopore {0}/qc/{1}/ONT_{1}.fastq.gz -o {0}/assembly/{1} -k {2} && quast {0}/assembly/{1}/scaffolds.fasta -o {0}/assembly/{1}/quast --no-plots --no-html && conda deactivate\n'.format(path, samp, str(kmer), conda)) 
            else:
                if method == "Flye":
                    r2.write('&& source {3} && conda activate mySVenv_python2 && flye --nano-raw {0}/cleandata/{1}/ONT_{1}_filter.fastq.gz --meta  --out-dir {0}/assembly/{1}/ --threads {2} && quast {0}/assembly/{1}/assembly.fasta -o {0}/assembly/{1}/quast --no-plots --no-html && conda deactivate && mv {0}/assembly/{1}/assembly.fasta {0}/assembly/{1}/scaffolds.fasta\n'.format(path, samp, assembly_threads, conda))
                elif method == "OPERA-MS":
                    if kmer == "default":
                        r2.write('&& source {2} && conda activate mySVenv_python3 && ln -sfn {0}/cleandata/{1}/NGS_{1}_filter_1.fastq.gz {0}/assembly/{1}/NGS_{1}_R1.fastq.gz && ln -sfn {0}/cleandata/{1}/NGS_{1}_filter_2.fastq.gz {0}/assembly/{1}/NGS_{1}_R2.fastq.gz && gzip -cd {0}/cleandata/{1}/ONT_{1}_filter.fastq.gz > {0}/assembly/{1}/ONT_{1}_filter.fastq && perl {3} --short-read1 {0}/assembly/{1}/NGS_{1}_R1.fastq.gz --short-read2 {0}/assembly/{1}/NGS_{1}_R2.fastq.gz --long-read {0}/assembly/{1}/ONT_{1}_filter.fastq --out-dir {0}/assembly/{1}/ --no-ref-clustering --no-strain-clustering --num-processors {4} && conda deactivate && mv {0}/assembly/{1}/contigs.fasta {0}/assembly/{1}/scaffolds.fasta\n'.format(path, samp, conda, opera_ms, assembly_threads))
                    else:
                        r2.write('&& source {2} && conda activate mySVenv_python3 && ln -sfn {0}/cleandata/{1}/NGS_{1}_filter_1.fastq.gz {0}/assembly/{1}/NGS_{1}_R1.fastq.gz && ln -sfn {0}/cleandata/{1}/NGS_{1}_filter_2.fastq.gz {0}/assembly/{1}/NGS_{1}_R2.fastq.gz && gzip -cd {0}/cleandata/{1}/ONT_{1}_filter.fastq.gz > {0}/assembly/{1}/ONT_{1}_filter.fastq && perl {3} --short-read1 {0}/assembly/{1}/NGS_{1}_R1.fastq.gz --short-read2 {0}/assembly/{1}/NGS_{1}_R2.fastq.gz --long-read {0}/assembly/{1}/ONT_{1}_filter.fastq --out-dir {0}/assembly/{1}/ --kmer-size {4} --no-ref-clustering --no-strain-clustering --num-processors {5} && conda deactivate && mv {0}/assembly/{1}/contigs.fasta {0}/assembly/{1}/scaffolds.fasta\n'.format(path, samp, conda, opera_ms, str(kmer), assembly_threads))
                else:
                    if kmer == "default":
                        r2.write('&& source {2} && conda activate mySVenv_python2 && metaspades.py -1 {0}/cleandata/{1}/NGS_{1}_filter_1.fastq.gz -2 {0}/cleandata/{1}/NGS_{1}_filter_2.fastq.gz  --nanopore {0}/cleandata/{1}/ONT_{1}_filter.fastq.gz -o {0}/assembly/{1} && quast {0}/assembly/{1}/scaffolds.fasta -o {0}/assembly/{1}/quast --no-plots --no-html && conda deactivate\n'.format(path, samp, conda)) 
                    else:
                        r2.write('&& source {3} && conda activate mySVenv_python2 && metaspades.py -1 {0}/cleandata/{1}/NGS_{1}_filter_1.fastq.gz -2 {0}/cleandata/{1}/NGS_{1}_filter_2.fastq.gz  --nanopore {0}/cleandata/{1}/ONT_{1}_filter.fastq.gz -o {0}/assembly/{1} -k {2} && quast {0}/assembly/{1}/scaffolds.fasta -o {0}/assembly/{1}/quast --no-plots --no-html && conda deactivate\n'.format(path, samp, str(kmer), conda)) 

    run_script('{}/shell/step3.assembly.sh'.format(path), int(threads))
    os.chdir(path)

    ##############################binning by metawrap###################################
    with open('{}/shell/step4.binning.sh'.format(path), 'w') as r3:
        for samp in data_dict.keys():
            if genome == "none":
                r3.write('mkdir -p {0}/binning/{1} && cd {0}/binning/{1} && cp {0}/qc/{1}/NGS_{1}_R1_val_1.fq.gz {0}/binning/{1}/NGS_{1}_1.fastq.gz && cp {0}/qc/{1}/NGS_{1}_R2_val_2.fq.gz {0}/binning/{1}/NGS_{1}_2.fastq.gz && gzip -d {0}/binning/{1}/NGS_{1}_*.fastq.gz && source {2} && conda activate mySVenv_python2 '.format(path, samp, conda))
                r3.write('&& metawrap binning -o initial_binning -t {2} --metabat2 --maxbin2 --concoct -a {0}/assembly/{1}/scaffolds.fasta {0}/binning/{1}/NGS_{1}_1.fastq {0}/binning/{1}/NGS_{1}_2.fastq '.format(path, samp, binning_dict["threads_bin"]))
                r3.write('&& metawrap bin_refinement -o bin_refinement -t {2} -A initial_binning/metabat2_bins/ -B initial_binning/maxbin2_bins/ -C initial_binning/concoct_bins/ -c {0} -x {1} '.format(binning_dict["mini_completion"], binning_dict["max_contamination"], binning_dict["threads_bin"]))
                r3.write('&& metawrap reassemble_bins -o reassemble_bins -1 {0}/binning/{1}/NGS_{1}_1.fastq -2 {0}/binning/{1}/NGS_{1}_2.fastq -t {4} -c {2} -x {3} -b bin_refinement/metawrap_{2}_{3}_bins && conda deactivate\n'.format(path, samp,  binning_dict["mini_completion"], binning_dict["max_contamination"], binning_dict["threads_bin"]))
            else:
                r3.write('mkdir -p {0}/binning/{1} && cd {0}/binning/{1} && cp {0}/cleandata/{1}/NGS_{1}_filter_*.fastq.gz {0}/binning/{1} && gzip -d {0}/binning/{1}/NGS_{1}_filter_*.fastq.gz && source {2} && conda activate mySVenv_python2 '.format(path, samp, conda))
                r3.write('&& metawrap binning -o initial_binning -t {2} --metabat2 --maxbin2 --concoct -a {0}/assembly/{1}/scaffolds.fasta {0}/binning/{1}/NGS_{1}_filter_1.fastq {0}/binning/{1}/NGS_{1}_filter_2.fastq '.format(path, samp, binning_dict["threads_bin"]))
                r3.write('&& metawrap bin_refinement -o bin_refinement -t {2} -A initial_binning/metabat2_bins/ -B initial_binning/maxbin2_bins/ -C initial_binning/concoct_bins/ -c {0} -x {1} '.format(binning_dict["mini_completion"], binning_dict["max_contamination"], binning_dict["threads_bin"]))
                r3.write('&& metawrap reassemble_bins -o reassemble_bins -1 {0}/binning/{1}/NGS_{1}_filter_1.fastq -2 {0}/binning/{1}/NGS_{1}_filter_2.fastq -t {4} -c {2} -x {3} -b bin_refinement/metawrap_{2}_{3}_bins && conda deactivate\n'.format(path, samp,  binning_dict["mini_completion"], binning_dict["max_contamination"], binning_dict["threads_bin"]))
    run_script('{}/shell/step4.binning.sh'.format(path), 2)
    os.chdir(path)

    ############################the de-replication of bins by dRep#########################
    with open('{}/shell/step5.drep_bins.sh'.format(path), 'w') as r4:
        r4.write('mkdir -p {0}/drep_bins/bins && cd {0}/drep_bins && '.format(path))
        for samp in data_dict.keys():
            bin_path = '{0}/binning/{1}/reassemble_bins/reassembled_bins'.format(path, samp)
            if len(os.listdir(bin_path)) == 0:
                #r4.write('## None of the bins were successfully reassembled. "reassemble_bins/reassembled_bins/" is empty.\n')
                r4.write('for i in `ls {0}/binning/{1}/bin_refinement/metawrap_{3}_{4}_bins/*.fa`; '.format(path, samp, binning_dict["mini_completion"], binning_dict["max_contamination"]))
                r4.write('do ')
                r4.write('file=`basename $i`; ')
                r4.write('ln -sfn $i {0}/drep_bins/bins/{1}_$file; '.format(path, samp))
                r4.write('done && ')
            else:
                r4.write('for i in `ls {}/*.fa`; '.format(bin_path))
                r4.write('do ')
                r4.write('file=`basename $i`; ')
                r4.write('ln -sfn $i {0}/drep_bins/bins/{1}.$file; '.format(path, samp))
                r4.write('done && ')
        r4.write('source {5} && conda activate base && dRep dereplicate {0}/drep_bins -g {0}/drep_bins/bins/*.fa -pa {1} -sa {2} -nc {3} -cm {4} && conda deactivate && conda activate mySVenv_python3 && '.format(path, derepl_dict["primary_ani"], derepl_dict["secondary_ani"], derepl_dict["min_overlap"], derepl_dict["coverage_method"], conda))
        r4.write('python {0}/Bins_info_for_each_MAGs.py {1}/drep_bins/figures/Cluster_scoring.pdf {1}/drep_bins/data_tables/genomeInfo.csv && conda deactivate\n'.format(script_path, path))
    run_script('{}/shell/step5.drep_bins.sh'.format(path), 1)
    #mags_bins("{0}/drep_bins/figures/Cluster_scoring.pdf".format(path), "{0}/drep_bins/data_tables/genomeInfo.csv".format(path))
    os.chdir(path)

    #########################The taxonomy of dereplicated bins by gtdbtk#####################
    with open('{}/shell/step6.taxonomy_bins.sh'.format(path), 'w') as r5:
        r5.write('mkdir -p {0}/taxonomy && cd {0}/taxonomy && '.format(path))
        r5.write('source {1} && conda activate base && gtdbtk classify_wf --genome_dir {0}/drep_bins/dereplicated_genomes/ --out_dir {0}/taxonomy --extension fa --prefix classify && conda deactivate\n'.format(path, conda))
    run_script('{}/shell/step6.taxonomy_bins.sh'.format(path), 1)
    os.chdir(path)
    
    #########################The gene model of dereplicated bins by prokka#####################
    with open('{}/shell/step7.gene_model.sh'.format(path), 'w') as r7:
        r7.write('mkdir -p {0}/gene_model && cd {0}/gene_model && source {1} && conda activate mySVenv_python2 && '.format(path, conda))
        r7.write('for i in `ls {}/drep_bins/dereplicated_genomes/*.fa`; '.format(path))
        r7.write('do ')
        r7.write('file=`basename $i`; ')
        r7.write('prokka $i --outdir $file --prefix $file --centre X --locustag L --force; ')
        r7.write('done ')
        r7.write('&& conda deactivate\n')
    run_script('{}/shell/step7.gene_model.sh'.format(path), 1)
    os.chdir(path)

    ######################################detect SVs by MUMandCo##################################
    final_mags = mags_cluster_info("{0}/taxonomy/classify.bac120.summary.tsv".format(path), "{0}/drep_bins/data_tables/genomeInformation.csv".format(path), "{0}/drep_bins/MAGs".format(path), sample_num, group_name, data_dict)
    species_list = []
    for val in final_mags.values():
        species_list.append(val[-2])
    with open('{}/shell/step8.detect_SVs.sh'.format(path), 'w') as r6:
        for spe in list(set(species_list)):
            r6.write('mkdir -p {0}/SVs/{1}/ && cd {0}/SVs/{1}/ '.format(path, spe.replace(" ", "_")))
            for mags, fa_list in final_mags.items():
                if spe == fa_list[-2] and fa_list[-1] == "reference genome":
                    genomesize = get_genome_size('{0}/drep_bins/bins/{1}.fa'.format(path, mags))
                    r6.write('&& ln -sfn {0}/drep_bins/bins/{1}.fa {0}/SVs/{2}/ref_{1}.fa '.format(path, mags, spe.replace(" ", "_")))
                elif spe == fa_list[-2] and fa_list[-1] == "query genome":
                    r6.write('&& ln -sfn {0}/drep_bins/bins/{1}.fa {0}/SVs/{2}/query_{1}.fa '.format(path, mags, spe.replace(" ", "_")))
                else:
                    pass
            r6.write('&& for i in `ls query_*.fa`; ')
            r6.write('do ')
            r6.write('bash {0} -r $(ls ref_*.fa) -q $i -g {1} -o $i\_run; if [ -f "transloc_list.txt" ]; then mv transloc_list.txt $i\_transloc_list.txt; fi '.format(mumandco, genomesize))
            #r6.write('bash {0} -r $(readlink -f {1}/SVs/{2}/ref_*.fa) -q $i -g {3} -o $i\_run; '.format(mumandco, path, spe.replace(" ", "_"), genomesize))
            r6.write('done\n')
    run_script('{}/shell/step8.detect_SVs.sh'.format(path), int(threads))
    subprocess.call('cd {0}/SVs && ls -d s__* > bacterial_strain.list'.format(path), shell=True, executable='/bin/bash')
    os.chdir(path)

    ######################################SVs visualization#####################################
    if group_num == 2:
        #####################################1.barplot and 2.wilcox_test########################################
        try:
            f =open('{0}/SVs/bacterial_strain.list'.format(path), "r")
            strain_list = [line.strip() for line in f.readlines()]
            f.close()
        except IOError:
            print('{0}/SVs/bacterial_strain.list File is not accessible.'.format(path))
        
        with open('{}/shell/step9.barplot_wilcox.sh'.format(path), 'w') as r8:
            r8.write('source {0} && conda activate mySVenv_python3 && python {1}/get_barplot_wilcox_script.py {2} {3}/SVs/bacterial_strain.list && '.format(conda, script_path, infotable, path))
            for strain in strain_list:
                r8.write('R --slave --no-restore --file={0}/result_stat/barplot/{1}/run_barplot.r && '.format(path, strain))
                r8.write('R --slave --no-restore --file={0}/result_stat/wilcox_test/{1}/run_test.r &&'.format(path, strain))
            r8.write('conda deactivate\n')
        run_script('{}/shell/step9.barplot_wilcox.sh'.format(path), 1)
        os.chdir(path)

        #####################################3.circos########################################
        with open('{}/shell/step10.run_circos.sh'.format(path), 'w') as r9:
            for strain in strain_list:
                r9.write('mkdir -p {0}/result_stat/circos/{1} && cd {0}/result_stat/circos/{1} && '.format(path, strain))
                r9.write('cp {0}/SVs/{1}/ref_*.fa {0}/result_stat/circos/{1} && '.format(path, strain))
                r9.write('cp {0}/SVs/{1}/*_run_output/*_run.SVs_all.tsv  {0}/result_stat/circos/{1} && '.format(path, strain))
                r9.write('source {0} && conda activate mySVenv_python2 && samtools faidx {1}/result_stat/circos/{2}/ref_*.fa && conda deactivate && '.format(conda, path, strain))
                r9.write('ref=`ls ref_*.fa|sed \'s/ref_//g\'` && ')
                r9.write('cp {0}/gene_model/$ref/$ref.gff {0}/result_stat/circos/{1} && '.format(path, strain))
                r9.write('awk -F \'\\t\' -v OFS=\' \' \'{{print "chr - "$1,$1,"0 "$2" lgrey"}}\' {0}/result_stat/circos/{1}/ref_*.fa.fai >  {0}/result_stat/circos/{1}/reference.dat && '.format(path, strain))
                r9.write('for t in `ls {0}/result_stat/circos/{1}/*fa_run.SVs_all.tsv`; '.format(path, strain))
                r9.write('do ')
                r9.write('out=`echo $t| sed \'s/fa_run.SVs_all.tsv/dat/g\'`; ')
                r9.write('source {0} && conda activate mySVenv_python3 && python {1}/get_circos_data.py $t ref_*.fa.fai $ref\.gff $out $t\_number.txt {2}; '.format(conda, script_path, sv_loc))
                r9.write('done && ')
                r9.write('ls query_*.dat > tile_input.list && ')
                r9.write('cat ./*_number.txt | sort|uniq | grep -v "Samples" | sed \'1i\Samples\\tDeletions\\tInsertions\\tTranslocations\\tInversions\\tDuplications\'> SVs_number_static.txt && ')
                r9.write('rm *_number.txt *fa_run.SVs_all.tsv && ')
                r9.write('cp {0}/circos_conf/*.conf ./ && '.format(script_path))
                r9.write('python {0}/get_circos_tile_conf.py tile_input.list {1} {2} && conda deactivate && '.format(script_path, infotable, circos_group))
                r9.write('source {0} && conda activate mySVenv_python2 && circos -conf circos.conf && conda deactivate && '.format(conda))
                r9.write('ls {0}/result_stat/circos/{1}/query_*.dat > sv_file.list && '.format(path, strain))
                r9.write('source {0} && conda activate mySVenv_python3 && python {1}/get_SVs_on_gene.py sv_file.list gene.dat SVs_on_gene.txt && conda deactivate\n'.format(conda, script_path))
        run_script('{}/shell/step10.run_circos.sh'.format(path), int(threads))
        os.chdir(path)

    ######################################KEGG enrichment analysis by kobas###############################
    # 1. build index of KO database
    
    with open('{}/shell/step11.blast_ko_database.sh'.format(path), 'w') as r10:
        for strain in strain_list:
            # 2. diamond blast
            r10.write('mkdir -p {0}/KEGG_enrichment/{1} && cd {0}/KEGG_enrichment/{1} && '.format(path, strain))
            r10.write('ln -sfn {0}/SVs/{1}/ref_* ./ && '.format(path, strain))
            r10.write('ref=`ls ref_*.fa|sed \'s/ref_//g\'` && ')
            r10.write('ln -sfn {0}/gene_model/$ref/$ref.faa ./ && '.format(path))
            r10.write('source {0} && conda activate mySVenv_python2 && diamond makedb --in {1}/ko.pep.fasta --db {1}/ko -p 24 && diamond blastp -e 1e-5 --db {1}/ko -q $ref.faa -p 24 -f 6 qseqid qlen qstart qend qcovhsp slen sstart send score evalue positive length ppos sseqid stitle nident mismatch gaps gapopen bitscore pident -o kobas.annotation && conda deactivate\n'.format(conda, seq_pep))
    run_script('{}/shell/step11.blast_ko_database.sh'.format(path), int(threads))
    os.chdir(path)
    
    with open('{}/shell/step12.KEGG_enrichment.sh'.format(path), 'w') as r11:
        r11.write(' cd {0}/KEGG_enrichment/ && cat ./*/kobas.annotation | sort |uniq > kobas.annotation && '.format(path))
        #3. get Tabular BLAST output format
        r11.write('awk -F "\\t" \'{print $1"\\t"$14"\\t"$21"\\t"$12"\\t"$17"\\t"$19"\\t"$3"\\t"$4"\\t"$7"\\t"$8"\\t"$10"\\t"$20}\' kobas.annotation > kobas.annotation.m8 && ')       
        #4. annotate
        r11.write('source {3} && conda activate mySVenv_python2 && python {0} -i kobas.annotation.m8 -t blastout:tab -s ko -o kegg.annotate.tmp -y {1} -q {2} && '.format(annotate, seq_pep, sqlite3, conda))
        r11.write('python {0}/get_annotation.py kegg.annotate.tmp kegg.annotate.ko.rlt && conda deactivate && '.format(script_path))
        #5. KEGG enrichment
        r11.write('cat {0}/result_stat/circos/*/SV-affected_genes.list|sort|uniq > {0}/KEGG_enrichment/foreground_genes.txt && '.format(path))
        r11.write('sed -i \'1i query_name\' {0}/KEGG_enrichment/foreground_genes.txt && '.format(path))
        r11.write('if [ ! -s "{0}/KEGG_enrichment/foreground_genes.txt" ]; then echo "None of SVs occurs in genes, please see \"{0}/result_stat/circos/*/SVs_on_gene.txt\" files."; else '.format(path))
        r11.write('conda activate mySVenv_python3 && R --slave --no-restore --file={0}/KEGG.enricher.R && '.format(script_path))
        r11.write('python {0}/get_bubble_input.py {1}/KEGG_enrichment/kegg_enrich.txt {0}/KEGG_pathway.tab && '.format(script_path, path))
        r11.write('R --slave --no-restore --file={0}/run_Bubble_Plot.R && conda deactivate; fi\n'.format(script_path)) 
    run_script('{}/shell/step12.KEGG_enrichment.sh'.format(path), 1)
    os.chdir(path)
    
########################################### main() is over ######################################
def run_script(sh_script, threads):
    sh_path = os.path.dirname(sh_script)
    sh_name = os.path.basename(sh_script)
    unfinish_sh = {}
    myfile = open(sh_script)
    numb = len(myfile.readlines())
    if os.path.exists('{0}/run_{1}/'.format(sh_path, sh_name)) and len(glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name))) == numb:
        if len(glob.glob('{0}/run_{1}/*.Check'.format(sh_path, sh_name))) == len(glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name))):
            print('Check last time run {} shell have completed.'.format(sh_script))
        else:
            for sh in glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name)):
                if os.path.exists('{}.Check'.format(sh)):
                    pass
                else:
                    k = 0
                    for efil in glob.glob('{}.*e*'.format(sh)):
                        #if os.path.getsize(efil) != 0:
                        k += 1  
                        #else:
                            #pass
                    if k == 3:
                        sys.exit()
                    else:
                        unfinish_sh[sh] = k
            multi_process(unfinish_sh, threads)
            run_script(sh_script, threads)
    else:
        subprocess.call('mkdir -p {0}/run_{1}/'.format(sh_path, sh_name), shell=True)
        subprocess.call('cd {3}/run_{4}/ && csplit {0} /\\n/ -n {1} -s {{*}} -f {2} -b \'%0{1}d.sh\''.format(sh_script, len(str(numb)), sh_name.replace("sh", ""), sh_path, sh_name), shell=True)
        subprocess.call('rm {0}/run_{1}/*.*00.sh {0}/run_{1}/*.0.sh'.format(sh_path, sh_name), shell=True)
        for sh in glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name)):
            subprocess.call('sed -i "$ s|$| \&\& echo This-Work-is-Completed! \&\& touch {0}.Check|" {0}'.format(sh), shell=True)
            unfinish_sh[sh] = 0
        #print(unfinish_sh.items())
        multi_process(unfinish_sh, threads)
        run_script(sh_script, threads)

def multi_process(script_dict, threads):
    # printing main program process id 
    print("ID of main process: {}".format(os.getpid())) 
    
    tmp = {}
    for i in range(threads):
        while len(script_dict) != 0:
            tmp[list(script_dict.keys())[0]] = script_dict[list(script_dict.keys())[0]]
            del script_dict[list(script_dict.keys())[0]]
    # creating processes
    proc = []
    if len(list(tmp.keys())) < threads:
        for t in range(len(list(tmp.keys()))):
            proc.append(multiprocessing.Process(target=run_cycle, args=(list(tmp.keys())[t], tmp[list(tmp.keys())[t]])))
    else:
        for t in range(threads):
            proc.append(multiprocessing.Process(target=run_cycle, args=(list(tmp.keys())[t], tmp[list(tmp.keys())[t]])))

    # starting processes
    k = 1
    for p in proc:
        p.start() 
        print("ID of the {0} process: {1}".format(k, p.pid))
        time.sleep(10)
        k += 1
    # wait until processes are finished
    for p in proc:
        p.join() 

def run_cycle(key, val):
    if val == 1:
        print('throw job {0} in the 2 cycle\n'.format(key))
        #print("That will continue the uncomplete jobs.\n")
        subprocess.run('bash {0} >>{0}.{1}o{2} 2>>{0}.{1}e{2}'.format(key, val+1, int(time.time())), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        time.sleep(5)
        if os.path.exists('{}.Check'.format(key)):
            pass
        else:
            val += 1
            run_cycle(key, val)
    elif val == 2:
        print('throw job {0} in the 3 cycle\n'.format(key))
        subprocess.run('bash {0} >>{0}.{1}o{2} 2>>{0}.{1}e{2}'.format(key, val+1, int(time.time())), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        time.sleep(5)
        if os.path.exists('{}.Check'.format(key)):
            pass
        else:
            print('Program stopped because the rerun cycle number has reached 3, the {} jobs unfinished.'.format(key))
            os._exit(0)
            sys.exit() 
    elif val == 3:
        print('Program stopped because the rerun cycle number has reached 3, the {} jobs unfinished.'.format(key))
        os._exit(0)
        sys.exit() 
    else:
        print('throw job {0} in the 1 cycle\n'.format(key))
        subprocess.run('bash {0} >>{0}.{1}o{2} 2>>{0}.{1}e{2}'.format(key, val+1, int(time.time())), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        time.sleep(5)
        if os.path.exists('{}.Check'.format(key)):
            pass
        else:
            val += 1
            run_cycle(key, val)
            
def mags_bins(clustfile, genefile):
    cluster_dict = {}
    k = 0
    fp=open(clustfile,"rb")
    parser=PDFParser(fp)
    doc=PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize("")
    resource=PDFResourceManager()
    laparam=LAParams()
    device=PDFPageAggregator(resource,laparams=laparam)
    interpreter=PDFPageInterpreter(resource,device)
    for page in doc.get_pages():
        k += 1
        interpreter.process_page(page)
        layout=device.get_result()
        for out in layout:
            if hasattr(out, 'get_text'): 
                print(out.get_text())
                if '.fa' in out.get_text():
                    cluster_dict.setdefault("MAG" + str(k), []).append(out.get_text().replace('\n', ''))

    with open(genefile,'r') as g:
        genome_info = [line.strip().split(',') for line in g.readlines()]

    subprocess.call('mkdir -p {0}/MAGs/'.format(path), shell=True, executable='/bin/bash')
    for key, val in cluster_dict.items():
        with open('{0}/MAGs/{1}.txt'.format(path, key),'w') as r:
            r.write("genome" + '\t' + "completeness" + '\t' + "contamination" + '\t' + "length" + '\t' + "N50" + '\n')
            for line in genome_info[1:]:
                for fa in val:
                    if line[0] in fa:
                        r.write(fa + '\t' + line[1] + '\t' + line[2] + '\t' + line[4] + '\t' + line[5] + '\n')
                        continue

def mags_cluster_info(clustfile, geneinfo, magpath, sampnumb, groupname, data_dict):
    group_dict = {}
    for sap, lis in data_dict.items():
        group_dict.setdefault(lis[-1], []).append(sap)
    
    cluster_dict = {}
    with open(clustfile,'r') as g:
        clustdata = [line.strip().split('\t') for line in g.readlines()]

    for clust in clustdata[1:]:
        if clust[1].split(';')[-1] == "s__":
            pass
        else:
            cluster_dict.setdefault(clust[1].split(';')[-1], []).append(clust[0])
    #print(cluster_dict)

    with open(geneinfo,'r') as g:
        genome_info = {line.strip().split(',')[0].replace(".fa", ""):line.strip().split(',')[1:] for line in g.readlines()}
    #print(genome_info.keys())

    cluster_gene_match = {}
    uniq_bins = {}
    
    for key, val in cluster_dict.items():
        gnumb=[]
        for v in val:
            if data_dict[v.split(".")[0]][-1] not in gnumb:
                gnumb.append(data_dict[v.split(".")[0]][-1])
        
        if len(val) > int(sampnumb)/2 + 1 and len(gnumb) == 2:
            for bins in val:
                if bins in genome_info.keys():
                    cluster_gene_match.setdefault(bins, []).extend(genome_info[bins])
                    score = 1*float(genome_info[bins][0])- 5*float(genome_info[bins][1])+ 0.5*math.log(float(genome_info[bins][-1])) #底数默认为e
                    cluster_gene_match.setdefault(bins, []).append(str(score))
                    cluster_gene_match.setdefault(bins, []).append(key)
                else:
                    print(bins)
        else:
            bins_list = []
            for v in val:
                bins_list.append(v.split('.')[0])
            for grop, samp in group_dict.items():
                if operator.eq(sorted(bins_list), sorted(samp)):
                    uniq_bins.setdefault(grop, []).append(key)
    #print(uniq_bins)
 
    for key, val in cluster_dict.items():
        g_num=[]
        for v in val:
            if data_dict[v.split(".")[0]][-1] not in g_num:
                g_num.append(data_dict[v.split(".")[0]][-1])
        
        if len(val) > int(sampnumb)/2 + 1 and len(g_num) == 2:
            raw_score = 0
            for v in val:
                if v in group_dict[groupname] and float(cluster_gene_match[v][-2]) > raw_score:
                    ref = v
                    raw_score = float(cluster_gene_match[v][-2])
            cluster_gene_match.setdefault(ref, []).append("reference genome")

    if cluster_gene_match:
        pass
    else:
        os.system("ls {0}/*.txt > {0}/mag.list".format(magpath))
        with open('{}/mag.list'.format(magpath)) as l:
            mag_list = [line.strip() for line in l.readlines()]
        for mag in mag_list:
            spe = "NA"
            with open(mag) as m:
                mag_cont = [line.strip().split("\t") for line in m.readlines()]
            
            gb=[]
            for cont in mag_cont[1:]:
                if data_dict[cont[0].split(".")[0]][-1] not in gb:
                    gb.append(data_dict[cont[0].split(".")[0]][-1])
            print(gb) 
            if len(mag_cont) > int(sampnumb) / 2 + 2 and len(gb) == 2:
                for cont in mag_cont[1:]:
                    if "*" in cont[0]:
                        for k, v  in cluster_dict.items():
                            for i in v:
                                if cont[0].replace(".fa", "").replace(" *", "") == i:
                                    spe = k
                for cont in mag_cont[1:]:
                    if spe != "NA":
                        cluster_gene_match.setdefault(cont[0].replace(".fa", "").replace(" *", ""), []).extend(cont[1:3])
                        cluster_gene_match.setdefault(cont[0].replace(".fa", "").replace(" *", ""), []).append("-")
                        cluster_gene_match.setdefault(cont[0].replace(".fa", "").replace(" *", ""), []).extend(cont[3:])
                        score = 1*float(cont[1])- 5*float(cont[2])+ 0.5*math.log(float(cont[-1])) #底数默认为e
                        cluster_gene_match.setdefault(cont[0].replace(".fa", "").replace(" *", ""), []).append(str(score))
                        cluster_gene_match.setdefault(cont[0].replace(".fa", "").replace(" *", ""), []).append(spe)
                        if "*" in cont[0]:
                            cluster_gene_match.setdefault(cont[0].replace(".fa", "").replace(" *", ""), []).append("reference genome")
                

    with open("{0}/drep_bins/bins_species_taxonomy.txt".format(os.getcwd()), 'w') as r:
        r.write("Bins" + '\t' + "completeness" + '\t' + "contamination" + '\t' + "strain_heterogeneity" + '\t' + "length" + '\t' + "N50" + '\t' + "Score" + '\t' + "Species"+ '\t' + "type" + '\n')
        for key, val in cluster_gene_match.items():
            if len(val) == 7:
                r.write(key + '\t' + '\t'.join(val) + '\t' + "query genome" + '\n')
                cluster_gene_match[key].append("query genome")
            elif len(val) == 8:
                r.write(key + '\t' + '\t'.join(val) + '\n')
            else:
                print("data missing\n")

    for key, val in uniq_bins.items():
        with open('{0}/drep_bins/{1}_uniq_species.txt'.format(os.getcwd(), key), 'w') as u:
            u.write("Bins" + '\t' + "completeness" + '\t' + "contamination" + '\t' + "strain_heterogeneity" + '\t' + "length" + '\t' + "N50" + '\t' + "Species" +  '\n')
            for v in val:
                for b in cluster_dict[v]:
                    u.write(b + '\t' + '\t'.join(genome_info[b]) + '\t' + v + '\n')
    
    return cluster_gene_match

def get_genome_size(fa_data):
    aList=[]
    with open(fa_data,'r') as f:
        for line in f:
            line = line.upper()
            if not line.startswith(">"):
                baseA = line.count("A")
                baseT = line.count("T")
                baseC = line.count("C")
                baseG = line.count("G")
                aList.extend([baseA, baseT, baseC, baseG])
                # print(aList)
    return sum(aList)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Description: generate and run shell scripts for every step",
        epilog="Example: python call_SVs_procedure.py config.ini")
    parser.add_argument('ifile', help='config.ini')
    args = parser.parse_args()

    main(args.ifile)
