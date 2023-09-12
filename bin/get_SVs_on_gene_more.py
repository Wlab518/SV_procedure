import os
import argparse

path = os.getcwd()

def main(ifile, gfile, ofile):
    
    with open(gfile,'r') as d:
        gdata = {line.strip().split('\t')[0]+'-'+line.strip().split('\t')[1]+'-'+line.strip().split('\t')[2]:line.strip().split('\t')[3:] for line in d.readlines()}

    result_dict = {}
    with open(ifile,'r') as f:
        fdata = [line.strip().split('\t')[1]+'-'+line.strip().split('\t')[2]+'-'+line.strip().split('\t')[3]+'-'+line.strip().split('\t')[0]+'-'+line.strip().split('\t')[4] for line in f.readlines()]
    
    for gff in gdata.keys():
        for f in fdata:
            if f not in result_dict.keys():
                result_dict[f] = []
            if f.split("-")[0] == gff.split("-")[0]:
                if int(gff.split("-")[1]) <= int(f.split("-")[1]) < int(gff.split("-")[2]) and int(gff.split("-")[1]) < int(f.split("-")[2]) <= int(gff.split("-")[2]):
                    result_dict.setdefault(f, []).extend([gff.split("-")[1],gff.split("-")[2],gdata[gff][0],gdata[gff][1],"gene middle"])
                elif int(gff.split("-")[1]) < int(f.split("-")[2]) <= int(gff.split("-")[2]) and int(f.split("-")[1]) < int(gff.split("-")[1]):
                    result_dict.setdefault(f, []).extend([gff.split("-")[1],gff.split("-")[2],gdata[gff][0],gdata[gff][1],"gene begin"])
                elif int(gff.split("-")[1]) <= int(f.split("-")[1]) < int(gff.split("-")[2]) and int(f.split("-")[2]) > int(gff.split("-")[2]):
                    result_dict.setdefault(f, []).extend([gff.split("-")[1],gff.split("-")[2],gdata[gff][0],gdata[gff][1],"gene end"]) 
                else:
                    pass 
            else:
                pass

    with open(ofile,'w') as r:
        r.write("sample" + '\t' + "seq_id" + '\t' + "sv_start" + '\t' + "sv_end" + '\t' + "sv_type" + '\t' + "gene_start" + '\t' + "gene_end" + '\t' + "gene_id" + '\t' + "gene_name" + "sv_location on gene" + '\n')
        r.write("total {} gene of reference genome".format(len(gdata.keys())) + '\n')
        for key, val in result_dict.items():
            r.write(key.split("-")[3] + '\t' + key.split("-")[0] + '\t' + key.split("-")[1] + '\t' + key.split("-")[2] + '\t' + key.split("-")[4] + '\t' + '\t'.join(val) + '\n')
    with open('{}/SV-affected_genes.list'.format(path),'w') as r1:
        for value in result_dict.values():
            for v in value:
                if v.startswith("ID="):
                    r1.write(v.replace("ID=", "") + '\n')

    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="static sv numbers on gene",
        epilog="Example: get_SVs_for_gene.py sv_info.txt SVs_for_gene.txt")
    parser.add_argument('ifile', help='input file: sv_info.txt')
    parser.add_argument('gfile', help='input file: gene.dat')
    parser.add_argument('ofile', help='output file: SVs_for_gene.txt')
    
    args = parser.parse_args()

    main(args.ifile, args.gfile, args.ofile)
