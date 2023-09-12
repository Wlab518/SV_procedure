import os
import argparse

path = os.getcwd()

def main(ifile, sfile, ids):

    with open(ifile,'r') as g:
        indata = [line.strip() for line in g.readlines()]
    with open(sfile,'r') as s:
        slist = [line.strip().split('\t') for line in s.readlines()]
        
    f_dict = {}
    for sap in slist[1:]:
        if sap[-1] == ids:
            f_dict.setdefault("in", []).append(sap[0])
        else:
            f_dict.setdefault("out", []).append(sap[0])
     
    with open('{}/tile.conf'.format(path),'w') as r:
        #r.write('show = yes\n')
        #r.write('type = tile\n')
        #r.write('layers_overflow = hide\n')
        for key, val in f_dict.items():
            if key == "in":
                rl = 0.999-len(val)*0.1
                for fil in indata:
                    for samp in val:
                        if fil.split("/")[-1].split(".")[0].replace("query_", "") == samp:
                            r.write('<plot>\n')
                            r.write('file = {}\n'.format(fil))
                            r.write('r0 = {}r\n'.format("%.3f" %(rl)))
                            rl = rl+0.1
                            r.write('r1 = {}r\n'.format("%.3f" %(rl)))
                            r.write('orientation = in\n')
                            r.write('layers = 15\n')
                            r.write('margin = 0.02u\n')
                            r.write('thickness = 15\n')
                            r.write('padding = 1\n')
                            r.write('stroke_thickness = 2\n')
                            r.write('<rules>\n')
                            r.write('<<include rule.conf>>\n')
                            r.write('</rules>\n')
                            r.write('</plot>\n')
                            r.write('\n')
            else:
                rl = 1.001
                for fil in indata:
                    for samp in val:
                        if fil.split("/")[-1].split(".")[0].replace("query_", "") == samp:
                            r.write('<plot>\n')
                            r.write('file = {}\n'.format(fil))
                            r.write('r0 = {}r\n'.format("%.3f" %(rl)))
                            rl = rl+0.1
                            r.write('r1 = {}r\n'.format("%.3f" %(rl)))
                            r.write('orientation = out\n')
                            r.write('layers = 15\n')
                            r.write('margin = 0.02u\n')
                            r.write('thickness = 15\n')
                            r.write('padding = 1\n')
                            r.write('stroke_thickness = 2\n')
                            r.write('<rules>\n')
                            r.write('<<include rule.conf>>\n')
                            r.write('</rules>\n')
                            r.write('</plot>\n')
                            r.write('\n')

        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="get tile.conf",
        epilog="Example: python get_circos_tile_conf.py tile_input.list sample_info.txt AOM")
    parser.add_argument('ifile', help='input file: tile_input.list')
    parser.add_argument('sfile', help='input file: sample_info.txt')
    parser.add_argument('ids', help='input: id for the "orientation = in" of circos')
    
    
    args = parser.parse_args()

    main(args.ifile, args.sfile, args.ids)
