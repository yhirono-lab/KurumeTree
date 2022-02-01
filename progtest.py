import os

SVS_DIR = '/Raw/Kurume_Dataset/svs'

svs_list = os.listdir(SVS_DIR)

for svs in svs_list:
    old_name = svs
    if 'ML18' in svs:
        new_name = svs.replace('ML18', 'ML_18')
        os.rename(f'{SVS_DIR}/{old_name}', f'{SVS_DIR}/{new_name}')
        print(old_name)