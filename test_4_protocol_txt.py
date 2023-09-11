import numpy as np

# Определение функции для перевода строки (str) в список (list)
def str_to_list (line):
    data = []
    for i in range(14):
         data.append(float(line[0:(int(line.find('\t')))]))
         line = line[(int(line.find('\t')))+1:]
    return data

# Определение функции для перевода списка (list) в строку (str)
def list_to_str (data):
    line = str(data[0])
    for i in range(13):
        line = line + ('\t') + f'{float(data[i + 1]):.2f}'
    return line

# Работа с txt файлом исходных данных
d = open('Data.txt', 'r+')
d.readline()

# ukaz = d.tell()
# line_1 = d.readline()
# data_1 = str_to_list(line_1)
# print(data_1)

k0 = 40.00
k = 384.00
n = 238.00

# data_1[8], data_1[9], data_1[10] = f'{k0:.2f}', f'{k0*9.8*2:.2f}', f'{0:.2f}'
# line_1 = list_to_str(data_1)
# print(line_1)
# d.seek(ukaz)
# d.write(line_1)

# for i in range(3):
#     ukaz = d.tell()
#     print(ukaz)
#     line_1 = d.readline()

for i in range(3):
    ukaz = d.tell()
    print(ukaz)
    line_1 = d.readline()
    # print(line_1)
    data_1 = str_to_list(line_1)
    print(i, ': ', data_1)
    if i == 0:
        data_1[8], data_1[9], data_1[10] = f'{k0:.2f}', f'{k0*9.8*2:.2f}', f'{0:.2f}'
    else:
        data_1[8], data_1[9], data_1[10] = f'{k0:.2f}', f'{k:.2f}', f'{n:.2f}'
    line_1 = list_to_str(data_1)
    print('str', line_1)
    print(d.tell())
    d.seek(ukaz)
    d.write(line_1 + '\n')
    # d.write(line_1)
    # d.readline()

d.close()
