import fileinput
import pandas as pd

amazon_file = fileinput.FileInput('amazon-meta.txt')
nodes=[]
node=[]
edges=[]
num=0

for line in amazon_file:
    print (line)
    num=num+1
    if num == 50:
        break
    line = line.strip().split(':')
    if line[0]=="Id":
        nodes.append(node)
        node=[]
        node.append(line[1].strip())
    if line[0] == 'ASIN':
        ASIN=line[1].strip()
        node.append(line[1].strip())
    if line[0] == 'title':
        node.append(line[1].strip())
    if line[0] == "group":
        node.append(line[1].strip())

    if line[0] == "similar":
        to_list=line[1].strip().split()
        for item in range(1,len(to_list)):
            edges.append([ASIN,to_list[item]])

pd.DataFrame(nodes[2:]).to_csv("nodes.csv",header=["Id","ASIN","Title","Group"],index=False)


