import csv

filename = '../hori_check/img_data/img_data.csv'
# 打开文件
with open(filename,'w') as f:
    writer = csv.writer(f)
    data = ('Machine_num','time','x','y','x1','y1')
    writer.writerow(data)

print('s')