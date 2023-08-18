import os
import argparse
import gzip

path = os.getcwd()

def main(ifile, ofile):
    n = 0
    indata={}
    if ifile.endswith(".gz"):
        f=gzip.open(ifile, 'rb')
        for line in f.readlines():
            if n % 4 == 1:
                indata[n]=len(line.decode())
            n += 1
        #indata = [line.decode() for line in f.readlines()]            
    else:
        with open(ifile,'r') as g:
            for line in g.readlines():
                if n % 4 == 1:
                    indata[n]=len(line)
                n += 1
            #indata = [line.strip() for line in g.readlines()]
    data_dict = {}
    data_dict["0-500"]=0
    data_dict["500-800"]=0
    data_dict["800-1000"]=0
    data_dict["1000-1200"]=0
    data_dict["1200-1400"]=0
    data_dict["1400-1600"]=0
    data_dict["1600-1800"]=0
    data_dict["1800-2000"]=0
    data_dict["2000-2200"]=0
    data_dict["2200-2400"]=0
    data_dict["2400-2600"]=0
    data_dict["2600-2800"]=0
    data_dict["2800-3000"]=0
    data_dict[">3000"]=0
    
    for i in indata.values():
        if i <= 500:
            data_dict["0-500"] = data_dict["0-500"] + 1
        elif i > 500 and i <= 800:
            data_dict["500-800"] = data_dict["500-800"] + 1
        elif i > 800 and i <= 1000:
            data_dict["800-1000"] = data_dict["800-1000"] + 1
        elif i > 1000 and i <= 1200:
            data_dict["1000-1200"] = data_dict["1000-1200"] + 1
        elif i > 1200 and i <= 1400:
            data_dict["1200-1400"] = data_dict["1200-1400"] + 1
        elif i > 1400 and i <= 1600:
            data_dict["1400-1600"] = data_dict["1400-1600"] + 1
        elif i > 1600 and i <= 1800:
            data_dict["1600-1800"] = data_dict["1600-1800"] + 1
        elif i > 1800 and i <= 2000:
            data_dict["1800-2000"] = data_dict["1800-2000"] + 1
        elif i > 2000 and i <= 2200:
            data_dict["2000-2200"] = data_dict["2000-2200"] + 1
        elif i > 2200 and i <= 2400:
            data_dict["2200-2400"] = data_dict["2200-2400"] + 1
        elif i > 2400 and i <= 2600:
            data_dict["2400-2600"] = data_dict["2400-2600"] + 1
        elif i > 2600 and i <= 2800:
            data_dict["2600-2800"] = data_dict["2600-2800"] + 1
        elif i > 2800 and i <= 3000:
            data_dict["2800-3000"] = data_dict["2800-3000"] + 1
        else:
            data_dict[">3000"] = data_dict[">3000"] + 1

    
    with open(ofile,'w') as r:
        r.write("distribute" + '\t' + "reads" + '\n')
        for k, v in data_dict.items():
            r.write(k + '\t' + str(v) + '\n')
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="get raeds_distribution",
        epilog="Example: python static_reads_length.py fastq.gz reads_distribution.txt")
    parser.add_argument('ifile', help='input file: fq.gz|fq file')
    parser.add_argument('ofile', help='output file: reads_distribution.txt')
    
    args = parser.parse_args()

    main(args.ifile, args.ofile)
