import csv
import collections
import numpy as np

def ReadOriginalCSV(filename):
    csv_data = open(filename, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_data)
    dataset = []

    for i in range(2):
        next(reader)
    
    for row in reader:
        header = ['No','SimpleName', 'FullName'] + row[62:86]
        break
    
    fix_list = ['＋', '(+,focal)', 'ー', '－', '弱', 'weak', 'ごく少数', '極少数', '少数', '一部', 'N/A', '　']
    fixed_list = ['+', '+', '-', '-', '', '', '', '', '', '', '', '']

    for idx, stain in enumerate(header):
        if stain == 'κ':
            header[idx] = 'kappa'
        if stain == 'λ':
            header[idx] = 'lambda'
    for row in reader:
        stain = row[62:86]
        for i,stain[i] in enumerate(stain):
            for j in range(len(fix_list)):
                if fix_list[j] in stain[i]:
                    stain[i] =stain[i].replace(fix_list[j], fixed_list[j])
                    
            if stain[i] != '+' and stain[i] != '-' and stain[i] != '':
                print(row[1], i, stain[i], fix_list[j], stain[i] is not fix_list[j])

        if row[7] is not '':
            fullname = f'{row[6]}-{row[7]}'
            dataset.append([row[1], row[6], fullname] + stain)
        else:
            fullname = row[6]
            dataset.append([row[1], row[6], fullname] + stain)
    
    return np.array([header] + dataset)


def WriteMultiCSV(data, filename):
    csv_file = open(filename, 'w', newline='')
    writer = csv.writer(csv_file)
    for d in data:
        writer.writerow(d)
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
    count_simple = collections.Counter(name_list)
    count_sort = sorted(count_simple.items(), key=lambda x:x[1], reverse=True)
    # WriteDicCSV(count_sort, f'data/Disease_{file_label}_list.csv')
    return dataset

    

dataset = ReadOriginalCSV('data/ML180001-180660 _to_NIT.csv')
# WriteSingleCSV(dataset[0][3:], 'data/Stain_list.csv')

dataset_simple = Add_Diseasae(dataset, 'SimpleName')
# WriteMultiCSV(dataset_simple, 'data/Data_SimpleName.csv')

dataset_full = Add_Diseasae(dataset, 'FullName')
# WriteMultiCSV(dataset_full, 'data/Data_FullName.csv')
