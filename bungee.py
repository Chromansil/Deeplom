import numpy as np
import matplotlib.pyplot as plt

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

# Работа с txt файлом данных о свойствах резинки
f = open('Protocol.txt', 'r')

delta, force = [], []
f.readline()
for i in range(5):
    line = f.readline()
    line = line[(int(line.find('\t')))+1:]
    L = round(float(line[0:int(line.find('\t'))]), 2)
    line = line[(int(line.find('\t')))+1:]
    delta.append(round((float(line[0:int(line.find('\t'))]) - L), 2))
    line = line[(int(line.find('\t')))+1:]
    force.append(float(line[0:(int(line.find('\t')))]))

# Предполагаем, что изменение свойств резинки имеет линейный характер в пределах удлинения от 20 % до 80 %
flag, delta_new, force_new = 0, [0.2*L, 0.8*L], []

for i in range(5):
    if (delta[i] == delta_new[flag]) and (len(force_new) < 2):
        force_new.append((force[i] + force[i+1])/2)
        flag = 1
    elif (delta[i] > delta_new[flag]) and (len(force_new) < 2):
        force_new.append(round(((force[i] * (delta_new[flag] - delta[i - 1])/(delta[i] - delta[i - 1]) + force[i])/2), 2))
        # x = force[i]*(delta_new[flag] - delta[i - 1])/(delta[i] - delta[i - 1])
        flag = 1

k0 = round(((force_new[0]/delta_new[0]) + (force_new[1]/delta_new[1]))/2, -1)
k = round((9.8 * (force_new[1] - force_new[0]))/(delta_new[1] - delta_new[0]))
n = round(9.8 * (force_new[0]) - k * delta_new[0])

# Закрытие txt файла данных о свойствах резинки
f.close()

# Осуществление записи в файл исходных данных для расчета скоростей и ускорений 

# Работа с txt файлом исходных данных
d = open('Data.txt', 'r+')
d.readline()

for i in range(3):
    ukaz = d.tell()
    line_1 = d.readline()
    data_1 = str_to_list(line_1)
    if i == 0:
        data_1[8], data_1[9], data_1[10] = f'{k0:.2f}', f'{k0*9.8*2:.2f}', f'{0:.2f}'
    else:
        data_1[8], data_1[9], data_1[10] = f'{k0:.2f}', f'{k * 2:.2f}', f'{n * 2:.2f}'
    line_1 = list_to_str(data_1)
    d.seek(ukaz)
    d.write(line_1 + '\n')

d.close()

# # Вывод данных (проверка, если запись в файл ещё не осуществлена)
# num = 2 # n - число жгутов
# print(f'{k0:.2f}')
# print(f'{k0 * 9.8 * num:.2f}')
# print(f'{k * num:.2f}')
# print(f'{n * num:.2f}')

# Построение графика
fig, ax = plt.subplots()

ax.plot(delta, force, color = 'blue', linewidth = 1)
ax.plot(delta_new, force_new, color = 'orange', linewidth = 1)
ax.plot([delta_new[0], delta_new[0]], [force[0], force[4]], color = 'grey', linewidth = 1, linestyle = 'dashed')
ax.plot([delta_new[1], delta_new[1]], [force[0], force[4]], color = 'grey', linewidth = 1, linestyle = 'dashed')

ax.legend(['Real cord', 'Approximate cord', '20 %', '80 %'], bbox_to_anchor = (1.025, 1.1), ncols = 4)

ax.set(xlabel = 'Elongation, m', ylabel ='Force, kG')

ax.grid()

fig.savefig("bungee.png")
plt.show()

# # Печать для промежуточной проверки :)
# print(delta_new)
# print(force_new)
