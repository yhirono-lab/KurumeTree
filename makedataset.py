import csv
import collections
import numpy as np
from numpy.core.machar import MachAr

def ReadOriginalCSV(filename, new_flag=False):
    csv_data = open(filename, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_data)
    dataset = []

    for i in range(2):
        next(reader)
    
    for row in reader:
        if not new_flag:
            header = ['No','SimpleName', 'FullName'] + row[62:86]
        else: 
            header = ['No','SimpleName', 'FullName'] + row[65:89]
        break
    
    fix_list = [
        '＋', '(+,focal)', 'ー', '－', '弱', 'weak', 'ごく少数', '極少数', 'ごく', '少数', '一部', 'N/A', '+/-', '±', '?', '　', 
        '赤脾髄に散在性に(+)', 'LEL(+)', '陽性に見えますが挫滅が加わり判定困難です'
    ]
    fixed_list = [
        '+', '+', '-', '-', '', '', '', '', '', '', '', '', '+', '+', '', '', 
        '+', '+', '+'
    ]

    for idx, stain in enumerate(header):
        if stain == 'κ':
            header[idx] = 'kappa'
        if stain == 'λ':
            header[idx] = 'lambda'
    for row in reader:
        if not new_flag:
            stain = row[62:86]
        else:
            stain = row[65:89]
        
        None_flag = False
        for i, stain[i] in enumerate(stain):
            for j in range(len(fix_list)):
                if fix_list[j] in stain[i]:
                    stain[i] = stain[i].replace(fix_list[j], fixed_list[j])
                    
            if stain[i] != '+' and stain[i] != '-' and stain[i] != '':
                if not new_flag:
                    print(row[1], i, stain[i], fix_list[j], stain[i] is not fix_list[j])
                else:
                    print(row[0], i, stain[i], fix_list[j], stain[i] is not fix_list[j])
            
            if stain[i] != '':
                None_flag = True
        
        if None_flag:
            if not new_flag:
                if row[7] is not '':
                    fullname = f'{row[6]}-{row[7]}'
                    dataset.append([row[1], row[6], fullname] + stain)
                else:
                    fullname = row[6]
                    dataset.append([row[1], row[6], fullname] + stain)
            else:
                if row[10] is not '':
                    fullname = f'{row[9]}-{row[10]}'
                    dataset.append([row[0], row[9], fullname] + stain)
                else:
                    fullname = row[9]
                    dataset.append([row[0], row[9], fullname] + stain)
    
    return np.array([header] + dataset)

def MatchSVSlist(data):
    svs_list =  np.loadtxt(f'./{dir_list[add_option]}/Kurume_img_list.txt', dtype='str', delimiter=',')
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

def Add_Diseasae(dataset, file_label):
    if file_label == 'SimpleName':
       dataset = np.delete(dataset, 2, axis=1)
    if file_label == 'FullName':
        dataset = np.delete(dataset, 1, axis=1)
    
    name_list = dataset[1:,1]
    count = collections.Counter(name_list)
    count_sort = sorted(count.items(), key=lambda x:x[1], reverse=True)
    return dataset, count_sort


add_option = 0
dir_list = ['data', 'add_data']
flag = [False, True]
dataset_list = ['ML180001_180660.csv', 'ML180001_182700.csv']

dataset = ReadOriginalCSV(f'./{dir_list[add_option]}/{dataset_list[add_option]}', new_flag=flag[add_option])
WriteSingleCSV(dataset[0][3:], f'{dir_list[add_option]}/Stain_list.csv')

dataset_simple, count_sort = Add_Diseasae(dataset, 'SimpleName')
WriteMultiCSV(dataset_simple, f'{dir_list[add_option]}/Data_SimpleName.csv')
WriteDicCSV(count_sort, f'{dir_list[add_option]}/Disease_SimpleName_list.csv')

dataset_full, count_sort = Add_Diseasae(dataset, 'FullName')
WriteMultiCSV(dataset_full, f'{dir_list[add_option]}/Data_FullName.csv')
WriteDicCSV(count_sort, f'{dir_list[add_option]}/Disease_FullName_list.csv')

dataset_svs = MatchSVSlist(dataset)

dataset_svs_simple, count_sort = Add_Diseasae(dataset_svs, 'SimpleName')
WriteMultiCSV(dataset_svs_simple, f'{dir_list[add_option]}/Data_SimpleName_svs.csv')
WriteDicCSV(count_sort, f'{dir_list[add_option]}/Disease_SimpleName_svs_list.csv')

dataset_svs_full, count_sort = Add_Diseasae(dataset_svs, 'FullName')
WriteMultiCSV(dataset_svs_full, f'{dir_list[add_option]}/Data_FullName_svs.csv')
WriteDicCSV(count_sort, f'{dir_list[add_option]}/Disease_FullName_svs_list.csv')


