from BoxGridParticle import *
import numpy as np
from itertools import combinations # Итераторы
#------Класс "симулятор"--------------
class Simulator:
    def __init__(self,radius,amount,mass,temp,box,grid):  #--Этот конструктор запускает генерацию списка частиц. (радиус, кол-во, масса, температура,объект класса "сосуд", объект класса "сетка").
        self.box = box  #--Объект класса "сосуд".
        self.createListOfParticles(radius,amount,mass,temp)  #--Запуск функции, генерирующей массив всех частиц particles.
        self.grid = grid #--Объект класса "сетка".
        '''idArray - словарь, ключевые слова в котором -- номера клеток сетки.
        Его элементы -- массивы, в которых содержатся объекты класса particle,
        находящиеся в данных момент в клетке с соответствующим номером.'''
        self.idArray = {str(i)+str(j): [] for i,j in grid.getCellArray()}

    ''' Функция, генерирующая массив с частицами particles'''
    def createListOfParticles(self,radius,amount,mass,temp):
        self.particles = []  #---Массив частиц
        self.N = amount      #---Кол-во частиц
        for i in range(self.N):
            while True:
                x, y = (self.box.getW()-2*radius)*np.random.random()+radius, (self.box.getH()-2*radius)*np.random.random()+radius
                vel = np.sqrt(2*temp/mass) #np.random.random()*5
                angle = 2*np.pi*np.random.random()
                vX, vY = vel*np.cos(angle), vel*np.sin(angle)
                newParticle = Particle(x,y,vX,vY,radius,mass)
                for p2 in self.particles:
                    if(p2.overlaps(newParticle)):
                        break
                else:
                    self.particles.append(newParticle)
                    break
        print("List of particles has been created.")
    #-------------------------------------------
    '''Функция, очищающая idArray от предыдущих значений.'''
    def clearIdArray(self):
        for i in self.idArray:
            self.idArray[i].clear()
    #-------------------------------------------
    '''Функция, добавляющая в idArray новые значения.'''
    def registerIdArray(self):
        for p in self.particles:
            ID = p.IDs
            for n in ID:
                self.idArray[n].append(p)
    #-------------------------------------------            
    def handleCol(self):          # -- Обработка столкновений.
        def collision(p1,p2):
            self.r1 = p1.pos
            self.r2 = p2.pos
            self.v1 = p1.vel
            self.v2 = p2.vel
            d = np.linalg.norm(self.r1 - self.r2)**2
            u1 = self.v1 - np.dot(self.v1-self.v2, self.r1-self.r2) / d * (self.r1 - self.r2)
            u2 = self.v2 - np.dot(self.v2-self.v1, self.r2-self.r1) / d * (self.r2 - self.r1)
            p1.vel = u1
            p2.vel = u2

        '''Перебор пар частиц с одинаковым IDs на предмет столкновения.'''
        for NumberGroup in self.idArray:  
            pairs = combinations(range(len(self.idArray[NumberGroup])), 2)
            for i,j in pairs:
                if self.idArray[NumberGroup][i].overlaps(self.idArray[NumberGroup][j]):
                    collision(self.idArray[NumberGroup][i], self.idArray[NumberGroup][j])
        
    def update(self,dt):       # Обновление цикла программы.
        
        self.clearIdArray()
        self.registerIdArray()
        #self.handleCol()
        for i, p in enumerate(self.particles):
            self.grid.getCellNumber(p)
            p.move(dt,self.box)
        self.handleCol()

if __name__ == "__main__":
    print("This module isn't for direct call!")