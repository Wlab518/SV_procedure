import os
import argparse

path = os.getcwd()

def main(ifile, sfile, svabund, ids):

    with open(ifile,'r') as g:
        indata = [line.strip() for line in g.readlines()]
    
    with open(sfile,'r') as s:
        sdata = [line.strip().split("\t") for line in s.readlines()]

    grop_dict = {}
    for samp in sdata[1:]:
        if samp[-1] not in grop_dict.keys():
            grop_dict.setdefault(samp[-1], []).append(1)
        else:
            grop_dict[samp[-1]][0] += 1
           
    with open('{}/tile.conf'.format(path),'w') as r:
        for grop in grop_dict.keys():
            if grop == ids:
                r.write('<plot>\n')
                r.write('show = yes\n')
                r.write('type = tile\n')
                r.write('layers_overflow = hide\n')
                r.write('file = {}_tile.dat\n'.format(grop))
                r.write('r0 = 0.85r\n')
                r.write('r1 = 0.95r\n')
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
                r.write('<plot>\n')
                r.write('show = yes\n')
                r.write('type = tile\n')
                r.write('layers_overflow = hide\n')
                r.write('file = {}_tile.dat\n'.format(grop))
                r.write('r0 = 1.05r\n')
                r.write('r1 = 1.15r\n')
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
    
    for fline in indata:
        with open(fline,'r') as f:
            infil = [line.strip().split("\t") for line in f.readlines()]
        for fil in infil:
            if len(grop_dict[fline.replace("_line.dat", "")]) == 1:
                grop_dict.setdefault(fline.replace("_line.dat", ""), []).append(fil[3])
            else:
                if int(fil[3]) > int(grop_dict[fline.replace("_line.dat", "")][1]):
                    grop_dict[fline.replace("_line.dat", "")][1] = fil[3]
    #print(grop_dict)
    with open('{}/line.conf'.format(path),'w') as r1:
        for grop, val in grop_dict.items():
            if grop == ids:
                r1.write('<plot>\n')
                r1.write('type = line\n')
                r1.write('thickness = 2\n')
                r1.write('max_gap = 1u\n')
                r1.write('file = {}_line.dat\n'.format(grop))
                r1.write('min = 0\n')
                r1.write('max = {}\n'.format(str(val[1])))
                r1.write('r0 = 0.2r\n')
                r1.write('r1 = 0.7r\n')
                r1.write('orientation = in\n')
                r1.write('color = vlgrey\n')
                r1.write('<rules>\n')
                r1.write('<<include line_rule.conf>>\n')
                r1.write('</rules>\n')
                r1.write('</plot>\n')
                r1.write('\n')
            else:
                r1.write('<plot>\n')
                r1.write('type = line\n')
                r1.write('thickness = 2\n')
                r1.write('max_gap = 1u\n')
                r1.write('file = {}_line.dat\n'.format(grop))
                r1.write('min = 0\n')
                r1.write('max = {}\n'.format(str(val[1])))
                r1.write('r0 = 1.3r\n')
                r1.write('r1 = 1.8r\n')
                r1.write('color = vlgrey\n')
                r1.write('<rules>\n')
                r1.write('<<include line_rule.conf>>\n')
                r1.write('</rules>\n')
                r1.write('</plot>\n')
                r1.write('\n')
    threshold = grop_dict[ids][0]*(float(svabund.strip("%"))/100)
    with open('{}/line_rule.conf'.format(path),'w') as r2:
        r2.write('<rule>\n')
        r2.write('condition = var(label) eq "duplication" && var(value) >= {}\n'.format(str(threshold)))
        r2.write('color = 147,112,219\n')
        r2.write('</rule>\n')
        r2.write('\n')
        r2.write('<rule>\n')
        r2.write('condition = var(label) eq "deletion" && var(value) >= {}\n'.format(str(threshold)))
        r2.write('color = 219,112,147\n')
        r2.write('</rule>\n')
        r2.write('\n')
        r2.write('<rule>\n')
        r2.write('condition = var(label) eq "insertion" && var(value) >= {}\n'.format(str(threshold)))
        r2.write('color = 95,158,160\n')
        r2.write('</rule>\n')
        r2.write('\n')
        r2.write('<rule>\n')
        r2.write('condition = var(label) eq "transloc" && var(value) >= {}\n'.format(str(threshold)))
        r2.write('color = 222,184,135\n')
        r2.write('</rule>\n')
        r2.write('\n')
        r2.write('<rule>\n')
        r2.write('condition = var(label) eq "inversion" && var(value) >= {}\n'.format(str(threshold)))
        r2.write('color = 60,179,113\n')
        r2.write('</rule>\n')   


        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="get tile.conf",
        epilog="Example: python get_circos_tile_conf.py line.list sample_info.txt AOM")
    parser.add_argument('ifile', help='input file: line.list')
    parser.add_argument('sfile', help='input file: sample_info.txt')
    parser.add_argument('svabund', help='input: a threshold for sv abundance in samples within a group')
    parser.add_argument('ids', help='input: id for the "orientation = in" of circos')
    
    
    args = parser.parse_args()

    main(args.ifile, args.sfile, args.svabund, args.ids)
