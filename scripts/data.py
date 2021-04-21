#!/usr/bin/env python3
import pandas as pd
import os

data_dir = '/home/ground/projects/tickets-search-system/data'


def pek_kmg():
    in_dir = os.path.join(data_dir, 'pek_kmg')
    out_file = os.path.join(data_dir, 'PEK-KMG.csv')
    files = os.listdir(in_dir)
    for file in files:
        df = pd.read_excel(os.path.join(in_dir, file))
        df['dairport_code'] = file[6:9]
        df['dcity_code'] = 'BJS'
        df['aairport_code'] = file[10:13]
        df['acity_code'] = 'KMG'
        df['ddate'] = file[14:24]
        print(df)
        break
        # df.to_csv(out_file, mode='a', index=False, header=False)


if __name__ == '__main__':
    pek_kmg()
