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
    line = ''
    for i in range(14):
        line = line + f'{float(data[i]):.2f}' + ('\t')
    return line

# Работа с txt файлом исходных данных
d = open('Data.txt', 'r+')
d.readline()
ukaz = d.tell()
line_1 = d.readline()
data_1 = str_to_list(line_1)

k0 = 40.00
k = 192.00
n = 238.00

data_1[8], data_1[9], data_1[10] = f'{k0:.2f}', f'{k0*9.8*2:.2f}', f'{0:.2f}'
line_1 = list_to_str(data_1)
d.seek(ukaz)
d.write(line_1)

d.close()
