import csv
import os
import numpy as np

data = np.loadtxt(f'./data/Data_SimpleName_svs.csv', dtype='str', delimiter=',')
add_data = np.loadtxt(f'./add_data/Data_SimpleName_svs.csv', dtype='str', delimiter=',')

data = data[1:,0].astype('uint32')
add_data = add_data[1:,0].astype('uint32')

flag = []
for d in add_data:
    if d in data:
        flag.append([d, 0])
    else:
        flag.append([d, 1])
flag = np.array(flag)
np.savetxt('./add_data/add_flag_list.csv', flag, delimiter=',', fmt='%d')
