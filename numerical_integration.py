import PySimpleGUI as sg
import math

a = 0
b = "pi"
d = 100
h = 0.01
n = 1000


def f(x):
   return 1


def rect_integral_left(f,xmin,xmax,n):
    dx=(xmax-xmin)/n
    area=0
    x=xmin
    for i in range(n):
        area+=dx*f(x)
        x+=dx
    return area

def rect_integral_right(f,xmin,xmax,n):       #O(h)     точность
    dx=(xmax-xmin)/n
    area=0
    x=xmin + dx
    for i in range(n):
        area+=dx*f(x)
        x+=dx
    return area

def tr_integral(f,xmin,xmax,n):             #O(h^2)
    dx=(xmax-xmin)/n
    area=0
    x=xmin
    for i in range(n):
        area+=dx*(f(x)+f(x+dx))/2
        x+=dx
    return area

def simpson_rule(f, a, b, n):
    if n%2 == 1: #n всегда четное
        n += 1
    dx = 1.0 * (b - a) / n
    sum = (f(a) + 4 * f(a + dx) + f(b))
    for i in range(1, int(n / 2)):
        sum += 2 * f(a + (2 * i) * dx) + 4 * f(a + (2 * i + 1) * dx)
    return sum * dx / 3

def cm_to_inch(value):
  return value / 2.54
def launch(a,b,n,f):
  if a == "pi":
     a = math.pi
  else:
     a = float(a)
  if b == "pi":
     b = math.pi
  else:
     b = float(b)
  n = int(n)
  window['l'].update(rect_integral_left(f,a,b,n))
  window['r'].update(rect_integral_right(f,a,b,n))
  window['t'].update(tr_integral(f,a,b,n))
  window['s'].update(simpson_rule(f,a,b,n))
  # print(rect_integral_right(f,a,b,n))
  # print(rect_integral_left(f,a,b,n))
  # print(tr_integral(f,a,b,n))
  # print(simpson_rule(f,a,b,n))

layout = [
    [sg.Text('A'), sg.Input(0,enable_events=True,k='-A-',size=(9, 1)),
    sg.Text('B'), sg.Input("pi",enable_events=True,k='-B-',size=(7, 1)),
    sg.Text('N'), sg.Input(1000,enable_events=True,k='-N-',size=(7, 1))
    ],
    [[sg.Text('М. Прямоугольников (левый)'),sg.Input('',k = 'l', enable_events=True)],
     [sg.Text('М. Прямоугольников (правый)'),sg.Input('',k = 'r', enable_events=True)],
     [sg.Text('Ф. трапеций'),sg.Input('',k = 't', enable_events=True)],
     [sg.Text('Ф.  Симпсона'),sg.Input('',k = 's', enable_events=True)]
     ],
    [[sg.Push(), sg.Button('go'), sg.Push()]]
    ]
window = sg.Window('Численное интегрирование',
                   layout,
                   finalize=True,
                   resizable=True) #, size = (640, 520)

while True:
  event, values = window.read()
  # print(event)
  if event in (sg.WIN_CLOSED, 'Exit'):
    break
  elif event == '-A-':
      a = values[event]
  elif event == '-B-':
      b = values[event]
  elif event == '-N-':
      n = values[event]
  elif event == 'go':
      launch(a,b,n,f)