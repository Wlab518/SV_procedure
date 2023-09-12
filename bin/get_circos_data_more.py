import os
import argparse

path = os.getcwd()

def main(inputfile, faidata, gffdata, mapdata, svnumber, svloc):
    map_dict = {}
    with open(mapdata,'r') as m:
        for line in m.readlines():
            if line.strip().split('\t')[0] == "sample_IDs":
                pass
            else:
                map_dict.setdefault(line.strip().split('\t')[3], []).append(line.strip().split('\t')[0])
    
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

    
    with open(inputfile,'r') as g:
        indata = [line.strip() for line in g.readlines()]
    sv_numb = {}
    sv_info = []
    for gro in map_dict.keys():
        #print(map_dict[gro])
        result_dict = {}
        for infile in indata:
            sample = infile.split('/')[-1].split('.')[0].replace('query_', '')
            if sample in [i for i in map_dict[gro]]:
                with open(infile,'r') as f:
                    svdata = [line.strip().split("\t") for line in f.readlines()]
                deletion = insertion = transloc = duplic = inversion = 0
                for iline in svdata[1:]:
                    ref_stop = int(fai_dict[iline[0]])
                    if int(iline[2]) <= int(svloc) or int(iline[3]) >= ref_stop - int(svloc):
                        pass
                    else:
                        if iline[5] == "insertion" and int(iline[3]) > ref_stop:
                            iline[3] = ref_stop
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
                        sv_info.append(sample + "+" + iline[0]+"+"+ iline[2] +"+"+ iline[3] +"+label="+ iline[5])
                        keys = iline[0]+ "+" + iline[2] + "+" + iline[3] + "+" + iline[4] + "+" + iline[5]

                        if keys not in result_dict.keys():
                            result_dict[keys] = 1
                        else:
                            result_dict[keys] += 1
                sv_numb.setdefault(sample, []).extend([str(deletion),str(insertion),str(transloc),str(inversion),str(duplic)])

        with open("{}_tile.dat".format(gro),'w') as r2:        
            for key, val in result_dict.items():
                r2.write(key.split("+")[0] + '\t' + key.split("+")[1] + '\t' + key.split("+")[2] + '\t' + 'label=' + key.split("+")[4] + '\n')
        with open("{}_line.dat".format(gro),'w') as r3:        
            for key, val in result_dict.items():
                r3.write(key.split("+")[0] + '\t' + key.split("+")[1] + '\t' + key.split("+")[2] + '\t' + str(val) + '\t' + 'label=' + key.split("+")[4] + '\n')
    with open(svnumber,'w') as r1:
        r1.write("Samples" + '\t' + "Deletions" + '\t' + "Insertions" + '\t' + "Translocations" + '\t' + "Inversions" + '\t' + "Duplications" + '\n')
        for k, v in sv_numb.items():
            r1.write(k + '\t' + '\t'.join(v) + '\n')

    with open("sv_info.txt",'w') as r2:
        for value in sv_info:
            r2.write(value.split("+")[0]  + '\t' + value.split("+")[1] + '\t' + value.split("+")[2] + '\t' + value.split("+")[3] + '\t' + value.split("+")[4] + '\n')

    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="run procedure",
        epilog="Example: get_circos_data.py run.SVs_all.list ref.fa.fai ref.fa.gff sample_info.txt SVs_number_static.txt")
    parser.add_argument('inputfile', help='input file: run.SVs_all.list')
    parser.add_argument('faidata', help='input file: ref.fa.fai')
    parser.add_argument('gffdata', help='input file: ref.fa.gff')
    parser.add_argument('mapdata', help='input file: sample_info.txt')
    parser.add_argument('svnumber', help='output file: sv number static')
    parser.add_argument('svloc', help='SV events within the distance (bp) of the start/end point of contigs in MAGs are not considered, default=10')
    
    args = parser.parse_args()

    main(args.inputfile, args.faidata, args.gffdata, args.mapdata, args.svnumber, args.svloc)
