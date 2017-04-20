import fileinput
import numpy as np
import pandas as pd
import re
import os
#os.chdir('/Users/angela/Desktop/columbia_life/datavisualization/project')
amazon = fileinput.FileInput('amazon-meta.txt')


#f = open('myfile','w')
#f.write('hi there\n')
amazon = fileinput.FileInput('amazon-meta.txt')
f = open('id_overall.txt','w')

cur_id=''
i=1
cur=0

for line in amazon:
    line = line.strip()
    if line.startswith('Id:'):
        s=4-cur
        if s!=0:
            for i in range(s):
                f.write(''+'\t')
        cur_id=re.search('(?<=Id)[^\d]*(\d+)[. ]*', line).groups()[0]
        f.write('\n')
        f.write(cur_id+'\t')
        cur=1
        continue
    #if line.startswith("ASIN:"):
       # s=1-cur
        #if s!=0:
            #for i in range(s):
                #f.write(''+'\t')
        #ASIN=re.search('(?<=ASIN)[^\d]*(\d+)[. ]*', line).groups()[0]
        #f.write(ASIN+'\t')
        #cur=3
        #continue

    #if line.startswith('title:'):
        #s=2-cur
        #if s!=0:
            #for i in range(s):
                #f.write(''+'\t')
        #title=re.search('(?<=title: )[ ]*(.*)', line).groups()[0] 
        #title=title.replace('\t', " ")
        #f.write(title+'\t')
        #cur=3
        #continue
        
    if line.startswith('group:'):
        s=1-cur
        if s!=0:
            for i in range(s):
                f.write(''+'\t')                        
        group=re.search('(?<=group: )[ ]*(.*)', line).groups()[0]
        f.write(group+'\t')
        cur=2
        continue

    if line.startswith('salesrank:'):
        s=2-cur
        if s!=0:
            for i in range(s):
                f.write(''+'\t') 
        salesrank=re.search('(?<=salesrank: )[ ]*(.*)', line).groups()[0]
        f.write(salesrank+'\t')
        cur=3
        continue

    #if line.startswith('similar:'):
        #s=5-cur
        #if s!=0:
            #for i in range(s):
                #f.write(''+'\t') 
        #similar=re.search('(?<=similar: )[ ]*(\d+)[. ]*', line).groups()[0]
        #f.write(similar+'\t')
        #cur=6
        #continue

    #if line.startswith('categories:'):
        #s=6-cur
        #if s!=0:
            #for i in range(s):
                #f.write(''+'\t') 
        #categories=re.search('(?<=categories: )[ ]*(.*)', line).groups()[0]
        #f.write(categories+'\t') 
        #cur=7
        #continue

    if 'reviews:' in line:
        s=3-cur
        if s!=0:
            for i in range(s):
                f.write(''+'\t') 
        #total=re.search('(?<=total)[^\d]*(\d+)[. ]*(?=downloaded)', line)
        #downloaded=re.search('(?<=downloaded)[^\d]*(\d+)[. ]*(?=avg rating)', line) 
        rating=re.search('(?<=rating)[^\d]*([\d|.]+)[. ]*', line)
        #if bool(total):
            #f.write(total.groups()[0]+'\t')
        #else:
            #f.write(''+'\t')
        #if bool(downloaded):
            #f.write(downloaded.groups()[0]+'\t')
        #else:
            #f.write(''+'\t')
        if bool(rating):
            f.write(rating.groups()[0]+'\t')
        else:
            f.write(''+'\t')
        cur=4
    

#f.write('\n')
f.close()       

lines = []

with open('id_overall.txt', 'r') as f:
    lines = f.readlines()
with open('id_overall.txt', 'w') as f:
    f.writelines(lines[1:])

with open("id_overall.txt", "r+") as f: s = f.read(); f.seek(0); f.write('Id\tgroup\tsalesrank\trating\t\n' + s)


