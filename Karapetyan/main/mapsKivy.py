import networkx as nx
from networkx.classes.graph import Graph
from numpy.lib.npyio import load
import numpy.random as rnd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class main():

    def changeData(location):
        for i in range(len(location)):
                for j in range(len(location[i])):
                    if j==2:
                        location[i][j] = pd.to_numeric(location[i][j], downcast='integer')
                        return location

    def buildData( valuesTab="", wayInData="",valueStrart="",valueEnd="" ):
        
        valueStrart = valueStrart
        valueEnd = valueEnd
        location = []
        
        if wayInData!="":
            location = np.load(wayInData)
            location = main.changeData(location)
        
        else:
            location = np.array(valuesTab.split(" "))
            print("Данные в mapsKiby на входе ",location)
            location = location[:-1]
            location = location.reshape(int(len(location)/3),3)
            location = main.changeData(location)
        
        print("mapsKivy.buildData Контроль выходящих значений {}".format(location))
        return location

    def buildGraf (valuesTab, wayInData="",valueStrart="",valueEnd="", number = 0 ):
        location = main.buildData(valuesTab, wayInData="",valueStrart="",valueEnd="" )
        сonvertedData = pd.DataFrame(location)
        сonvertedData.columns = ("From", "In","Time")
        сonvertedData = сonvertedData.astype({'Time': np.float})
        print(сonvertedData)

        treeBuild = nx.from_pandas_edgelist( df=сonvertedData, source='From', target='In', edge_attr='Time') 
        positionTree = nx.spectral_layout(treeBuild) 

        nx.draw(treeBuild, positionTree,node_size=500, with_labels=True, node_color='#A0CBE2')

        valeuDijkstra = nx.dijkstra_path(treeBuild,valueStrart, valueEnd)
        print(valeuDijkstra)

        labels = {e: treeBuild.edges[e]['Time'] for e in treeBuild.edges}
        nx.draw_networkx_edge_labels(treeBuild, positionTree, edge_labels=labels)
        
        nx.draw_networkx_nodes(treeBuild,positionTree,valeuDijkstra,node_size=250, node_color="#00a693")
        nx.draw_networkx_nodes(treeBuild,positionTree,valeuDijkstra[:1],node_size=125, node_color="#eceabe")
        
        print("Кратчайший путь(временной): {}".format(nx.shortest_path_length(treeBuild,valueStrart, valueEnd, weight='Time' )))
        global valueForShortPathLengthTreeBuild 
        valueForShortPathLengthTreeBuild = treeBuild
        global valueForShortPathLengthValueStrart
        valueForShortPathLengthValueStrart = valueStrart
        global valueForShortPathLengthValueEnd
        valueForShortPathLengthValueEnd = valueEnd

        plt.savefig('Karapetyan/dataImage/' + str(number) + '.jpg')
        plt.show()

    def ShortPathLength(): 
        return nx.shortest_path_length(valueForShortPathLengthTreeBuild,valueForShortPathLengthValueStrart, valueForShortPathLengthValueEnd, weight='Time')

    def combiningArrayForSave(passOne='',passTwo='', nameFiles=''):
        location1 = np.load(passOne) 
        location2 = np.load(passTwo)   
        location3 = np.vstack([location1, location2])
        print("Сохраняем ")
        fullNameFilesPath = "Karapetyan\\data\\"+nameFiles
        np.save(fullNameFilesPath, location3 )
        print("Успешно сохранено")
        return  fullNameFilesPath
    
    def combiningArray(passOne='',passTwo=''):
        location1 = np.load(passOne) 
        location2 = np.load(passTwo)   
        joinData = np.vstack([location1, location2])
        readyJoinData = main.changeData(joinData)
        return readyJoinData