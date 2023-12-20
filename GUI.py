'''Graphical interface of the program'''

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from BoxGridParticle import *
from Simulator import *
from tkinter import ttk
import time
from PIL import Image, ImageTk
import webbrowser
#----------------------
'''Variables'''
N = ''     # --- number of particles
T = ''     # --- temperature
dt = ''    # --- time step
m = ''     # --- particle's mass
Time = ''  # --- total time of simulation
radius = '' # --- particle's radius
a = ''     # --- length of box
b = ''   # --- width of box
gr = ''  # --- grid parameter

STAT_LIST = [] # --- list with statistics
maximum_velocities = [] #--- list used for x-axis range
vel2 = 0 #--- RMS velocity
y_limit = 1
#-----------------------
'''Splitting the window into frames'''
root = tk.Tk()
root.geometry('900x563')
root.title("Simulation of Maxwell's distribution")
root.resizable(width=False,height=False)
frame = tk.Frame(root,highlightthickness=0,highlightbackground='red')
frame2 = tk.Frame(root,highlightthickness=1,highlightbackground='black')
frame.grid(row=0,column=0,padx=40,pady=20,ipadx=20,ipady=13)
frame2.grid(row=0,column=1,padx=40,pady=0,ipadx=0,ipady=0)
icon = tk.PhotoImage(file='icon.png')
#-------------------
'''Widgets of the 1st frame'''
L1 = tk.Label(frame,text="Кол-во частиц", font = (25))
L1.grid(row=0,column=0)

txtb1 = tk.Entry(frame,textvariable=N,font=(25))
txtb1.grid(row=1,column=0,pady=0)

L2 = tk.Label(frame,text="Температура", font = (25))
L2.grid(row=2,column=0,pady=0)

txtb2 = tk.Entry(frame,textvariable=T,font=(25))
txtb2.grid(row=3,column=0,pady=0)

L3 = tk.Label(frame,text="Масса частиц", font = (25))
L3.grid(row=4,column=0,pady=0)

txtb3 = tk.Entry(frame,textvariable=m,font=(25))
txtb3.grid(row=5,column=0,pady=0)

L4 = tk.Label(frame,text="Шаг времени", font = (25))
L4.grid(row=6,column=0,pady=0)

txtb4 = tk.Entry(frame,textvariable=dt,font=(25))
txtb4.grid(row=7,column=0,pady=0)

L5 = tk.Label(frame,text="Время симуляции", font = (25))
L5.grid(row=8,column=0,pady=0)

txtb5 = tk.Entry(frame,textvariable=Time,font=(25))
txtb5.grid(row=9,column=0,pady=0)

L9 = tk.Label(frame,text="Длина сосуда", font = (25))
L9.grid(row=10,column=0,pady=0)

txtb9 = tk.Entry(frame,textvariable=a,font=(25))
txtb9.grid(row=11,column=0,pady=0)

L12 = tk.Label(frame,text="Ширина сосуда", font = (25))
L12.grid(row=12,column=0,pady=0)

txtb12 = tk.Entry(frame,textvariable=b,font=(25))
txtb12.grid(row=13,column=0,pady=0)

L10 = tk.Label(frame,text="Частота сетки", font = (25))
L10.grid(row=14,column=0,pady=0)

txtb10 = tk.Entry(frame,textvariable=gr,font=(25))
txtb10.grid(row=15,column=0,pady=0)

L11 = tk.Label(frame,text="Радиус частиц", font = (25))
L11.grid(row=16,column=0,pady=0)

txtb11 = tk.Entry(frame,textvariable=radius,font=(25))
txtb11.grid(row=17,column=0,pady=0)

#---------Функция, считающая число частиц,--------------
#----движущихся со скоростью от vel до vel+dv-----------
def countVelocities(array,vel,dv):
    n = 0
    for v in array:
        if (v > vel) and (v < vel+dv):
            n+=1
    return n
#--------------------------------------------------------
#--------------------------------------------------------

drawGrid = tk.IntVar()   # --- option for drawing plot grid
drawCurve = tk.IntVar()  # --- option for drawing theoretical curve

def start():
    if txtb1.get() == '' or txtb2.get() == '' or txtb3.get() == '' or txtb4.get() == '' or txtb5.get() == '':
        tk.messagebox.showerror("error","Введены не все параметры!")
        return
    elif txtb1.get().replace('.','',1).isdigit() == False or txtb2.get().replace('.','',1).isdigit() == False or txtb3.get().replace('.','',1).isdigit() == False or txtb4.get().replace('.','',1).isdigit() == False or txtb5.get().replace('.','',1).isdigit() == False:
        tk.messagebox.showerror("error","Должны быть введены числа!")
        return
    elif txtb9.get().replace('.','',1).isdigit() == False or txtb10.get().replace('.','',1).isdigit() == False or txtb11.get().replace('.','',1).isdigit() == False or txtb12.get().replace('.','',1).isdigit() == False:
        tk.messagebox.showerror("error","Должны быть введены числа!")
        return
    elif int(txtb1.get()) <= 0:
        tk.messagebox.showerror("error","Количество частиц должно быть больше 0!")
        return
    elif float(txtb2.get()) <= 0:
        tk.messagebox.showerror("error","Абсолютная температура должна быть больше 0!")
        return
    elif float(txtb3.get()) <= 0:
        tk.messagebox.showerror("error","Масса частиц неотрицательна!")
        return
    elif float(txtb4.get()) <= 0:
        tk.messagebox.showerror("error","Шаг времени больше 0!")
        return
    elif float(txtb5.get()) <= 0:
        tk.messagebox.showerror("error","Время симуляции больше 0!")
        return
    elif float(txtb4.get()) >= float(txtb5.get()):
        tk.messagebox.showerror("error","Шаг времени должен не превосходить время симуляции")
        return
    elif float(txtb9.get()) <= 0 or float(txtb12.get()) <= 0:
        tk.messagebox.showerror("error","Размеры сосуда больше!")
        return
    elif float(txtb10.get()) <= 0:
        tk.messagebox.showerror("error","Частота сетки больше 0!")
        return
    elif float(txtb10.get())%1 != 0:
        tk.messagebox.showerror("error","Частота сетки - целое число!")
        return
    elif float(txtb11.get()) <= 0:
        tk.messagebox.showerror("error","Радиус частицы больше 0!")
        return
    elif np.pi*int(txtb1.get())*float(txtb11.get())**2 >= 3*float(txtb9.get())*float(txtb12.get())/4:
        tk.messagebox.showerror("error","Частицы не помещаются! Или увеличьте размеры сосуда, или сделайте радиус частиц меньше!")
        return

    N = txtb1.get()
    T = txtb2.get()
    m = txtb3.get()
    dt = txtb4.get()
    Time = txtb5.get()
    a = txtb9.get()
    b = txtb12.get()
    gr = txtb10.get()
    radius = txtb11.get()
    global vel2
    vel2 = 2*float(T)/float(m) 
    
    L7.config(text = "активно",fg = 'green')
    slider.set(0)
    STAT_LIST.clear()
    maximum_velocities.clear()
    
    box = Box(float(a),float(b))
    grid = Grid(int(gr),box)
    s1 = Simulator(float(radius),int(N),float(m),float(T),box,grid) #--симулятор(радиус_частицы,кол-во,масса,сосуд)
    C = round(float(Time)/float(dt))
    
    for i in range(C):
        s1.update(float(dt))
        velocities = [np.hypot(p.vel[0],p.vel[1]) for p in s1.particles]
        vel_range = np.arange(0,max(velocities)+10,1)
        Ns = [countVelocities(velocities,vel,1)/int(N) for vel in vel_range]
        data = np.array([vel_range,Ns])
        STAT_LIST.append(data)
        maximum_velocities.append(max(velocities))
        L8.config(text='Выполнено: '+str(100*round(i/C))+'%')
        root.update()
    
    L7.config(text = "неактивно",fg = 'red')
    L8.config(text='Выполнено: '+'0%')
    figure.axes[0].bar(STAT_LIST[0][0],STAT_LIST[0][1],width=1,
                       color='#1f77b4',edgecolor='black')
    figure.axes[0].set_ylim(0,y_limit)
    figure.axes[0].set_xlim(0,max(maximum_velocities)+5)
    
    if drawGrid.get():
        figure.axes[0].grid(True)
    if drawCurve.get():
        v = np.arange(0,max(maximum_velocities),1)
        fv = (2*v)/(vel2)*np.exp(-(np.power(v,2))/(vel2))*1
        figure.axes[0].plot(v,fv,color='red')
    slider.config(from_=0,to=len(STAT_LIST)-1)
    canvas.draw()
    root.update()
    
def slider_changed(event):
    global y_limit
    figure.axes[0].cla()
    figure.axes[0].set_xlabel('Скорость $v$,м/с')
    figure.axes[0].set_ylabel('$dN/Ndv$')
    figure.axes[0].set_title('Распределение частиц по скоростям')
    
    figure.axes[0].set_xlim(0,max(maximum_velocities)+5)
    
    if drawGrid.get():
        figure.axes[0].grid(True)
    if drawCurve.get():
        v = np.arange(0,max(maximum_velocities),1)
        fv = (2*v)/(vel2)*np.exp(-(np.power(v,2))/(vel2))*1
        figure.axes[0].plot(v,fv,color='red')
    figure.axes[0].bar(STAT_LIST[slider.get()][0],STAT_LIST[slider.get()][1],
                       width=1,edgecolor='black')
    figure.axes[0].set_ylim(0,y_limit)
    canvas.draw()
    root.update()

def slider2_changed(event):
    global y_limit
    y_limit = slider2.get()
    figure.axes[0].set_ylim(0,y_limit)
    canvas.draw()
    
def save_to_txt():
    if STAT_LIST == []:
        tk.messagebox.showerror("error","Отсутствуют данные! Запустите симуляцию!")
    else:
        filepath = tk.filedialog.asksaveasfilename()
        if filepath != "":
            with open(filepath+".txt", 'w') as output:
                for row in STAT_LIST:
                    output.write(str(row) + '\n')
            tk.messagebox.showinfo("Save to .txt","Сохранение данных выполнено!")
        else:
            tk.messagebox.showerror("error","Не указан путь сохранения!")

clicked = 0

def save_plots():
    if STAT_LIST == []:
        tk.messagebox.showerror("error","Отсутствуют данные! Запустите симуляцию!")
        return
    global clicked
    clicked += 1 
    if clicked == 1:
        top_level = tk.Toplevel()
        top_level.geometry('300x185')
        top_level.title("Window")
        top_level.resizable(width=False,height=False)
        top_level.iconphoto(False,icon)
               
        W1 = tk.Label(top_level,text="Выберите с какого по какой"+ "\nкадр сохранять графики. Введите \nномера крайних кадров.", 
                      font = (25))
        W1.pack()
        W2 = tk.Label(top_level,text="Первый кадр", font = (25))
        W3 = tk.Label(top_level,text="Последний кадр", font = (25))
        
        field1 = tk.Entry(top_level)
        field2 = tk.Entry(top_level)
        field1.place(x=5,y=70)
        field2.place(x=170,y=70)
        W2.place(x=14,y=85)
        W3.place(x=170,y=85)
        combobox = ttk.Combobox(top_level,values=[".png",".jpeg",".svg"])
        combobox.place(x=5,y=130)
        
        def save():
            global y_limit
            global clicked
            if field1.get() == "" or field2.get() == "":
                tk.messagebox.showerror("error","Введены не все числа!")
                return
            elif float(field1.get())%1 != 0 or float(field2.get())%1 != 0:
                tk.messagebox.showerror("error","Введённые числа нецелые!")
                return
            elif float(field1.get()) > float(field2.get()):
                tk.messagebox.showerror("error","Номер первого кадра не больше последнего!")
                return
            elif float(field1.get()) < 0 or float(field2.get()) < 0:
                tk.messagebox.showerror("error","Числа должны быть больше 0!")
                return
            elif float(field1.get()) > len(STAT_LIST)-1 or float(field2.get()) > len(STAT_LIST)-1:
                tk.messagebox.showerror("error","Кадров с введенными номерами нет!")
                return
            n = round(float(field1.get()))
            k = round(float(field2.get()))+1
            filepath = tk.filedialog.askdirectory()
            if filepath != "":
                for i in range(n,k):
                    X = STAT_LIST[i][0]
                    Y = STAT_LIST[i][1]
                    fig2 = Figure(figsize=(5, 4), dpi=100)
                    plot2 = fig2.add_subplot(1, 1, 1)
                    fig2.axes[0].bar(X,Y,width=1,color='#1f77b4',edgecolor='black')
                    fig2.axes[0].set_ylim(0,y_limit)
                    fig2.axes[0].set_xlim(0,max(maximum_velocities)+5)
                    fig2.axes[0].set_xlabel('Скорость $v$,м/с')
                    fig2.axes[0].set_ylabel('$dN/Ndv$')
                    fig2.axes[0].set_title('Распределение частиц по скоростям')
                    if drawGrid.get():
                        fig2.axes[0].grid(True)
                    if drawCurve.get():
                        v = np.arange(0,max(maximum_velocities),1)
                        fv = (2*v)/(vel2)*np.exp(-(np.power(v,2))/(vel2))*1
                        fig2.axes[0].plot(v,fv,color='red')
                    
                    fig2.savefig(filepath+'/plot'+str(i)+combobox.get())
                    fig2.axes[0].cla()
                tk.messagebox.showinfo("Save plots","Сохранение графиков выполнено!")
                clicked -= clicked
            else:
                tk.messagebox.showerror("error","Не указан путь сохранения!")
                clicked -= clicked
            top_level.destroy()
        
        def callback():
            global clicked
            clicked -= clicked
            top_level.destroy()
            
        top_level.protocol("WM_DELETE_WINDOW",callback)
        btn4 = tk.Button(top_level,text='>Сохранить<',font=(25),command=save)
        btn4.place(x=180,y=120)
        top_level.mainloop()

btn1 = tk.Button(frame,text='>Пуск<',command=start,font=(25))
btn1.grid(row=18,column=0,pady = 2)

btn2 = tk.Button(frame,text='>Сохранить в .txt<', command = save_to_txt,font=(25))
btn2.grid(row=19,column=0,pady = 2)

btn3 = tk.Button(frame,text='>Сохранить графики<',font=(25),command = save_plots)
btn3.grid(row=20,column=0,pady = 2)

figure = Figure(figsize=(5, 4), dpi=100)
plot = figure.add_subplot(1, 1, 1).set_xlabel('Скорость $v$,м/с')
figure.axes[0].set_ylabel('$dN/Ndv$')
figure.axes[0].set_title('Распределение частиц по скоростям')
figure.axes[0].set_ylim(0,1)
canvas = FigureCanvasTkAgg(figure, frame2)
canvas.get_tk_widget().grid(row=0, column=1)

L6 = tk.Label(root, text="Состояние симуляции:",font=(25))
L7 = tk.Label(root,text="неактивно",fg='red',font=(25))
L6.place(x=600,y=20)
L7.place(x=770,y=20)
L8 = tk.Label(root,text='Выполнено: 0%',font=(25))
L8.place(x=600,y=40)
slider = tk.Scale(root,from_ = 1, to=1,orient = 'horizontal',command=slider_changed)
slider.place(x=460,y=520)
L13 = tk.Label(root,text="Выбрать кадр")
L13.place(x=475,y=500)
slider2 = tk.Scale(root,from_ = 0.05, to=1,orient = 'horizontal',
                   resolution=0.05,command=slider2_changed)
slider2.place(x=350,y=520)
L14 = tk.Label(root,text="Масштаб по y")
L14.place(x=365,y=500)
chB1 = tk.Checkbutton(root,text="Рисовать теоретическую зависимость",
                      variable = drawCurve)
chB1.place(x=580,y=520)
    
chB2 = tk.Checkbutton(root,text="Рисовать сетку",variable = drawGrid)
chB2.place(x=580,y=540)

clicked2 = 0

def info():
    global clicked2
    clicked2 += 1 
    def callback():
        global clicked2
        clicked2 -= clicked2
        top_level.destroy()
    if clicked2 == 1:
        top_level = tk.Toplevel()
        top_level.geometry('300x215')
        top_level.title("Information")
        top_level.resizable(width=False,height=False)
        top_level.iconphoto(False,icon)
        top_level.protocol("WM_DELETE_WINDOW",callback)
        notebook = ttk.Notebook(top_level)
        notebook.pack(pady=10, expand=True)
        frame11 = ttk.Frame(notebook, width=400, height=300)
        frame21 = ttk.Frame(notebook, width=400, height=300)
        frame11.pack(fill='both', expand=True)
        frame21.pack(fill='both', expand=True)
        notebook.add(frame11, text='Разработчики')
        notebook.add(frame21, text='Как работает программа')
        
        #-----Developers-----------------
        text1 = tk.Label(frame11,text="Разработчики \nАндрюшечкин Алексей \nЗалесова Екатерина \nПопова Ксения \nПлиев Аслан", font=(30))
        text1.pack()
        #-----Software-----------------
        docs1 = "В данной программе моделируется поведение \nдвумерного идеального газа и определяется \nраспределение его частиц по скоростям."
        docs2 = "\nФизические параметры вводятся в \nусловных единицах. Параметр <<Частота сетки>> \nиспользуется для оптимизации \nработы обработчика столкновений. \nПодробнее см. "
        text2 = tk.Label(frame21,text=docs1+docs2,anchor="e")
        text2.pack()
        
        link = tk.Label(frame21,text="здесь",fg='blue')
        link.place(x=185,y=105)
        link.bind('<Button-1>',
                  lambda x: webbrowser.open_new("https://github.com/Andryu1233/Simulation-of-Maxwell-s-distribution.-MIPT.-Python-Project.git"))
        top_level.mainloop()

image_file = Image.open("info.png")
image_file = image_file.resize((32,32))
img = ImageTk.PhotoImage(image_file)

btn5 = tk.Button(root,image=img,command=info)
btn5.place(x=360,y=30)

l = tk.Label(root,text="О программе",font=(25))
l.place(x=400,y=37)

#-------------------
if __name__ == "__main__":
    root.iconphoto(False, icon)
    root.mainloop()