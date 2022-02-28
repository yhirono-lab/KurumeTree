import csv
import collections
import numpy as np
from numpy.core.machar import MachAr
from pathlib import Path

def ReadOriginalCSV(filename, data_option):
    csv_data = open(filename, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_data)
    dataset = []

    for i in range(2):
        next(reader)
    
    for row in reader:
        if data_option == '1st':
            header = ['No','SimpleName', 'FullName'] + row[62:86]
        elif data_option == '2nd': 
            header = ['No','SimpleName', 'FullName'] + row[65:89]
        elif data_option == '3rd':
            header = ['No','SimpleName', 'FullName'] + row[62:86]
        break
    
    fix_list = [
        '＋', '(+,focal)', 'ー', '－', '弱', 'weak', 'ごく少数', '極少数', 'ごく', '少数', '一部',
        'N/A', '+/-', '-/+', '±', '?', '　', 
        '赤脾髄に散在性に(+)', 'LEL(+)', '陽性に見えますが挫滅が加わり判定困難です'
    ]
    fixed_list = [
        '+', '+', '-', '-', '', '', '', '', '', '', '',
        '', '+', '-', '+', '', '', 
        '+', '+', '+'
    ]

    for idx, stain in enumerate(header):
        if stain == 'κ':
            header[idx] = 'kappa'
        if stain == 'λ':
            header[idx] = 'lambda'
    for row in reader:
        if data_option == '1st':
            stain = row[62:86]
        elif data_option == '2nd':
            stain = row[65:89]
        elif data_option == '3rd':
            stain = row[62:86]
        
        None_flag = False
        for i, stain[i] in enumerate(stain):
            for j in range(len(fix_list)):
                if fix_list[j] in stain[i]:
                    stain[i] = stain[i].replace(fix_list[j], fixed_list[j])
                    
            if stain[i] != '+' and stain[i] != '-' and stain[i] != '':
                if data_option == '1st':
                    print(row[1], i, stain[i], fix_list[j], stain[i] is not fix_list[j])
                elif data_option == '2nd':
                    print(row[0], i, stain[i], fix_list[j], stain[i] is not fix_list[j])
                elif data_option == '3rd':
                    print(row[62:86], i, stain[i], fix_list[j], stain[i] is not fix_list[j])
            
            if stain[i] != '':
                None_flag = True
        
        if None_flag:
            if data_option == '1st':
                if row[7] is not '':
                    fullname = f'{row[6]}-{row[7]}'
                    dataset.append([row[1], row[6], fullname] + stain)
                else:
                    fullname = row[6]
                    dataset.append([row[1], row[6], fullname] + stain)
            elif data_option == '2nd':
                if row[10] is not '':
                    fullname = f'{row[9]}-{row[10]}'
                    dataset.append([row[0], row[9], fullname] + stain)
                else:
                    fullname = row[9]
                    dataset.append([row[0], row[9], fullname] + stain)
            elif data_option == '3rd':
                if row[7] is not '':
                    fullname = f'{row[6]}-{row[7]}'
                    dataset.append([row[1], row[6], fullname] + stain)
                else:
                    fullname = row[6]
                    dataset.append([row[1], row[6], fullname] + stain)
    
    return np.array([header] + dataset)

def MatchSVSlist(data, data_option):
    svs_list =  np.loadtxt(f'./Raw_data/{data_option}/Kurume_img_list.txt', dtype='str', delimiter=',')
    data_svs = [data[0]]
    for d in data[1:]:
        d_svs = [d for svs in svs_list if d[0] in svs[:11]]
        if len(d_svs)>0:
            data_svs.append(d_svs[0])
    data_svs = np.array(data_svs)

    return data_svs

def WriteMultiCSV(data, filename):
    csv_file = open(filename, 'w', newline='')
    writer = csv.writer(csv_file)
    for d in data:
        try:
            writer.writerow(d)
        except:
            print(d)
    csv_file.close()

def WriteSingleCSV(data, filename):
    csv_file = open(filename, 'w', newline='')
    writer = csv.writer(csv_file)
    for d in data:
        writer.writerow([d])
    csv_file.close()

def WriteDicCSV(data, filename):
    csv_file = open(filename, 'w', newline='')
    writer = csv.writer(csv_file)
    for d in data:
        writer.writerow(list(d))
    csv_file.close()

# SimpleNameなのかFullNameなのかを選ぶ
# 各病型のカウントも行う
def Add_Diseasae(dataset, file_label):
    if file_label == 'SimpleName':
        dataset = np.delete(dataset, 2, axis=1)
    if file_label == 'FullName':
        dataset = np.delete(dataset, 1, axis=1)
    
    name_list = dataset[1:,1]
    count = collections.Counter(name_list)
    count_sort = sorted(count.items(), key=lambda x:x[1], reverse=True)
    return dataset, count_sort


data_option = 2
dir_list = ['1st', '2nd', '3rd']
dataset_list = ['ML180001_180660.csv', 'ML180001_182700.csv', 'O_C_00001-02530.csv']
data_dir = dir_list[data_option]
Raw_data = dataset_list[data_option]
save_dir = Path(f'./dataset/{data_dir}')
save_dir.mkdir(exist_ok=True, parents=True)

dataset = ReadOriginalCSV(f'./Raw_data/{data_dir}/{Raw_data}', data_option=data_dir)
WriteSingleCSV(dataset[0][3:], f'./dataset/{data_dir}/Stain_list.csv')


dataset_simple, count_sort = Add_Diseasae(dataset, 'SimpleName')
WriteMultiCSV(dataset_simple, f'./dataset/{data_dir}/Data_SimpleName.csv')
WriteDicCSV(count_sort, f'./dataset/{data_dir}/Disease_SimpleName_list.csv')

dataset_full, count_sort = Add_Diseasae(dataset, 'FullName')
WriteMultiCSV(dataset_full, f'./dataset/{data_dir}/Data_FullName.csv')
WriteDicCSV(count_sort, f'./dataset/{data_dir}/Disease_FullName_list.csv')

"""持っているsvsファイルのデータのみ抽出して保存"""
dataset_svs = MatchSVSlist(dataset, data_dir)

dataset_svs_simple, count_sort = Add_Diseasae(dataset_svs, 'SimpleName')
WriteMultiCSV(dataset_svs_simple, f'./dataset/{data_dir}/Data_SimpleName_svs.csv')
WriteDicCSV(count_sort, f'./dataset/{data_dir}/Disease_SimpleName_svs_list.csv')

dataset_svs_full, count_sort = Add_Diseasae(dataset_svs, 'FullName')
WriteMultiCSV(dataset_svs_full, f'./dataset/{data_dir}/Data_FullName_svs.csv')
WriteDicCSV(count_sort, f'./dataset/{data_dir}/Disease_FullName_svs_list.csv')


