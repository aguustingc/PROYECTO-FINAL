import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# En codigos.py estan las listas y diccionarios que usamos en el Notebook.
import codigos

class Emisiones(object):
    
    def __init__(self):
        self.DataFrame = self.GenerarDataFrame()


    def GenerarDataFrame(self):
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


    def EstacionesDisponibles(self):
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


    def MagnitudesDisponibles(self):
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


    def ResumenContaminante(self):
        # Ejercicio 7
        dDescripcion = self.DataFrame.loc[:, ["MAGNITUD", "VALOR"]]
        print(dDescripcion.groupby("MAGNITUD").describe())


x = Emisiones()