import csv
import os
import numpy as np

def pm2unu(s):
    if s == '':
        return 0
    else:
        return 1

def readCSV(data_option, mode, unu_flag=True):
    # 免疫染色のリスト mensen_list
    # 病名のリスト dis_list
    # 症例データ dlist
    # 症例番号と病名番号の対応付け dis_id

    csv_data = open(f'./dataset/{data_option}/Data_{mode}Name.csv')
    reader = csv.reader(csv_data)
    
    for row in reader:
        stain_list = row[2:]
        break

    id_list = []
    dis_list = []
    dis_id_list = []
    unu_list = []
    dataset = []
    for row in reader:
        id_list.extend(row[0])

        if row[1] not in dis_list:
            dis_list.append(row[1])

        idx = dis_list.index(row[1])
        dis_id_list.extend([idx])

        if unu_flag:
            unu = [pm2unu(r) for r in row[2:]]
        else:
            unu = row[2:]
        unu_list.append(unu)

        dataset.append(row)

    csv_data.close()

    return np.array(unu_list), np.array(dis_id_list), np.array(stain_list), np.array(dis_list), np.array(dataset)

def readCSV_svs(data_option, mode, unu_flag=True):
    # 免疫染色のリスト mensen_list
    # 病名のリスト dis_list
    # 症例データ dlist
    # 症例番号と病名番号の対応付け dis_id

    csv_data = open(f'./Raw_data/{data_option}/Kurume_img_list.txt')
    reader = csv.reader(csv_data)
    svs_list = []
    for row in reader:
        svs_list.append(row[0])
    csv_data.close()

    csv_data = open(f'./dataset/{data_option}/Data_{mode}Name.csv')
    reader = csv.reader(csv_data)
    
    for row in reader:
        stain_list = row[2:]
        break
    dis_list = []
    dis_id_list = []
    unu_list = []
    dataset = []
    for row in reader:
        svs_flag = [row[0] for s in svs_list if row[0] in s[:11]]
        if len(svs_flag) > 0:
            if row[1] not in dis_list:
                dis_list.append(row[1])

            idx = dis_list.index(row[1])
            dis_id_list.extend([idx])

            if unu_flag:
                unu = [pm2unu(r) for r in row[2:]]
            else:
                unu = row[2:]
            unu_list.append(unu)

            dataset.append(row)
    csv_data.close()

    return np.array(unu_list), np.array(dis_id_list), np.array(stain_list), np.array(dis_list), np.array(dataset)

def makeCSV2(data, dirpath, filename):
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    csv_file = open(f'{dirpath}/{filename}', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerows(data)

    csv_file.close()

def save_leaf_data(data, dirpath, leaf_id):
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    csv_file = open(f'{dirpath}/leaf_{leaf_id}.csv', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerows(data)
    csv_file.close()