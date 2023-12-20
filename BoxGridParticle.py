import numpy as np
import math
from itertools import product
#----------Класс "сетка"--------------
class Grid:
    def __init__(self,N,box):       # Конструктор класса "сетка".
        self.N = N  # Количество клеток на одной стороне сетки
        self.box = box # Объект сосуд, в котором создаётся сетка
    
    def getCellNumber(self,p):
        ''' Данная функция определяет номер клетки сетки, на которой
            находится частица p. Для этого создаётся массив verticies,
            содержащий координаты вершин квадрата, в который вписана частица.
            Для каждый вершины вычисляется величины i = [N*Xv/width] и
            j = [N*Yv/height ], где Xv и Yv - координаты вершины, [] - взятие целой части.
            Клетки имеют нумерацию ij, где i и j - какие-то целые положительные числа.
            Например, в сетке при N=3 (то есть 3 на 3) клетка в нижнем левом углу имеет
            номер 00, клетка правее - 10. Вычисляемые для вершин квадрата величины  - номера
            соответствующей клетки вершины.
            При прохождении проверки на нахождение в какой-то клетке в массив объекта "частица"
            IDs добавляется номер соответствующей клетки.
        '''
        verticies = [[p.pos[0]-p.radius,p.pos[1]-p.radius],[p.pos[0]-p.radius,p.pos[1]+p.radius],
                     [p.pos[0]+p.radius,p.pos[1]+p.radius], [p.pos[0]+p.radius,p.pos[1]-p.radius]]
        p.IDs.clear()   # Очищение массива IDs от прежних значений.
        for vertex in verticies:
            i = math.floor((vertex[0]*self.N)/self.box.getW())
            j = math.floor((vertex[1]*self.N)/self.box.getH())
            if(i< self.N and j< self.N):
                p.IDs.add(str(i)+str(j))    # Добавление нового номера в IDs.
    def getCellArray(self):
        pairs = product(range(self.N),range(self.N)) # Массив, содержащий все номера клеток сетки.
        return pairs
    
#----------Класс "сосуд"--------------
class Box:
    def __init__(self,width,height):    # Конструктор класса "сосуд".
        self.width = width
        self.height = height
    def getW(self):
        return self.width
    def getH(self):
        return self.height
#-------Класс "частица"---------------
class Particle:
    def __init__(self,x,y,vX,vY,radius,mass):
        self.pos = np.array([x,y])      # Радиус-вектор
        self.vel = np.array([vX,vY])    # Скорость-вектор
        self.radius = radius            # Радиус
        self.mass = mass                # Масса
        self.IDs = set([])              # Множество из номеров клеток
    def overlaps(self,p2):          # Функция, проверяющая частицы на пересечение друг с другом.
        return (self.radius+p2.radius)**2 > ((self.pos[0]-p2.pos[0])**2+(self.pos[1]-p2.pos[1])**2)
    def move(self,dt,box):
        self.pos += dt*self.vel
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.vel[0] *= -1
        if self.pos[0] + self.radius > box.getW():
            self.pos[0] = box.getW()-self.radius
            self.vel[0] *= -1
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.vel[1] *= -1
        if self.pos[1] + self.radius > box.getH():
            self.pos[1] = box.getH()-self.radius
            self.vel[1] *= -1
    def getVel2(self):
        return (self.vel[0]**2+self.vel[1]**2)

if __name__ == "__main__":
    print("This module isn't for direct call!")