import csv
import os
import argparse
import numpy as np
import collections

def read_ImgList(filepath):
    csv_data = open(filepath)
    reader = csv.reader(csv_data)
    file_data = []
    for row in reader:
        file_data.append(row[0][4:10])
    csv_data.close()

    return file_data

def read_LeafList(dirpath):
    file_list = os.listdir(dirpath)
    print(file_list)

    data_list = []
    for file_name in file_list:
        file_path = f'{dirpath}/{file_name}'
        data = []

        csv_data = open(file_path)
        reader = csv.reader(csv_data)
        for row in reader:
            data.append(row[0:2])
        csv_data.close()

        data_list.append(np.array(data))
    
    return data_list

parser = argparse.ArgumentParser(description='作成した決定木の葉にあるデータと所持している画像の比較')
parser.add_argument('--mode', help='choose disease name mode (Simple or Full)', choices=['Simple','Full'], default='Simple')
parser.add_argument('--depth', help='input tree depth', default=2, type=int)
args = parser.parse_args()

mode = args.mode
depth = args.depth
imgfile_path = './data/Kurume_img_list.csv'
leafdir_path = f'./result/{mode}/unu_depth{depth}/leafs_data'

img_list = read_ImgList(imgfile_path)
leaf_list = read_LeafList(leafdir_path)
# print(leaf_list[3][:,0])

all_img_list = []
img_leaf_list = [ [] for i in range(len(leaf_list)+1)]
for img in img_list:
    flag = True
    for i, leaf in enumerate(leaf_list):
        if img in leaf:
            disease = leaf[leaf[:,0]==img, 1]
            img_leaf_list[i].append([img, disease[0]])
            all_img_list.append([img, disease[0]])
            flag = False
    
    if flag == True:
        img_leaf_list[-1].append([img, 'N/A'])

# print(leaf_list[0][:,0])
# print(img_leaf_list[0])

count_leaf = 0
for i, leaf in enumerate(leaf_list):
    print(f'{i}:{len(leaf)}')
    count_leaf += len(leaf)
print(f'total:{count_leaf}')

count_img = 0
for i, img_leaf in enumerate(img_leaf_list):
    print(f'{i}:{len(img_leaf)}')
    count_img += len(img_leaf)

    img_leaf = np.array(img_leaf)
    count = collections.Counter(img_leaf[:,1])
    count_sort = sorted(count.items(), key=lambda x:x[1], reverse=True)
    print(len(count_sort), count_sort)

print(f'total:{count_img}')

print(len(all_img_list))
all_img_list = np.array(all_img_list)
count = collections.Counter(all_img_list[:,1])
count_sort = sorted(count.items(), key=lambda x:x[1], reverse=True)
print(len(count_sort), count_sort)