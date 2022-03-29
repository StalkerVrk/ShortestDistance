import networkx as nx
from networkx.classes.graph import Graph
from numpy.lib.npyio import load
import numpy.random as rnd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class main():
    
    def Hellow():
        print("__Определения маршрута продвижения__")
        location_ = 0
        location = []

        while True:
            a = input("Маршрут L\nВыход N  ").lower()
            if a == "n":
                return print("До свидания")
            elif a=="l":
                while True:
                    
                    b = input("Построить маршрут L\nСохранить значения S\nИзменить значения C\nВыход E\n  ").lower()
                    
                    if b == "l":
                        location = main.Graph()
                        location_ = 1
                    
                    elif b == "s":
                        if location_ != 0:
                            name = input("Введите название файла: ")
                            np.save(name, location )
                            print("Успешно сохранено")
                        else: print("Ошибка, не заданы узлы продвижения")
                    
                    elif b == "c":
                        if location_ != 0:
                            location = main.ChangeLocation(location)
                        else: print("Ошибка, не заданы узлы продвижения")
                    elif b == "e":
                        break


    def Prep_Graph():
        Location_time = []
        print("\n- Вводим локации. \nПример ввода:\nFromNameLocation InNameLocation Time \nКогда ввода завершен, пропишите exit")
        control = 0
        
        while True:
            control +=1
            F = input("пункт А ")
            
            if F=="exit":
                break
            
            I,T = input("пункт Б "),int(input("Время "))
            Location_time.append([F,I,T])
            print("Ячейка {}".format(control))

        value = str(input("Введите начальный пункт: "))
        value_end =str(input("Введите конечный пункт: "))

        return Location_time, value, value_end
    

    def Graph():
        value = ''
        value_end = ''
        location = []
        if input("Загрузить данные: l\nВвести новые: n\n")== "l":
            name = input("Введите путь: ")
            print("Выбрано:\n",np.load(name))
            location = np.load(name)
            
            for i in range(len(location)):
                for j in range(len(location[i])):
                    if j==2:
                        location[i][j] = pd.to_numeric(location[i][j], downcast='integer')
            
            
            value = input("Введите начальный пункт: ")
            value_end =input("Введите конечный пункт: ")
        else:  
            location,value, value_end = main.Prep_Graph()

        df = pd.DataFrame(location)
        df.columns = ("From", "In","Time")
        df = df.astype({'Time': np.int})
        print(df)

        G = nx.from_pandas_edgelist(df=df, source='From', target='In', edge_attr='Time')
        pos = nx.spring_layout(G, k=40)  
        nx.draw(G, pos,node_size=1000, with_labels=True)
        
        labels = {e: G.edges[e]['Time'] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        print(nx.shortest_path_length(G,value, value_end, weight='Time'))

        plt.show()
        return location
    
    def ChangeLocation(location):
        df = pd.DataFrame(location)
        df.columns = ("From", "In","Time")
        print(df)

        a = int(input("Номер строки: "))
        location[a][0],location[a][1],location[a][2], = input("Заменить на: "),input(),int(input())
        df = pd.DataFrame(location)
        df.columns = ("From", "In","Time")
        print("Изменённый: \n",df)
        
        if input("Продолжить изменение? y/n ")=="y":
            main.ChangeLocation(location)
        else: return location
    
    def combiningArray():
        print("Объединить массивы")
        name = input("Введите путь: ")
        location1 = np.load(name) 
        name = input("Введите путь: ")
        location2 = np.load(name)   
        location3 = np.vstack([location1, location2])
        print("Сохраняем ")
        name = input("Введите название файла: ")
        np.save(name, location3 )
        print("Успешно сохранено") 

a = main
print(a.Hellow())
