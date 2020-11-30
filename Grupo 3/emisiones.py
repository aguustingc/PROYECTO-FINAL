import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# En codigos.py estan las listas y diccionarios que usamos en el Notebook.
import codigos

class Emisiones(object):
    
    def __init__(self):
        self.DataFrame = self.generarDataFrame()


    def generarDataFrame(self):
        # Ejercicio 1

        df_2016 = pd.read_csv('DataFrames/emisiones-2016.csv', sep=';')
        df_2017 = pd.read_csv('DataFrames/emisiones-2017.csv', sep=';')
        df_2018 = pd.read_csv('DataFrames/emisiones-2018.csv', sep=';')
        df_2019 = pd.read_csv('DataFrames/emisiones-2019.csv', sep=';')

        dfs = [df_2016,
               df_2017,
               df_2018,
               df_2019]

        dfPrincipal = pd.concat(dfs, ignore_index=True)

        # Ejercicio 2

        dfFiltrado = dfPrincipal.loc[:,
                                     codigos.dias + codigos.columnasFiltradas]
        

        # Ejercicio 3

        dfValuesPerDay = dfFiltrado.melt(id_vars = codigos.columnasNecesarias, 
                                         value_vars=codigos.dias, var_name='DIA',
                                         value_name = 'VALOR')

        # Ejercicio 4

        dfValuesPerDay.replace(codigos.conversionDic, inplace=True)

        fechas = pd.DataFrame([dfValuesPerDay['ANO'],
                               dfValuesPerDay['MES'],
                               dfValuesPerDay['DIA']]).T
        fechas.rename(columns={'ANO':'year', 'MES':'month', 'DIA':'day'}, inplace=True)
        fechas = pd.to_datetime(fechas, format='%d-%m-%Y', errors='coerce')
        dfValuesPerDay['FECHA'] = fechas

        # Ejericio 5

        # Se agregan columnas ANO, MES y DIA para las funciones del 8 a 12

        dfDate = dfValuesPerDay.dropna()
        dfDate = dfDate.sort_values(["ESTACION", "MAGNITUD", "FECHA", "VALOR"], ascending=True)
        dfDate = dfDate.loc[:, ["ESTACION",
                                "MAGNITUD",
                                "FECHA",
                                "ANO",
                                "MES",
                                "DIA",
                                "PROVINCIA", 
                                "MUNICIPIO", 
                                "PUNTO_MUESTREO", 
                                "VALOR"]]

        dfDate = dfDate.reset_index(drop=True)

        return dfDate


    def mostrarEstacionesDisponibles(self):
        # Ejercicio 6

        listaNumeros = []
        for i in range(0, len(self.DataFrame)):
            # Columna ESTACION: 0
            listaNumeros.append(self.DataFrame.iloc[i, 0])

        listaNombres = []
        for i in range(0, len(listaNumeros)):
            listaNombres.append(codigos.estaciones[listaNumeros[i]])
        
        listaNombresActualizada = list(dict.fromkeys(listaNombres))

        print('Estaciones disponibles: ')
        for estacion in listaNombresActualizada:
            print('\t-', estacion)


    def mostartMagnitudesDisponibles(self):
        # Ejericio 6
        
        listaNumeros = []
        for i in range(0, len(self.DataFrame)):
            # Columna MAGNITUD: 1
            listaNumeros.append(self.DataFrame.iloc[i, 1])

        listaNombres = []
        for i in range(0, len(listaNumeros)):
            listaNombres.append(codigos.contaminantes[listaNumeros[i]])
        
        listaNombresActualizada = list(dict.fromkeys(listaNombres))

        print('Estaciones disponibles: ')
        for estacion in listaNombresActualizada:
            print('\t-', estacion)


    def mostrarResumenContaminante(self):
        # Ejercicio 7
        dDescripcion = self.DataFrame.loc[:, ["MAGNITUD", "VALOR"]]
        print(dDescripcion.groupby("MAGNITUD").describe())

    def ResumenContaminantePorEstacion(self):
        # Ejercicio 8
        dDescripcion = self.DataFrame.loc[:, ["MAGNITUD", "VALOR", "ESTACION"]]
        print(dDescripcion.groupby(["MAGNITUD", "ESTACION"]).describe())

    def mediaMensualPorAño(self, contaminante, año): #PUNTO 9

        dfMedia = self.DataFrame.loc[:, ["MAGNITUD","ESTACION","MES","ANO","VALOR"]] 

        return dfMedia[(dfMedia["MAGNITUD"] == contaminante) & (dfMedia["ANO"] == año)].groupby(["MAGNITUD","ESTACION","ANO","MES"]).agg({"VALOR":"mean"}) 

    
    def obtenerDiccionarioMediasMensuales(self, mes, estacion):  #PUNTO 10

        dfDiccionario = self.DataFrame.loc[:, ["MAGNITUD","ESTACION","MES","VALOR"]] 
        diccionarioMediaPorMagnitud = {}

        dfValores = dfDiccionario[(dfDiccionario["ESTACION"] == estacion) & (dfDiccionario["MES"] == mes)].groupby(["MAGNITUD","ESTACION","MES"]).agg({"VALOR":"mean"})
        dfMagnitudes = dfDiccionario[(dfDiccionario["ESTACION"] == estacion) & (dfDiccionario["MES"] == mes)].groupby(["MAGNITUD","ESTACION","MES"]).agg({"MAGNITUD":"max"})
    
        medias = dfValores["VALOR"].to_list() 
        magnitudes = dfMagnitudes["MAGNITUD"].to_list() 
        
        for i in range(0, len(medias)):
            diccionarioMediaPorMagnitud[magnitudes[i]] = medias[i]
        
        return diccionarioMediaPorMagnitud 


    def evolucionMagnitud(self, fechaInicio, fechaFinal, magnitud): #PUNTO 11

        dfFecha = self.DataFrame.loc[(self.DataFrame["FECHA"] >= fechaInicio) & (self.DataFrame["FECHA"] <= fechaFinal) & (self.DataFrame['MAGNITUD']==magnitud), ['FECHA', 'VALOR']]  
        
        fig, ax=plt.subplots()  
        dfFecha.plot(kind= 'line', x='FECHA', y= 'VALOR', ax=ax)   
        plt.show()


    def graficoMediasMensualesCentrales(self,magnitud): #PUNTO 12(1/2)

        listaCentrales = [35,38,11,15,47,48,49,50,60] 

        dfCentrales = self.DataFrame.loc[(self.DataFrame['ESTACION'].isin(listaCentrales)), ["MAGNITUD","MES","VALOR"]] 

        dfCalculoMediasCentrales = dfCentrales[(dfCentrales["MAGNITUD"] == magnitud)].groupby(["MES"]).mean().reset_index() 
 
        fig, ax = plt.subplots()  
        dfCalculoMediasCentrales.plot(kind= 'line', x= 'MES', y= 'VALOR', ax=ax)   
        plt.show()
    

    def graficoMediasMensualesNoCentrales(self, magnitud): #PUNTO 12(2/2)

        listaNoCentrales = [1,2,4,39,6,7,8,9,12,40,14,16,17,18,19,36,21,22,23,24,25,26,27,54,55,56,57,58,59] 
        
        dfNoCentrales = self.DataFrame.loc[(self.DataFrame['ESTACION'].isin(listaNoCentrales)), ["MAGNITUD","MES","VALOR"]] 
        
        dfCalculoMediasNoCentrales = dfNoCentrales[(dfNoCentrales["MAGNITUD"] == 1)].groupby(["MES"]).mean().reset_index()

        fig, ax = plt.subplots()  
        dfCalculoMediasNoCentrales.plot(kind= 'line', x= 'MES', y= 'VALOR', ax=ax)
        plt.show()



x = Emisiones()