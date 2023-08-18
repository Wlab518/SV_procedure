import sys

input = sys.argv[1]
output = sys.argv[2]
input_file = open(input, "r")
input_reads = input_file.read()
with open(output, 'w') as o:
    o.write("query_name" + "\t" + "gene_name" + "\t" + "KO_number" + "\t" + "pathway" + '\n')

    for lines in input_reads.split("Query"):
        if "Pathway" in lines:
            for line in lines.split("\n"):
                if line.startswith(":"):
                    query_name = line.split("\t")[1]
                if line.startswith("KO:"):
                    gene_name = line.split("\t")[1]
                if "KEGG" in line:
                    KO_number = str(line.split("\t")[3]).replace("aly", "") 
                    pathway = line.split("\t")[1]
            print(query_name)
            o.write(query_name + "\t" + gene_name + "\t" + KO_number + "\t" + pathway + '\n')

input_file.close()
