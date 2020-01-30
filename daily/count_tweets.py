import pandas as pd
import os


folders = ['VLDset1', 'VLDset2', 'VLDset3']

grand_total = 0
for folder in folders:
    filenames = os.listdir(folder)
    total_count = 0
    for filename in filenames:
        data = pd.read_csv(os.path.join(folder, filename))
        total_count += len(data)
    print total_count
    grand_total += total_count
print grand_total
