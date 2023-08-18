# Introduction

MetaSVs is a pipeline combining Nanopore long reads and Illumina short reads to analyze SVs in the microbial genomes from gut microbiome, and further identify differential SVs that can be reflective of metabolic differences. The pipeline integrates multiple software tools and its core mission consists of 13 steps, including the creation of soft links, quality control and sequence statistics, removal of host reads, metagenome assembly and evaluation, extraction of high-quality draft genomes (bins) and de-replication, species taxonomy and gene models of bins, detection and visualization of SVs, and KEGG enrichment analyses. MetaSVs gives researchers easy access to SVs and relevant metabolites in the microbial genomes without the requirement of specific technical expertise, which is particularly useful to researchers interested in metagenomic SVs but lacking sophisticated bioinformatic knowledge.

![image](https://github.com/Wlab518/SV_procedure/blob/main/fig/fig1.png)

# Installation

To install with Docker, run:

`# Docker installation`

`docker pull wanglab518/metasvs:latest`

![image](https://github.com/Wlab518/SV_procedure/blob/main/fig/fig2.png)

# Databases

In addition to the Docker installation, you will need to configure the paths to some databases that you downloaded onto your system according to the following guide.

| Database | Size |	Used in module |
| -------- | ---- | -------------- |
| CheckM_db |	1.4G |	binning, de-replication |
| gtdbtk_db	| 49G	| taxonomy |
| kobas_db |	54G	| KEGG enrichment |

1.Downloading the CheckM database:

`mkdir CheckM_db && cd CheckM_db`

`wget https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz`

`tar xvzf checkm_data_2015_01_16.tar.gz`

`rm checkm_data_2015_01_16.tar.gz`

2.Downloading the gtdbtk database:

`wget https://data.gtdb.ecogenomic.org/releases/release202/202.0/auxillary_files/gtdbtk_r202_data.tar.gz`

`tar xvzf gtdbtk_r202_data.tar.gz` 

`mv release202 gtdbtk_db` 

`rm gtdbtk_r202_data.tar.gz`

3.Downloading the kobas database:

`mkdir kobas_db && cd kobas_db`

`#to download sqlite3.tar.gz and seq_pep.tar.gz`

`Link: ftp://ftp.cbi.pku.edu.cn/pub/KOBAS_3.0_DOWNLOAD/`

`tar xvzf sqlite3.tar.gz  && tar xvzf seq_pep.tar.gz`

`rm sqlite3.tar.gz seq_pep.tar.gz`

# Usage

1.To create a working directory

`mkdir -p $workpath && cd $workpath`

2.To run a MetaSVs docker container:

`docker run --name sv_project -v $workpath:/opt/project -idt wanglab518/metasvs`

`docker start sv_project`

`docker exec -it sv_project /bin/bash`

3.To prepare the table of the data information according to the “SV_procedure/test/sample_info.txt” file

##“sample_info.txt” file used to save the table of sample information, including 4 columns separated by TAB

#sample_IDs: sample names

#NGS_rawnames: the names of Illumina sequence data

#ONT_rawnames: the names of Nanopore sequence data

#group: the group names of the sample

`vi sample_info.txt`

4.To prepare the configuration file as the pipeline input according to the “SV_procedure/test/config.ini” file

`vi config.in  #including the path of database downloaded above, raw sequence data and so on`

5.To run the pipeline in a docker container, simply use the following command (we recommend using the “nohup” command to run the pipeline in the background):

`cd /opt/project`

`python /opt/conda/SV_procedure/call_SVs_procedure.py config.ini` 
 
# Output

The output includes the source code, the running process and the running results of the scripts. In order to support the process traceability, a "shell/" directory is first generated to hold the script files, and then the specific process of script execution is stored in the "step*.sh.*e*" (stored error information) and the "step*.sh.*o*" (stored the normal process) files in the "run_*.sh" sub-folders of the current folder. Taking the step12 KEGG enrichment analysis as an example, the running process of the "step12.KEGG_enrichment.sh" script is stored in the "run_step12.KEGG_enrichment.sh" folder. If the script is functioning normally, the "step12.KEGG_enrichment.1.sh.Check" file is generated. If not, the execution will exit after the loop has executed three times. The resulting output files from step 0 to step 12 are respectively stored in the following directories: "rawdata_10ge/", "qc/", "cleandata/", "assembly/", "binning/", "drep_bins/", "gene_model/", "taxonomy/", "SV/", "KEGG_enrichment/" and "result_stat/".

![image](https://github.com/Wlab518/SV_procedure/blob/main/fig/fig3.png)

# Error

when the program failure occurs due to a variety of corruption or bugs (such as file, network or disk issues), the program execution does not simply exit but enters the next execution using an identical scripting code. After the loop executes three times, if the failure still exists, the program will exit and errors in during this step will be stored in the “shell/run_step*/*.e*” files. After troubleshooting, we can delete the “*.1o*, *.1e*, *.2o*, *.2e*, *.3o*, *.3e*” files or this “run_step*” folder, and then rerun the pipeline:

`python /opt/conda/SV_procedure/call_SVs_procedure.py config.ini`

By now, the program will be able to recover from the nearest checkpoint rather than overwrite otherwise usable intermediate files, obviating the need to restart from the beginning of a process.

# Examples

The example project can be found in the following directory: SV_procedure/test 
