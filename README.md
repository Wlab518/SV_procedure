
Introduction

This is a pipeline combining Nanopore long reads and Illumina short reads to analyze SVs in the microbial genomes from gut microbiome, and further identify differential SVs that can be reflective of metabolic differences. The pipeline integrates multiple software tools and its core mission consists of 13 steps, including the creation of soft links, quality control and sequence statistics, removal of host reads, metagenome assembly and evaluation, extraction of high-quality draft genomes (bins) and de-replication, species taxonomy and gene models of bins, detection and visualization of SVs, and KEGG enrichment analyses. The pipeline gives researchers easy access to SVs and relevant metabolites in the microbial genomes without the requirement of specific technical expertise, which is particularly useful to researchers interested in metagenomic SVs but lacking sophisticated bioinformatic knowledge.

Installation

1.To install Miniconda on a typical Linux/Unix system run the following commands:

wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh

chmod 755 Miniconda3-py38_4.9.2-Linux-x86_64.sh

sh Miniconda3-py38_4.9.2-Linux-x86_64.sh

2.To download all scripts and example results of our pipeline run the following commands:

git clone https://github.com/Wlab518/SV_procedure.git

3.To install dependencies of our pipeline to Miniconda3 according to the “SV_procedure-new/config.ini” file  

minimap2: 

wget https://github.com/lh3/minimap2/releases/download/v2.17/minimap2-2.17_x64-linux.tar.bz2

tar -jxvf minimap2-2.17_x64-linux.tar.bz2

cd minimap2-2.17_x64-linux/

metaspades:
wget http://cab.spbu.ru/files/release3.13.0/SPAdes-3.13.0-Linux.tar.gz

tar -xzf SPAdes-3.13.0-Linux.tar.gz

cd SPAdes-3.13.0-Linux/bin/

mumandco:

git clone https://github.com/SAMtoBAM/MUMandCo.git

opera_ms:

git clone https://github.com/CSB5/OPERA-MS.git

cd OPERA-MS

make

perl OPERA-MS.pl check-dependency

diamond:

wget http://github.com/bbuchfink/diamond/releases/download/v0.9.25/diamond-linux64.tar.gz

tar xzf diamond-linux64.tar.gz

Other conda environments, such as metawrap:

conda create -y -n metawrap1.2 python=2.7

conda activate metawrap1.2

conda install -y -c ursky metawrap-mg=1.2.0

Usage

1.To prepare the table of the data information according to the “SV_procedure/test/sample_info.txt” file

cd $outdir && vi sample_info.txt

2.To prepare the configuration file as the pipeline input according to the “SV_procedure/test/config.ini” file

3.To run the pipeline on the dataset, simply use the following command (we recommend using nohup to run the command in the background):

python SV_procedure-new/call_SVs_procedure.py config.ini 
 
Output

The output includes the source code, the running process and the running results of the scripts. In order to support the process traceability, a "shell/" directory is first generated to hold the script files, and then the specific process of script execution is stored in the "step*.sh.*e*" (stored error information) and the "step*.sh.*o*" (stored the normal process) files in the "run_*.sh" sub-folders of the current folder. Taking the step12 KEGG enrichment analysis as an example, the running process of the "step12.KEGG_enrichment.sh" script is stored in the "run_step12.KEGG_enrichment.sh" folder. If the script is functioning normally, the "step12.KEGG_enrichment.1.sh.Check" file is generated. If not, the execution will exit after the loop has executed three times. The resulting output files from step 0 to step 12 are respectively stored in the following directories: "rawdata_10ge/", "qc/", "cleandata/", "assembly/", "binning/", "drep_bins/", "gene_model/", "taxonomy/", "SV/", "KEGG_enrichment/" and "result_stat/".

Examples

The example project can be found in the following directory: “SV_procedure/test”


