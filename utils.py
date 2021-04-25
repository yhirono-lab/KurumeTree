import csv
import os
import numpy as np

def pm2unu(s):
    if s == '':
        return 0
    else:
        return 1

def readCSV(dirpath, mode):
    # 免疫染色のリスト mensen_list
    # 病名のリスト dis_list
    # 症例データ dlist
    # 症例番号と病名番号の対応付け dis_id

    csv_data = open(f'{dirpath}/Data_{mode}Name.csv')
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

        unu = [pm2unu(r) for r in row[2:]]
        unu_list.append(unu)

        dataset.append(row)

    csv_data.close()

    return np.array(unu_list), np.array(dis_id_list), np.array(stain_list), np.array(dis_list), np.array(dataset)

def makeCSV2(data, dirname, filename):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    csv_file = open(f'{dirname}/{filename}', 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerows(data)

    csv_file.close()