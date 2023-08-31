import numpy as np
import matplotlib.pyplot as plt
# import math

# # Объявление параметров с расшифровкой
# g = 9.8     # Ускорение свободного падения, м/с2
# m = 6.85    # Масса системы (БПЛА с нагрузкой + каретка), кг
# L = 2       # Длина разгонного участка, м
# b = 2       # Длина нерастянутого эластичного троса, м
# x0 = 4.10   # Длина растянутого эластичного троса, м
# mu = 0.1    # Коэффициент пропорциональности для силы трения скольжения, б/р
# alpha = 15  # Угол установки направляющих к горизонту, градусы
# T = 0       # Сила тяги, Н
# k0 = 40     # Номинальный коэффициент жесткости, кГс/м
# k = 784     # Коэффициент жесткости, Н/м
# n = 0       # Свободный член из выражения определения силы растяжения k(x-b)+n, б/р
# Rx = 0      # Сила лобового сопротивления, Н 
# Ry = 0      # Нормальная сила, Н
     
# Расчет конечного времени, скорости, ускорения в условиях общих допущений и без уточнения характеристик эластичного троса
def time_f (g, m, L, b, x0, mu, alpha, T, k0, k, n, Rx, Ry, t0):
    tf = (np.sqrt(m/k))*(np.arccos((x0 - L - ((m*g/k)*(np.sin(alpha*(np.pi/180)) + (mu*np.cos(alpha*(np.pi/180))))) - b + ((T+n)/k) - (Rx/k) + ((Ry*mu)/k))/(x0 - ((m*g/k)*(np.sin(alpha*(np.pi/180)) + (mu*np.cos(alpha*(np.pi/180))))) - b + ((T+n)/k) - (Rx/k) + ((Ry*mu)/k))))    # Конечное время
    return tf

# Определение функции для подсчета скорости и ускорения в точке
def velocity_acceleration (g, m, L, b, x0, mu, alpha, T, k0, k, n, Rx, Ry, t0, tf):
    v = (x0 - ((m*g)/k)*(np.sin(alpha*(np.pi/180)) + (mu*np.cos(alpha*(np.pi/180)))) - b + ((T+n)/k) - (Rx/k) + ((Ry*mu)/k))*np.sqrt(k/m)*np.sin(tf*np.sqrt(k/m))     # Скорость
    a = (x0 - ((m*g)/k)*(np.sin(alpha*(np.pi/180)) + (mu*np.cos(alpha*(np.pi/180)))) - b + ((T+n)/k) - (Rx/k) + ((Ry*mu)/k))*(k/m)*np.cos(tf*np.sqrt(k/m))     # Ускорение
    return v, a

# Определение функции для перевода строки (str) в список (list)
def str_to_list (line):
    data = []
    for i in range(14):
         data.append(float(line[0:(int(line.find('\t')))]))
         line = line[(int(line.find('\t')))+1:]
    return data

# Определение функции для создания 
def list_of_tva (t0, tf, data):
    time, velocity, acceleration = [], [], []
    for i in range(10):
        t0 = t0 + tf/10
        v, a = velocity_acceleration(*data, t0)
        time.append(round(t0, 2))
        velocity.append(round(v, 2))
        acceleration.append(round(a, 2))
    return time, velocity, acceleration

# Работа с txt файлом исходных данных
f = open('test.txt', 'r')

print('Здравствуй, путник! Перед тобой три пути:\n', 'Первым (1) пойдешь - просто посчитаешь,\n', 'Вторым (2) пойдешь - жгуты настоящие намотаешь,\n', 'Третьим (3) пойдешь - аэродинамику добавишь!\n', 'P.S. Коли всё сразу хочешь - жми на ноль (0), умник!\n')
print('Ответ держи строкой ниже: ')
number = int(input())

t0 = 0              # начальное время, с
time_1, velocity_1, acceleration_1 = [], [], []
time_2, velocity_2, acceleration_2 = [], [], []
time_3, velocity_3, acceleration_3 = [], [], []

if (number == 1) or (number == 2) or (number == 3):
    for i in range(number):
        f.readline()
    line_1 = f.readline()
    data_1 = str_to_list(line_1)
    tf = time_f(*data_1)  # конечное время, с
    time_1, velocity_1, acceleration_1 = list_of_tva(t0, tf, data_1)
elif (number == 0):
    f.readline()
    # Для первой строки файла
    line_1 = f.readline()
    data_1 = str_to_list(line_1)
    tf = time_f(*data_1)  # конечное время, с
    time_1, velocity_1, acceleration_1 = list_of_tva(t0, tf, data_1)
    # Для второй строки файла
    line_2 = f.readline()
    data_2 = str_to_list(line_2)
    tf = time_f(*data_2)  # конечное время, с
    time_2, velocity_2, acceleration_2 = list_of_tva(t0, tf, data_2)
    # Для третьей строки файла
    line_3 = f.readline()
    data_3 = str_to_list(line_3)
    tf = time_f(*data_3)  # конечное время, с
    time_3, velocity_3, acceleration_3 = list_of_tva(t0, tf, data_3)
else:
    print('Умник, куда ты жмал?!')    

# Построение графика
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(time_1, velocity_1, color = 'blue', linewidth = 0.5)
ax1.plot(time_2, velocity_2, color = 'blue', linewidth = 0.5, linestyle = 'dashed')
ax1.plot(time_3, velocity_3, color = 'blue', linewidth = 0.5, linestyle = 'dashdot')
ax2.plot(time_1, acceleration_1, color = 'green', linewidth = 0.5)
ax2.plot(time_2, acceleration_2, color = 'green', linewidth = 0.5, linestyle = 'dashed')
ax2.plot(time_3, acceleration_3, color = 'green', linewidth = 0.5, linestyle = 'dashdot')

ax1.set(xlabel ='Time, sec')
# ax1.set(ylabel ='Velocity, m/sec')
# ax2.set(ylabel ='Acceleration, m/sec2')

ax1.legend(['Velocity, m/sec'], bbox_to_anchor = (0.325, 1.1))
ax2.legend(['Acceleration, m/sec2'], bbox_to_anchor = (1.025, 1.1))

ax1.grid()

fig.savefig("test_plot.png")
plt.show()

f.close()

# # Печать для промежуточной проверки :)
# print(line_1)
# print(line[0:(int(line.find('\t')))])
# print(int(line.find('\t')))

# print(data_1)
# print(data[0])

# print('time         : ', time_1)
# print('velocity     : ', velocity_1)
# print('acceleration : ', acceleration_1)
# print('---')
# print('time         : ', time_2)
# print('velocity     : ', velocity_2)
# print('acceleration : ', acceleration_2)
# print('---')
# print('time         : ', time_3)
# print('velocity     : ', velocity_3)
# print('acceleration : ', acceleration_3)

# print(round((tf), 2))
# print(round((v), 2))
# print(round((a), 2))
