import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math
import matplotlib as mt
import numpy as np
from matplotlib.patches import Circle
a = 1
b = 2
d = 100
eps = 0.01


class Canvas(FigureCanvasTkAgg):
  """
    Create a canvas for matplotlib pyplot under tkinter/PySimpleGUI canvas
    """

  def __init__(self, figure=None, master=None):
    super().__init__(figure=figure, master=master)
    self.canvas = self.get_tk_widget()
    self.canvas.pack(side='top', fill='both', expand=1)

def cm_to_inch(value):
  return value / 2.54

def f(x):
   return x**4+2.83*x**3-4.5*x**2-20

def f_d(x) :
    return 4*x**3+((849*x**2)/(100))-9*x
print(f_d(0))

layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [sg.Text('A'), sg.Input(2,enable_events=True,k='-A-',size=(9, 1)),
    sg.Text('B'), sg.Input(7,enable_events=True,k='-B-',size=(7, 1)),
    sg.Text('D'), sg.Input(100,enable_events=True,k='-D-',size=(7, 1)),
    sg.Text('eps'), sg.Input(0.01,enable_events=True,k='-H-',size=(7, 1))
    ],
    [[sg.Push(), sg.Button('go'), sg.Push()]]
    ]
window = sg.Window('Нахождение корней',
                   layout,
                   finalize=True,
                   resizable=True) #, size = (640, 520)


def newton(a,b,eps):
        xn = (a+b)/2
        xn1 = xn - f(xn) / f_d(xn)
        while abs(xn1-xn) > eps:
            xn = xn1
            xn1 = xn - f(xn) / f_d(xn)
        return xn1

def dyhotomy(a, b, eps):
    while abs(f(b)-f(a)) > eps:
        mid = (a+b) / 2
        if f(mid) == 0 or abs(f(mid)) < eps:
            return mid
        elif f(a)*f(mid) < 0:
            b = mid
        else:
            a = mid
    print('Корень не найден')
    return None


fig = Figure(figsize=(cm_to_inch(18), cm_to_inch(14)))
ax_1 = fig.add_subplot(3, 1, 1)
# fig.subplots_adjust(top=0.8, bottom=0.1)
# ax_2 = ax_1.twinx()
ax_2 = fig.add_subplot(3, 1, 2)
ax_3 = fig.add_subplot(3, 1, 3)
canvas = Canvas(fig, window['Canvas'].Widget)
def plot_figure(a,b,d,eps):
    ax_1.cla()
    ax_2.cla()
    ax_3.cla()
    a = float(a)
    b = float(b)
    eps = float(eps)
    x_values = np.linspace(a, b, d)  # Например, от -5 до 5 с шагом 0.1
    x_0 = x_values[(abs(f(x_values)) < eps)]
    plt.figure(figsize=(12, 8))
    print(x_0)
    ax_1.plot(x_values, f(x_values), label='Функция')
    ax_1.scatter(x_0, f(x_0), color='red', label='Точки x_0')
    # ax_1.plot(x_values, x_0)
    ax_1.set_title('График функции')
    ax_1.grid(True)
    ax_1.legend()
    ax_2.plot(x_values, f(x_values), label='Функция')
    r = dyhotomy(a, b, eps)
    if r != None:
       ax_2.annotate(("x = "+ str(r)), (r, f(r)), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='blue')
       ax_2.scatter(r, f(r), color='red')
    #    print(r, f(r))
    else:
        print("No root!")
    # ax_2.set_aspect('equal')
    ax_2.set_title('Дихотомия')
    ax_2.legend()
    ax_3.plot(x_values, f(x_values), label='Функция')
    r = newton(a, b, eps)
    if r != None:
       ax_3.annotate(("x = "+ str(r)), (r, f(r)), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='blue')
       ax_3.scatter(r, f(r), color='red')
    #    print(r, f(r))
    ax_3.set_title('Ньютон')
    ax_3.legend()
    # plt.tight_layout()
    canvas.draw()
    
def launch():
    plot_figure(a,b,d,eps)

while True:
  event, values = window.read()
  # print(event)
  if event in (sg.WIN_CLOSED, 'Exit'):
    break
  elif event == '-A-':
      a = values[event]
  elif event == '-B-':
      b = values[event]
  elif event == '-D-':
      d = values[event]
  elif event == '-H-':
      eps = values[event]
  elif event == 'go':
      launch()
