import numpy as np
import matplotlib.pyplot as plt

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

# Вывод данных (проверка, запись в файл пока не осуществлена)
num = 2 # n - число жгутов
print(f'{k0:.2f}')
print(f'{k0 * 9.8 * num:.2f}')
print(f'{k * num:.2f}')
print(f'{n * num:.2f}')

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

f.close()