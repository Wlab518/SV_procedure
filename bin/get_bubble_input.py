import os
import argparse

path = os.getcwd()

def main(ifile, gfile):
    
    with open(ifile,'r') as g:
        indata = {line.strip().split('\t')[0]:line.strip().split('\t')[1:] for line in g.readlines()}
    with open(gfile,'r') as d:
        gdata = {line.strip().split('\t')[0]:line.strip().split('\t')[1:] for line in d.readlines()}
    
    with open('{}/input.txt'.format(path),'w') as r:
        r.write("x" + '\t' + "KEGG_level1" + '\t' + "KEGG_level3" + '\t' + "GeneNumber" + '\t' + "FoldEnrichment" + '\t' + "p.adj" + '\t' + "ID" + '\n')
        for k, v in indata.items():
            if k=="ID":
                pass
            else:
                if k in gdata.keys():
                    level1=gdata[k][1].replace(' ', '_')
                    level3=gdata[k][3].replace(' ', '_').replace('_/_', '_').replace(')', '').replace('(', '').replace(',', '')
                    foldEnrichment=(float(indata[k][1].split("/")[0])/float(indata[k][1].split("/")[1]))/(float(indata[k][2].split("/")[0])/float(indata[k][2].split("/")[1]))

                    r.write("1" + '\t' + level1 + '\t' + level3 + '\t' + indata[k][-1] + '\t' + str(foldEnrichment) + '\t' + indata[k][4] + '\t' + k + '\n')
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="get bubble plot input file",
        epilog="Example: python get_bubble_input.py kegg_enrich.txt pathway.tab")
    parser.add_argument('ifile', help='input file: kegg_enrich.txt')
    parser.add_argument('gfile', help='input file: pathway.tab')
    
    args = parser.parse_args()

    main(args.ifile, args.gfile)
