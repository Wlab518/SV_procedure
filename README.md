Introduction

This is a pipeline combining Nanopore long reads and Illumina short reads to analyze SVs in the microbial genomes from gut microbiome, and further identify differential SVs that can be reflective of metabolic differences. The pipeline integrates multiple software tools and its core mission consists of 13 steps, including the creation of soft links, quality control and sequence statistics, removal of host reads, metagenome assembly and evaluation, extraction of high-quality draft genomes (bins) and de-replication, species taxonomy and gene models of bins, detection and visualization of SVs, and KEGG enrichment analyses. The pipeline gives researchers easy access to SVs and relevant metabolites in the microbial genomes without the requirement of specific technical expertise, which is particularly useful to researchers interested in metagenomic SVs but lacking sophisticated bioinformatic knowledge.

###Please ensure that free space of the working path is greater than 1T

all scripts and dependencies (including database): 140G

test data: 60G

the running result of the project (with 10 samples): 800G



Installation

1.To install Miniconda on a typical Linux/Unix system run the following commands:

`wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh`

`chmod 755 Miniconda3-py38_4.9.2-Linux-x86_64.sh`

`sh Miniconda3-py38_4.9.2-Linux-x86_64.sh`

`conda info`  #View the default conda environment path

`vi ~/.condarc`  #To modify "envs_dirs" and "pkgs_dirs"

#the "$conda_path" means the install path of miniconda3, for example, conda_path=/use/bin/miniconda3

`vi ~/.bashrc` # To add `export PATH="/use/bin/miniconda3/bin:$PATH"`

2.To download test data, there are the two ways. 

1> all scripts and dependencies of our pipeline from the Baidu Cloud:

Click the link: https://pan.baidu.com/s/1ErKeJ0_2D-XEwGWWbq1O_A

Password: L518 

##Test data is stored in the "data" folder. The "sample_info.txt" and "config.ini" files are sample information of test data and the configuration file (including a set of the main parameters that control pipeline execution), respectively.
##All dependencies of our pipeline are packaged into "miniconda3_env.tar.gz" file and need to be extracted to "$conda_path/". 
##All scripts (written in Python 3) of our pipeline are packaged into "SV_procedure.tar.gz" file, and should be extracted to the "$conda_path/envs/mySVenv_python3/" path as follows: 

`cd $conda_path/ && rm -r envs`

`tar -xzf miniconda3_envs.tar.gz`

`cd $conda_path/envs/mySVenv_python3`

`tar -xzf SV_procedure.tar.gz`

2>all scripts and dependencies of our pipeline from the Terabox:

Click the link: https://1024tera.com/s/1zgl2ywN2ZsNBxSptc5USww 

##Test data is stored in the "data" folder. The "sample_info.txt" and "config.ini" files are sample information of test data and the configuration file (including a set of the main parameters that control pipeline execution), respectively. Note: the TD5, TD59 and TD7 samples need to be merged, respectively. such as `cat data/TD7/TD7.fq.gz.* > ../TD7.fq.gz`
##All dependencies of our pipeline are packaged into "miniconda3_envs" folder and need to be merged and extracted to "$conda_path/".
##All scripts (written in Python 3) of our pipeline are packaged into "SV_procedure.tar.gz" file, and should be extracted to the "$conda_path/envs/mySVenv_python3/" path as follows: 

`cd $conda_path/ && rm -r envs`

`cat miniconda3_envs/miniconda3_envs.tar.gz.* | tar zxv`

`cd $conda_path/envs/mySVenv_python3`

`tar -xzf SV_procedure.tar.gz`


Usage

1.To prepare the table of the data information according to the "$conda_path/envs/mySVenv_python3/SV_procedure/test/sample_info.txt" file

##"sample_info.txt" file used to save the table of sample information, including 4 columns separated by TAB

#sample_IDs: sample names

#NGS_rawnames: the names of Illumina sequence data

#ONT_rawnames: the names of Nanopore sequence data

#group: the group names of the sample

##the $outdir means the working path of the project, which should correspond to the outdir parameters of the "config.ini" file

`cd $outdir && vi sample_info.txt`

2.To prepare the configuration file as the pipeline input according to the "$conda_path/envs/mySVenv_python3/SV_procedure/test/config.ini" file

##the following parameters in "config.ini" file must be modified:

#conda, datapath, infotable, outdir, group_name(based on the information of "sample_info.txt" file)

3.To run the pipeline on the dataset, simply use the following command (we recommend using the "nohup" command to run the pipeline in the background):

`$conda_path/bin/python $conda_path/envs/mySVenv_python3/SV_procedure/call_SVs_procedure.py config.ini`
 
 
 
Output

The output includes the source code, the running process and the running results of the scripts. In order to support the process traceability, a "shell/" directory is first generated to hold the script files, and then the specific process of script execution is stored in the "step*.sh.*e*" (stored error information) and the "step*.sh.*o*" (stored the normal process) files in the "run_*.sh" sub-folders of the current folder. Taking the step12 KEGG enrichment analysis as an example, the running process of the "step12.KEGG_enrichment.sh" script is stored in the "run_step12.KEGG_enrichment.sh" folder. If the script is functioning normally, the "step12.KEGG_enrichment.1.sh.Check" file is generated. If not, the execution will exit after the loop has executed three times. The resulting output files from step 0 to step 12 are respectively stored in the following directories: "rawdata_10ge/", "qc/", "cleandata/", "assembly/", "binning/", "drep_bins/", "gene_model/", "taxonomy/", "SV/", "KEGG_enrichment/" and "result_stat/".



Error

when the program failure occurs due to a variety of corruption or bugs (such as file, network or disk issues), the program execution does not simply exit but enters the next execution using an identical scripting code. After the loop executes three times, if the failure still exists, the program will exit and errors in during this step will be stored in the "$outdir/shell/run_step*/*.e*" files. After troubleshooting, we can delete the result files (or folders) generated by the error step and its script execution files such as "*.1o*, *.1e*, *.2o*, *.2e*, *.3o*, *.3e*" (or this "run_step*" folder), and then rerun the pipeline:

`$conda_path/bin/python $conda_path/envs/mySVenv_python3/SV_procedure/call_SVs_procedure.py config.ini`

By now, the program will be able to recover from the nearest checkpoint rather than overwrite otherwise usable intermediate files, obviating the need to restart from the beginning of a process.



Examples

The example project can be found in the following directory:
 $conda_path/envs/mySVenv_python3/SV_procedure/test 
