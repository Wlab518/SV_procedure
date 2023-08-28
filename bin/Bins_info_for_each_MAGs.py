import os
import argparse
from subprocess import call
from urllib.request import urlopen
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
 
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams

path = os.getcwd()

def main(clustfile, genefile):
    cluster_dict = {}
    k = 0
    fp=open(clustfile,"rb")
    parser=PDFParser(fp)
    doc=PDFDocument(parser)
    parser.set_document(doc)
    #doc.set_parser(parser)
    #doc.initialize("")
    resource=PDFResourceManager()
    laparam=LAParams()
    device=PDFPageAggregator(resource,laparams=laparam)
    interpreter=PDFPageInterpreter(resource,device)
    #for page in doc.get_pages():
    #for page in PDFPage.get_pages(doc):
    for page in PDFPage.create_pages(doc):
        k += 1
        interpreter.process_page(page)
        layout=device.get_result()
        for out in layout:
            if hasattr(out, 'get_text'):  
                if '.fa' in out.get_text():
                    cluster_dict.setdefault("MAG" + str(k), []).append(out.get_text().replace('\n', ''))

    with open(genefile,'r') as g:
        genome_info = [line.strip().split(',') for line in g.readlines()]

    call('mkdir -p {0}/MAGs/'.format(path), shell=True)
    for key, val in cluster_dict.items():
        with open('{0}/MAGs/{1}.txt'.format(path, key),'w') as r:
            r.write("genome" + '\t' + "completeness" + '\t' + "contamination" + '\t' + "length" + '\t' + "N50" + '\n')
            for line in genome_info[1:]:
                for fa in val:
                    if line[0] in fa:
                        r.write(fa + '\t' + line[1] + '\t' + line[2] + '\t' + line[4] + '\t' + line[5] + '\n')
                        continue


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="run procedure",
        epilog="Example: python Bins_info_for_each_MAGs.py Cluster_scoring.pdf genomeInformation.csv")
    parser.add_argument('clustfile', help='Cluster_scoring.pdf')
    parser.add_argument('genefile', help='genomeInformation.csv')
    args = parser.parse_args()

    main(args.clustfile, args.genefile)
