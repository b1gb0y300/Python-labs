import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import pi, cos, sin

class Canvas(FigureCanvasTkAgg):
    def __init__(self, figure=None, master=None):
        super().__init__(figure=figure, master=master)
        self.canvas = self.get_tk_widget()
        self.canvas.pack(side='top', fill='both', expand=1)

def cm_to_inch(value):
    return value / 2.54

def M1(dy, dt, p1, i, j, u):
    if u >= 0:
        return dy * dt * p1[i][j] * u
    else:
        return dy * dt * p1[i + 1][j] * u

def M2(dy, dt, p1, i, j, u):
    if u < 0:
        return dy * dt * p1[i][j] * u
    else:
        return dy * dt * p1[i - 1][j] * u

def M3(dx, dt, p1, i, j, v):
    if v >= 0:
        return dx * dt * p1[i][j] * v
    else:
        return dx * dt * p1[i][j + 1] * v

def M4(dx, dt, p1, i, j, v):
    if v < 0:
        return dx * dt * p1[i][j] * v
    else:
        return dx * dt * p1[i][j - 1] * v

def Q(i, j, x1, y1, initial_concentration):
    return initial_concentration if (i == x1 and j == y1) else 0

def check_courant_condition(dx, dy, D, u, v, dt):
    K = 0.5 

    dt_courant_x = (dx ** 2) / (2 * D) + dx / abs(u) if u != 0 else (dx ** 2) / (2 * D)
    dt_courant_y = (dy ** 2) / (2 * D) + dy / abs(v) if v != 0 else (dy ** 2) / (2 * D)
    dt_courant = K * min(dt_courant_x, dt_courant_y)

    print(f"dt: {dt}, dt_courant: {dt_courant}")

    if dt >= dt_courant:
        layout = [
            [sg.Text(f"Шаг времени ({dt:.4f}) превышает допустимое значение ({dt_courant:.4f}).")],
            [sg.Text("Введите новый шаг времени:"), sg.Input(dt_courant, key='-NEW_DT-', size=(10, 1))],
            [sg.Button('Применить'), sg.Button('Отмена')]
        ]
        window = sg.Window('Ошибка условия Куранта', layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Отмена'):
                window.close()
                return False
            elif event == 'Применить':
                try:
                    new_dt = float(values['-NEW_DT-'])
                    if new_dt <= dt_courant:
                        dt = new_dt
                        window.close()
                        return dt 
                    else:
                        sg.popup_error(f"Шаг времени должен быть меньше или равен {dt_courant:.4f}.")
                except ValueError:
                    sg.popup_error("Некорректное значение. Пожалуйста, введите число.")
        return False
    return dt

def calculate_concentration(max_layer, x1, y1, wind_speed, wind_air_angle, initial_concentration):
    dx, dy, dt = 200, 200, 5  
    D, alpha = 10, 0.05       
    N_points = 80            

    wind_air_angle_rad = wind_air_angle * pi / 180
    u = wind_speed * cos(wind_air_angle_rad)
    v = wind_speed * sin(wind_air_angle_rad)

    dt = check_courant_condition(dx, dy, D, u, v, dt)
    if not dt:
        return [] 

    p1 = np.zeros((N_points, N_points))
    p2 = np.zeros((N_points, N_points))
    results = []

    for n in range(1, max_layer + 1):
        for i in range(1, N_points - 1):
            for j in range(1, N_points - 1):
               
                m1 = M1(dy, dt, p1, i, j, u)
                m2 = M2(dy, dt, p1, i, j, u)
                m3 = M3(dx, dt, p1, i, j, v)
                m4 = M4(dx, dt, p1, i, j, v)

                diff_x2 = (dt / (dx ** 2)) * D * ((p1[i + 1][j] - p1[i][j]) - (p1[i][j] - p1[i - 1][j]))
                diff_y2 = (dt / (dy ** 2)) * D * ((p1[i][j + 1] - p1[i][j]) - (p1[i][j] - p1[i][j - 1]))
                p2[i][j] = (p1[i][j] - (1.0 / (dx * dy)) * (m1 - m2 + m3 - m4) +
                            diff_x2 + diff_y2 + dt * (Q(i, j, x1, y1, initial_concentration) - alpha * p1[i][j]))

        p1 = p2.copy()
        results.append(p1.copy())

    return results

def update_plot(ax, canvas, concentration, x1, y1, zoom=2000):
    ax.clear()
    x = np.linspace(0, (80 - 1) * 200, 80)  # Ось X
    y = np.linspace(0, (80 - 1) * 200, 80)  # Ось Y
    X, Y = np.meshgrid(x, y)

    c = ax.contour(X, Y, concentration, 8, colors='black', linewidths=0.5)
    cf = ax.contourf(X, Y, concentration, 8, cmap='Pastel1')
    ax.clabel(c, inline=1, fontsize=10)
    ax.set_xlabel('X (м)')
    ax.set_ylabel('Y (м)')

    ax.set_xlim(max(0, x1 * 200 - zoom), min((80 - 1) * 200, x1 * 200 + zoom))
    ax.set_ylim(max(0, y1 * 200 - zoom), min((80 - 1) * 200, y1 * 200 + zoom))
    concentration_value = concentration[x1, y1] if x1 < concentration.shape[0] and y1 < concentration.shape[1] else 0
    window['-CONCENTRATION-'].update(f'Концентрация: {concentration_value:.2f}')
   
    canvas.figure.colorbar(cf, ax=ax, label=f'Концентрация ({len(canvas.figure.axes)})')
    canvas.draw()



layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [sg.Text('Временной слой:'), sg.Input(10, key='-LAYER-', size=(10, 1)),
     sg.Text('X1:'), sg.Input(40, key='-X1-', size=(10, 1)),
     sg.Text('Y1:'), sg.Input(40, key='-Y1-', size=(10, 1))],
    [sg.Text('Скорость ветра:'), sg.Input(25, key='-WIND-', size=(10, 1)),
     sg.Text('Угол ветра:'), sg.Input(90, key='-ANGLE-', size=(10, 1)),
     sg.Text('Начальная концентрация:'), sg.Input(1.0, key='-CONC-', size=(10, 1))],
     [sg.Text('', size=(30, 1), key='-CONCENTRATION-')],
    [sg.Push(), sg.Button('Рассчитать'), sg.Push()]
]

window = sg.Window('Модель концентрации', layout, finalize=True, resizable=True)
fig = Figure(figsize=(cm_to_inch(18), cm_to_inch(14)))
ax = fig.add_subplot()
canvas = Canvas(fig, window['Canvas'].Widget)

concentration_data = None  
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Рассчитать':
        layer = int(values['-LAYER-'])
        x1, y1 = int(values['-X1-']), int(values['-Y1-'])
        wind_speed = float(values['-WIND-'])
        angle = float(values['-ANGLE-'])
        initial_concentration = float(values['-CONC-'])

        layers = calculate_concentration(layer, x1, y1, wind_speed, angle, initial_concentration)
        if layers: 
            concentration_data = layers[-1]  

            update_plot(ax, canvas, concentration_data, x1, y1)

window.close()