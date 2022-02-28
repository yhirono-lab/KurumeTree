import csv
import os
import numpy as np

data = np.loadtxt(f'./dataset/1st/Data_SimpleName_svs.csv', dtype='str', delimiter=',')
add_data = np.loadtxt(f'./dataset/2nd/Data_SimpleName_svs.csv', dtype='str', delimiter=',')

data = data[1:,0].astype('uint32')
add_data = add_data[1:,0].astype('uint32')

flag = []
for d in add_data:
    if d in data:
        flag.append([d, 0])
    else:
        flag.append([d, 1])
flag = np.array(flag)
np.savetxt('./dataset/2nd/add_flag_list.csv', flag, delimiter=',', fmt='%d')

data = np.loadtxt(f'./dataset/1st/Data_SimpleName_svs.csv', dtype='str', delimiter=',')
add_data = np.loadtxt(f'./dataset/3rd/Data_SimpleName_svs.csv', dtype='str', delimiter=',')

data = [int(d[-4:]) for d in data[1:,0]]
add_data = [d for d in add_data[1:,0]]

flag = []
for d in add_data:
    if int(d[-4:]) in data:
        flag.append([d, 0])
    else:
        flag.append([d, 1])
flag = np.array(flag)
np.savetxt('./dataset/3rd/add_flag_list.csv', flag, delimiter=',', fmt='%s')