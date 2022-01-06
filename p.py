from matplotlib import pyplot as plt

# Класс Generation с (x,y)-(номер строки, номер столбца) и вектором ( alive ) с состояниями
# клеток ( живая(True)-мертвая(False) ) для каждого периода времени. Класс содержит
# методы : demise-birth для изменения состояния клетки ; neighbours возвращает соседей клетки ;
# alive_neighbours для подсчета живых соседей.

# То есть это класс , который представляет клетки в данной игре

class Generation:
    cells = []

    def __init__(self,x,y,alive):
        self.x = x
        self.y = y
        self.alive = alive
        Generation.cells.append(self)
        return

    def demise(self,t):
        self.alive[t] = False
        return

    def birth(self,t):
        self.alive[t] = True
        return

    def neighbours(self):
        a = []
        cells = Generation.cells
        a += [z for z in cells if z.x == self.x and z.y == self.y+1]
        a += [z for z in cells if z.x == self.x and z.y == self.y-1]
        a += [z for z in cells if z.x == self.x-1 and z.y == self.y]
        a += [z for z in cells if z.x == self.x-1 and z.y == self.y+1]
        a += [z for z in cells if z.x == self.x-1 and z.y == self.y-1]
        a += [z for z in cells if z.x == self.x+1 and z.y == self.y-1]
        a += [z for z in cells if z.x == self.x+1 and z.y == self.y+1]
        a += [z for z in cells if z.x == self.x+1 and z.y == self.y]
        return a

    def alive_neighbours(self,t):
        a = [z for z in self.neighbours() if z.alive[t]]
        return a
    
# Класс , который представляет способ задания начального состояния "вселенной" данной игры
# Здесь делаю лестницу из палочек

class setupp:
    @staticmethod

    def setup(n,m,t):
        for i in range(n):
            for j in range(m):
                a = [False]*t
                if i==3*j :
                    a[0] = True
                    Generation(i,j,a)
                elif i==3*(j-1) :
                    a[0] = True
                    Generation(i,j,a)
                elif i==3*(j-2) :
                    a[0] = True
                    Generation(i,j,a)
                else:
                    a[0] = False
                    Generation(i,j,a)
        return

# Класс , который представляет правила данной игры

class rules_of_game:
    @staticmethod

    def stage(t):
        for generation in Generation.cells:
            if generation.alive[t-1]:
                if len(generation.alive_neighbours(t-1))<2:
                    generation.demise(t)
                if len(generation.alive_neighbours(t-1)) in [2,3]:
                    generation.birth(t)
                if len(generation.alive_neighbours(t-1))>3:
                    generation.demise(t)
            else:
                if len(generation.alive_neighbours(t-1))==3:
                    generation.birth(t)
        return
    

# Класс Game. Осуществление самой игры
#play - процесс жизни клеток (запуск игры) ;
# results - показывает состояние клеток в каждый момент времени (результаты игры) .

class Game:
    def __init__(self, n, m, t):
        a = setupp()
        a.setup(n,m,t)
        self.n = n
        self.m = m
        self.t = t
        return
    
    

    def play(self):
        b = rules_of_game()
        for i in range(1,self.t):
            b.stage(i)
        return

    def results(self):
        cells = Generation.cells
        a = [[z.x, z.y, z.alive] for z in cells]
        return a

    
# Запуск игры (Blastoff !!!):    

    
# Задаю строки , столбцы , количество периодов соответственно    
        

    
n=30
m=30
t=50


# n=int(input("Введите желаемое кол-во строк (целое число)"))
# m=int(input("Введите желаемое кол-во столбцов (целое число)"))
# t=int(input("Введите желаемое кол-во периодов (целое число)"))
    

a = Game(n,m,t)

a.play()

a.results()


# сделаем снимки состояния "вселенной" данной игры в каждый момент времени:
for j in range(t):
    b = []
    for i in range(n):
        b.append([z[2][j] for z in a.results() if z[0]==i])
    plt.spy(b)
    plt.savefig(f"{j}time_GDS.png")

# Сделаем динамическую визуализацию :
from PIL import Image
import glob


frames = []
imgs = glob.glob("*time_GDS.png")
imgs.sort(key= lambda x: int(x.strip('time_GDS.png')))
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)



dur = 900
number = 0 # to infinity and beyond
    
# dur=int(input("Введите желаемое время продолжительности отображения на экране каждого кадра в миллисекундах"))
# number=int(input("Введите желаемое кол-во повторов анимации"))




frames[0].save('png_to_gif_GDS.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=dur, loop=number)

# Посмотрим куда сохранилась анимация
import os
cwd = os.getcwd()
print(f'Анимация в : {cwd}')

#удалим снимки состояния "вселенной" данной игры в каждый момент времени:
# test = os.listdir(cwd)

# for images in test:
#     if images.endswith("time_GDS.png"):
#         os.remove(os.path.join(cwd, images))