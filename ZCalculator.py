import tkinter.messagebox as tmsg
from math import *
import time
import os
import tkinter as tk
from tkinter import *
import math
root = tk.Tk()
root.title('ZCalculator')
root.config(bg='gray')
root.geometry('430x470')
root.resizable(0, 0)
display_text = tk.StringVar()
display_text.set('0.00')
canvas = tk.Canvas(bg='gray', bd=0, highlightthickness=0)
canvas.pack(padx=15, pady=15)
var = {'front': [], 'back': [], 'decimal': False,
       'x_val': 0.0, 'y_val': 0.0, 'result': 0.0, 'operator': ''}

def main_btn(text, row, col, width=7, height=2, font=('Calibri', 24)):
    btn = tk.Button(canvas, text=text, bg='black', fg='gray', width=5,
                    height=1, font=font, command=lambda: main_click(text))
    return btn.grid(row=row, column=col, padx=4, pady=4)

tk.Label(canvas, textvariable=display_text, anchor='e', bg='black', fg='white', font=(
    'Digital-7', 40)).grid(row=1, columnspan=4, sticky='ew', padx=4, pady=2)
main_btn("C",  2, 0)
main_btn("CE", 2, 1)
main_btn("%", 2, 2)
main_btn("/", 2, 3)
main_btn("7", 3, 0)
main_btn("8", 3, 1)
main_btn("9", 3, 2)
main_btn("*", 3, 3)
main_btn("4", 4, 0)
main_btn("5", 4, 1)
main_btn("6", 4, 2)
main_btn("-", 4, 3)
main_btn("1", 5, 0)
main_btn("2", 5, 1)
main_btn("3", 5, 2)
main_btn("+", 5, 3)
main_btn("0", 6, 0)
main_btn(".", 6, 1)
rtn_btn = tk.Button(canvas, text='=', bg='white', width=9, height=1, font=(
    'Franklin Gothic Book', 24), command=lambda: main_click("="))
rtn_btn.focus()
rtn_btn.grid(row=6, column=2, columnspan=2, padx=4, pady=4)

def main_click(event):
    global var
    if event in ['CE', 'C']:
        clear_click()
        update_display(0.0)
        var['operator'] = ''
        var['result'] = 0.0
    if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        number_click(event)
    if event in ['*', '/', '+', '-']:
        operator_click(event)
    if event == '.':
        var['decimal'] = True
    if event == '%':
        update_display(var['result'] / 100.0)
    if event == '=':
        calculate_click()

def update_display(display_value):
    global display_text
    try:
        display_text.set('{:,.2f}'.format(display_value))
    except:
        display_text.set(display_value)

def format_number():
    return ''.join(var['front']) + '.' + ''.join(var['back'])

def number_click(event):
    global var
    if var['decimal']:
        var['back'].append(event)
    else:
        var['front'].append(event)

    display_value = float(format_number())
    update_display(display_value)

def clear_click():
    global var
    var['front'].clear()
    var['back'].clear()
    var['decimal'] = False

def operator_click(event):
    global var
    var['operator'] = event
    try:
        var['x_val'] = float(format_number())
    except:
        var['x_val'] = var['result']
    clear_click()

def calculate_click():
    global var
    if not var['x_val']:
        return
    try:
        var['y_val'] = float(format_number())
    except:
        var['y_val'] = 0.0
    try:
        var['result'] = float(
            eval(str(var['x_val']) + var['operator'] + str(var['y_val'])))
        update_display(var['result'])
    except ZeroDivisionError:
        error = "ERROR! DIV/0"
        var['x_val'] = 0.0
        clear_click()
        update_display(error)
    clear_click()
menubar = Menu(root)
def printmessage():
    print("This is test for menu")
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="scientific calculator",command=lambda: openscientific())
filemenu.add_separator()
filemenu.add_command(label='Exit',command=quit)
menubar.add_cascade(label="Go", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Print Message", command=printmessage)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)
def openscientific():
    newWindow = Toplevel(root)
    newWindow.title("scientific")

    newWindow.resizable(0, 0)
    def getvals(event):
        value = event.widget.cget('text')
        if value == 'Clr':
            sc_variable.set('')
        elif value == '=':
            try:
                sc_variable.set(eval(screen.get()))
                screen.update()
            except Exception as e:
                sc_variable.set('Error - Wait for 3 sec')
                screen.update()
                status_var.set('Preparing...')
                screen.update()
                time.sleep(3)
                sc_variable.set('')
                screen.update()
                status_var.set('Ready..')
                screen.update()

        else:
            sc_variable.set(f'{sc_variable.get()}{value}')


    def term_of_use():
        tmsg.showinfo('Terms of Use ', 'IF YOU LIVE IN (OR IF YOUR PRINCIPAL PLACE OF BUSINESS IS IN) THE UNITED STATES, PLEASE READ THE BINDING ARBITRATION CLAUSE AND CLASS ACTION WAIVER IN SECTION 11. IT AFFECTS HOW DISPUTES ARE RESOLVED.')


    def send_feedback():
        ans = tmsg.askquestion(
            'Feedback Hub', 'Was your experience good with us ? ')
        if ans == 'yes':
            tmsg.showinfo('Feedback', 'Please Rate us on PlayStore')
        else:
            tmsg.showinfo(
                'Feedback', 'We will contact you soon to know about your bad experience')    
    canvas_width = 555
    canvas_height = 575
    newWindow.geometry('400x400')
    newWindow.maxsize(canvas_width, canvas_height)
    newWindow.minsize(canvas_width, canvas_height)
    newWindow.title(' Scientific ZCalCulator ')
    newWindow.config(bg='gray')
    sc_variable = StringVar()
    sc_variable.set('0.00')
    screen = Entry(newWindow, textvariable=sc_variable,
                font='Digital-7 35', fg='white', bg='black', borderwidth=10)
    screen.pack(pady=20)

    f = Frame(newWindow)
    f.pack()
    b1 = Button(f, text='7', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b2 = Button(f, text='8', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b3 = Button(f, text='9', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b4 = Button(f, text='*', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b5 = Button(f, text='sin', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b6 = Button(f, text='(', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b1.bind('<Button-1>', getvals)
    b2.bind('<Button-1>', getvals)
    b3.bind('<Button-1>', getvals)
    b4.bind('<Button-1>', getvals)
    b5.bind('<Button-1>', getvals)
    b6.bind('<Button-1>', getvals)
    buttons = [b1, b2, b3, b4, b5, b6]
    count = 0
    for i in range(6):
        buttons[count].grid(row=1, column=i)
        count += 1
    f = Frame(newWindow)
    f.pack()
    b1 = Button(f, text='4', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b2 = Button(f, text='5', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b3 = Button(f, text='6', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b4 = Button(f, text='-', font='Calibri 17', padx=20, pady=20,
            borderwidth=3, fg='gray', bg='black', width=3)

    b5 = Button(f, text='cos', font='Calibri 17', padx=20,
            pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b6 = Button(f, text=')', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)
    b1.bind('<Button-1>', getvals)
    b2.bind('<Button-1>', getvals)
    b3.bind('<Button-1>', getvals)
    b4.bind('<Button-1>', getvals)
    b5.bind('<Button-1>', getvals)
    b6.bind('<Button-1>', getvals)
    buttons = [b1, b2, b3, b4, b5, b6]
    count = 0
    for i in range(6):
        buttons[count].grid(row=2, column=i)
        count += 1
    f = Frame(newWindow)
    f.pack()
    b1 = Button(f, text='1', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b2 = Button(f, text='2', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b3 = Button(f, text='3', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b4 = Button(f, text='+', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b5 = Button(f, text='tan', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b6 = Button(f, text='%', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b1.bind('<Button-1>', getvals)
    b2.bind('<Button-1>', getvals)
    b3.bind('<Button-1>', getvals)
    b4.bind('<Button-1>', getvals)
    b5.bind('<Button-1>', getvals)
    b6.bind('<Button-1>', getvals)
    buttons = [b1, b2, b3, b4, b5, b6]
    count = 0
    for i in range(6):
        buttons[count].grid(row=3, column=i)
        count += 1
    f = Frame(newWindow)
    f.pack()
    b1 = Button(f, text='.', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b2 = Button(f, text='0', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b3 = Button(f, text='sinh', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b4 = Button(f, text='cosh', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b5 = Button(f, text='tanh', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b6 = Button(f, text='pi', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)
    b1.bind('<Button-1>', getvals)
    b2.bind('<Button-1>', getvals)
    b3.bind('<Button-1>', getvals)
    b4.bind('<Button-1>', getvals)
    b5.bind('<Button-1>', getvals)
    b6.bind('<Button-1>', getvals)
    buttons = [b1, b2, b3, b4, b5, b6]
    count = 0
    for i in range(6):
        buttons[count].grid(row=4, column=i)
        count += 1
    f = Frame(newWindow)
    f.pack()

    b1 = Button(f, text='log10', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b2 = Button(f, text='exp', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b3 = Button(f, text='/', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='gray', bg='black', width=3)

    b4 = Button(f, text='Clr', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b5 = Button(f, text='log', font='Calibri 17', padx=20,
                pady=20, borderwidth=3, fg='gray', bg='black', width=3)

    b6 = Button(f, text='=', font='Calibri 17', padx=20, pady=20,
                borderwidth=3, fg='black', bg='white', width=3)

    b1.bind('<Button-1>', getvals)
    b2.bind('<Button-1>', getvals)
    b3.bind('<Button-1>', getvals)
    b4.bind('<Button-1>', getvals)
    b5.bind('<Button-1>', getvals)
    b6.bind('<Button-1>', getvals)
    buttons = [b1, b2, b3, b4, b5, b6]
    count = 0
    for i in range(6):
        buttons[count].grid(row=5, column=i)
        count += 1
    status_var = StringVar()
    status_var.set('Ready..')
root.mainloop()