import os
import argparse

path = os.getcwd()

def main(inputfile, faidata, gffdata, circosdata, svnumber, svloc):
    sample = inputfile.split('/')[-1].split('.')[0].replace('query_', '')
    with open(inputfile,'r') as g:
        indata = [line.strip().split('\t') for line in g.readlines()]
    with open(faidata,'r') as f:
        fai_dict = {line.strip().split('\t')[0]:line.strip().split('\t')[1] for line in f.readlines()}
    if os.path.exists('{}/gene.dat'.format(path)):
        pass
    else:
        with open(gffdata,'r') as d:
            gfdata = [line.strip().split('\t') for line in d.readlines()]
        
        gff_dict = {}
        k = 0
        for gff in gfdata:
            if gff[0].startswith("#"):
                pass
            elif len(gff) < 8:
                pass
            elif "ID=" not in gff[8].split(";")[0]:
                pass
            else:
                k += 1
                gff_dict.setdefault(k, []).append(gff[0])
                gff_dict.setdefault(k, []).append(gff[3])
                gff_dict.setdefault(k, []).append(gff[4])
                gff_dict.setdefault(k, []).append(gff[8].split(";")[0])
                for i in gff[8].split(";")[1:]:
                    if i.startswith("gene="):
                        gff_dict.setdefault(k, []).append(i)
                        break
        with open('{}/gene.dat'.format(path),'w') as r2:
            for val in gff_dict.values():
                if len(val) < 5:
                    r2.write('\t'.join(val) + '\t' + "gene=Null" + '\n')
                else:
                    r2.write('\t'.join(val) + '\n')


    result_dict = {}
    deletion = insertion = transloc = duplic = inversion = 0
    k = 0
    for iline in indata[1:]:
        ref_stop = int(fai_dict[iline[0]])
        if int(iline[2]) <= int(svloc) or int(iline[3]) >= ref_stop - int(svloc):
            pass
        else:
            if iline[5] == "insertion" and int(iline[3]) > ref_stop:
                iline[3] = ref_stop
            k += 1
            if iline[5] == "deletion":
                #color = "219,112,147"
                deletion += 1
            elif iline[5] == "insertion":
                #color = "95,158,160"
                insertion += 1
            elif iline[5] == "transloc":
                #color = "222,184,135"
                transloc += 1
            elif iline[5] == "inversion":
                #color = "60,179,113"
                inversion += 1
            else:
                #color = "147,112,219"
                duplic += 1
            result_dict.setdefault(iline[0]+"-"+str(k), []).append(iline[2])
            result_dict.setdefault(iline[0]+"-"+str(k), []).append(str(iline[3]))
            #result_dict.setdefault(iline[0]+"-"+str(k), []).append(color)
            result_dict.setdefault(iline[0]+"-"+str(k), []).append('label=' + iline[5])
        
    with open(circosdata,'w') as r:        
        for key, val in result_dict.items():
            r.write(key.split("-")[0] + '\t' + '\t'.join(val) + '\n')
    with open(svnumber,'w') as r1:
        r1.write("Samples" + '\t' + "Deletions" + '\t' + "Insertions" + '\t' + "Translocations" + '\t' + "Inversions" + '\t' + "Duplications" + '\n')
        r1.write(sample + '\t' + str(deletion) + '\t' + str(insertion) + '\t' + str(transloc) + '\t' + str(inversion) + '\t' + str(duplic) + '\n')

    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="run procedure",
        epilog="Example: get_circos_data.py run.SVs_all.tsv ref.fa.fai ref.fa.gff sv_static.txt")
    parser.add_argument('inputfile', help='input file: run.SVs_all.tsv')
    parser.add_argument('faidata', help='input file: ref.fa.fai')
    parser.add_argument('gffdata', help='input file: ref.fa.gff')
    parser.add_argument('circosdata', help='output file: circos inputdata')
    parser.add_argument('svnumber', help='output file: sv number static')
    parser.add_argument('svloc', help='SV events within the distance (bp) of the start/end point of contigs in MAGs are not considered, default=10')
    
    args = parser.parse_args()

    main(args.inputfile, args.faidata, args.gffdata, args.circosdata, args.svnumber, args.svloc)
