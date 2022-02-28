import csv
import os
import numpy as np

csv_data = open(f'./Raw_data/3rd/Kurume_img_list.txt')
reader = csv.reader(csv_data)
svs_list = []
for row in reader:
    name = row[0][:11].split(']')[0]
    svs_list.append('JMR' + name[-4:])
csv_data.close()

svs_list = sorted(svs_list)
with open('./Raw_data/3rd/Rename_img_list.txt', 'w') as f:
    for svs in svs_list:
        f.write(svs+'\n')