import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math
import matplotlib as mt
import numpy as np

a = 2.5 #левая точка
b = 5 #правая точка
d = 120 #число точек
h = ( b - a )/( d ) #ШАГ



class Canvas(FigureCanvasTkAgg):

  def __init__(self, figure=None, master=None):
    super().__init__(figure=figure, master=master)
    self.canvas = self.get_tk_widget()
    self.canvas.pack(side='top', fill='both', expand=1)

def cm_to_inch(value):
  return value / 2.54

def my_function(x):
    return ((2*x**2 + 3)*(np.sqrt(x**2 - 3))) / (9*x**3)

def numerical_derivative(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)
def numerical_derivative_right(f, x, h):
    return f(x + h) - f(x)
def numerical_derivative_left(f, x, h):
    return f(x) - f(x- h)
def analytical1(x):
    numerator = x**3 * (4*x*np.sqrt(x**2 - 3) + (x*(2*x**2 + 3))/(np.sqrt(x**2 - 3))) - 3*x**2*np.sqrt(x**2 - 3)*(2*x**2 + 3)
    denominator = 9*x**6
    return numerator / denominator

def analytical2(x):
    numerator = (x**6 * (-3*(x**2*(4*x*np.sqrt(x**2-3) + (x*(2*x**2+3))/(np.sqrt(x**2-3))) + 2*x*np.sqrt(x**2-3)*(2*x**2+3)) +
                  x**3*(4*(np.sqrt(x**2-3) + (x**2)/(np.sqrt(x**2-3))) + (6*x**2+3)/(np.sqrt(x**2-3)) - (x**2*(2*x**2+3))/(((x**2-3))**(3/2)))+
                  3*x**2*(4*x*np.sqrt(x**2-3) + (x*(2*x**2+3))/(np.sqrt(x**2-3)))) -
                 6*x**5*(x**3*(4*x*np.sqrt(x**2-3) + (x*(2*x**2+3))/(np.sqrt(x**2-3))) - 3*x**2*np.sqrt(x**2-3)*(2*x**2+3)))
    denominator = 9*x**12
    return numerator / denominator


def analytical3(x):
    numerator = ((-12 * x ** 9) * np.sqrt(x ** 2 - 3) - 6 * x ** 9 * (2 * x ** 2 + 3) * np.sqrt(x ** 2 - 3) + (4 * x ** 8) * ((3 * x ** 2 - 2) / (np.sqrt(x ** 2 - 3)) - (2 * x ** 10 - 2 * x ** 8) / ((x ** 2 - 3) ** 1.5)) - (36 * x ** 7) * (2 * x ** 2 + 3) * np.sqrt(x ** 2 - 3) + (48 * x ** 6) * np.sqrt(x ** 2 - 3))*(-1)
    denominator = 9 * x ** 12
    return numerator / denominator

def numerical_second_derivative(f, x, h):
    return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)

def numerical_third_derivative(f, x, h):
    return (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h)) / (2 * h**3)

layout = [
    [sg.Canvas(size=(600, 480), key='Canvas', background_color='white')],
    [sg.Text('D', size=(6, 1),background_color='white', text_color='black')],
    [sg.Input(100, enable_events=True, k='-D-', size=(7, 1))],
    [[sg.Push(), sg.Button('ESHKIN KOT', button_color=('black', 'white')), sg.Push()]]
]

window = sg.Window('ЧД',
                   layout,
                   finalize=True,
                   resizable=True,
                    background_color='white')
#, size = (640, 520)

fig = Figure(figsize=(cm_to_inch(20), cm_to_inch(16))) # Измените размеры по вашему усмотрению
fig.subplots_adjust(wspace=0.5, hspace=0.5)  # Регулирует расстояние между графиками по горизонтали и вертикали
ax_1 = fig.add_subplot(2, 2, 1)
ax_2 = fig.add_subplot(2, 2, 2)
ax_3 = fig.add_subplot(2, 2, 3)
ax_4 = fig.add_subplot(2, 2, 4)

canvas = Canvas(fig, window['Canvas'].Widget)
def plot_figure(a,b,d,h):
    h = (b - a) / (d )
    ax_1.cla() #переделывает
    ax_2.cla()
    ax_3.cla()
    x_values = np.linspace(a, b, d)

    right = numerical_derivative_right(my_function,x_values, h)
    left = numerical_derivative_left(my_function, x_values, h)
    first_derivative_values = numerical_derivative(my_function, x_values, h) #значения функций -  производных
    second_derivative_values = numerical_second_derivative(my_function, x_values, h)
    third_derivative_values = numerical_third_derivative(my_function, x_values, h)

    analyt = analytical1(x_values)
    analyt2 = analytical2(x_values)
    anatyt3 = analytical3(x_values)

    plt.figure(figsize=(12, 6))

    ax_2.plot(x_values, first_derivative_values, label='Численно', color='green')
    ax_1.plot(x_values, right, label='Численно прав', color='red')
    ax_1.plot(x_values, analyt, label='Аналитически', color='green', linestyle='--')
    ax_1.plot(x_values, left, label='Численно лев', color='pink',linestyle='--')
    ax_2.plot(x_values, analyt, label='Аналитически', color='red', linestyle='--')
    ax_3.plot(x_values, second_derivative_values, label='Численно', color='blue')
    ax_3.plot(x_values, analyt2, label='Аналитически', color='red', linestyle='--')
    ax_4.plot(x_values, third_derivative_values, label='Численно', color='orange')
    ax_4.plot(x_values, anatyt3, label='Аналитически', color='red', linestyle='--')

    ax_1.set_title('Функция')
    ax_1.legend()
    ax_1.grid(True)  # Добавляет сетку на график

    ax_2.set_title('I')
    ax_2.legend()
    ax_2.grid(True)  # Добавляет сетку на график

    ax_3.set_title('II')
    ax_3.legend()
    ax_3.grid(True)  # Добавляет сетку на график


    ax_4.set_title('III')
    ax_4.legend()
    ax_4.grid(True)  # Добавляет сетку на график
    # plt.tight_layout()
    canvas.draw()

def launch():
    plot_figure(a,b,d,h)

while True:
  event, values = window.read()
  # print(event)
  if event in (sg.WIN_CLOSED, 'Exit'):
    break
  elif event == '-A-':
      a = float(values[event])
  elif event == '-B-':
      b = float(values[event])
  elif event == '-D-':
      d = float(values[event])
  elif event == '-H-':
      h = float(values[event])
  elif event == 'ESHKIN KOT':
      launch()