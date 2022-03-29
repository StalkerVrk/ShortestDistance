from kivy.config import Config

from typing import Text
from kivy.lang.builder import Instruction
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

import mapsKivy 
import numpy as np


Window.size = (800,600)

class Digt(ScreenManager):
    def InstractionText(self):
        text = ''
        path = r"txt\instruction.txt"
        with open(path, 'r',encoding="utf-8") as file:
            for line in file:
                text += line
        return text

class Main(MDApp):

    def getTxtMainScr(self):
        try:
            global LocationOT
            global LocationDO
            global during

            LocationOT = self.root.ids.locationOTK.text
            LocationDO = self.root.ids.locationDOK.text
            during = self.root.ids.timeK.text
            print(LocationOT,LocationDO,during)
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка импорта данных\nиз таблицы"
        else:
            self.root.ids.notification.text = "Ошибок нет"
    
    def addTabReadyValues(self, data):
        try:
            data.text += LocationOT+" "+LocationDO+" "+during+"\n"
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка импорта данных \nв таблицу"
        else:
            self.root.ids.notification.text = "Ошибок нет"

    def getValuesWhithDataInTab(self,data):
        try:
            path = self.root.ids.pathToValuesK.text
            data.text = Main.converDataForTab(mapsKivy.main.buildData("",path))
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка импорта значений\nиз файла"
        else:
            self.root.ids.notification.text = "Ошибок нет"
    
    def combiningArray(self, data):
        try:
            location1 = self.root.ids.passLoadDataOne.text
            location2 = self.root.ids.passLoadDataTwo.text
            joinDataWithPath = Main.converDataForTab(mapsKivy.main.combiningArray(location1,location2))
            data.text = joinDataWithPath
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка объединения файлов"
        else:
            self.root.ids.notification.text = "Ошибок нет"

    def converDataForTab(dataBeforeProcessing):
        textData = ''
        
        for i in range(len(dataBeforeProcessing)):
                for j in range(len(dataBeforeProcessing[i])):
                    if j == 2:
                        textData += dataBeforeProcessing[i][j]+"\n"
                    else:
                        textData += dataBeforeProcessing[i][j]+' '
        return textData

    def saveData(self):
        try:
            dataTextWithTab = self.root.ids.tabReadyValuesK.text
            name = "Karapetyan/data/"+self.root.ids.nameSave.text
            data = mapsKivy.main.buildData(dataTextWithTab.replace("\n"," "))
            
            if self.root.ids.nameSave.text != '':
                np.save(name, data)
                self.root.ids.notification.text = "Сохранили"
            else:
                self.root.ids.notification.text = "Проверьте данные"
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка сохранения"

    def getValuesStarEndPos(self):
        try:

            global startingPosition
            global finalPosition
            global pathToValues
            global tabReadyValues

            startingPosition = self.root.ids.startingPositionK.text
            finalPosition = self.root.ids.finalPositionK.text
            pathToValues = self.root.ids.pathToValuesK.text
            print(startingPosition,finalPosition,pathToValues) 

            tabReadyValues = self.root.ids.tabReadyValuesK.text
            print("Табличные значения: {}".format(tabReadyValues))
            
            self.root.ids.numberPosForTwoScreen.text = "Количество маршрутов в древе: " + str(len(mapsKivy.main.buildData(tabReadyValues.replace("\n",' ')))) #вывод количества маршрутов
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка в пути&нач/конеч точках"
        else:
            self.root.ids.notification.text = "Ошибок нет"

    numberImg = 0
    def calculateNumbersForSaveImg(self):
        try:
            Main.numberImg +=1
            print(Main.numberImg)
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка построения дерева"
        else:
            self.root.ids.notification.text = "Дерево построено"

    def startBuildTree(self):
        try:
            mapsKivy.main.buildGraf(tabReadyValues.replace("\n",' '),pathToValues,startingPosition,finalPosition, Main.numberImg)
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка в создании\nдерева"
        else:
            self.root.ids.notification.text = "Дерево построено"

    def getImgTree(self, imageTree):
        try:
            imageTree.source = "Karapetyan/dataImage/"+str(Main.numberImg)+".jpg"
        
        except BaseException:
            self.root.ids.notification.text = "Дерево не построено"
        else:
            self.root.ids.notification.text = "Дерево построено"

    def getLabelTime(self, time):
        try:
            time.text = "Время: " + str(mapsKivy.main.ShortPathLength())
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка построения дерева"
        else:
            self.root.ids.notification.text = "Дерево построено"
        
    def getTextTwoScreen(self):
        try:
            self.root.ids.startPosForTwoScreen.text = "Начальная точка: " + self.root.ids.startingPositionK.text
            self.root.ids.endPosForTwoScreen.text = "Конечная точка: " + self.root.ids.finalPositionK.text
        
        except BaseException:
            self.root.ids.notification.text = "Ошибка построения дерева"
        else:
            self.root.ids.notification.text = "Дерево построено"

    def build(self):
        Builder.load_file("digital.kv")
        return Digt()

Main().run()