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
    
    def ResumenContaminantePorEstacion(self):
        # Ejercicio 8
        dDescripcion = self.DataFrame.loc[:, ["MAGNITUD", "VALOR", "ESTACION"]]
        print(dDescripcion.groupby(["MAGNITUD", "ESTACION"]).describe())

    def validarMagnitud(self):
        #Validamos que el dato sea entero

        while True:

            try:
                magnitud= int(input("ingrese la magnitud: "))

                if magnitud != " ":
                    break

            except ValueError:
                print("debe ingresar numeros")

        return magnitud
    
    def validarEstacion(self):
        #validamos que el dato sea entero
        while True:

            try:  
                estacion = int(input("ingrese la estacion: "))
                if estacion != " ":
                    break

            except ValueError:
                print("debe ingresar numeros")
        
        return estacion
            
    def validarMes(self):
    
        while True:
            try:
                mes = int(input("Ingrese el mes que desea: "))

                if (mes >= 1) and (mes <= 12):

                    break

                else:
                    raise (MesInvalido)

            except MesInvalido:
                print("Error. El mes ingresado es inválido")
            
            except ValueError:
                print("Se esperaba el ingreso de un número ")
                
        return mes

    
    def filtrarPorEstacionYFecha(self, fecha1,fecha2):
        #PUNTO 9
        #creamos una funcion para filtrar por : Estación,magnitud y un rango de fechas ( desde: fecha1 , hasta: fecha2)
        estacion = self.validarEstacion()
        magnitud = self.validarMagnitud()

        if fecha1 < fecha2 :
            dfFiltradoPorEstacion = (self.DataFrame[(self.DataFrame["ESTACION"] == estacion) &\
                 (self.DataFrame["MAGNITUD"] == magnitud) & (self.DataFrame["FECHA"]>=fecha1) & (self.DataFrame["FECHA"]<= fecha2)])

            dfFiltradoPorEstacion.reset_index(drop=True, inplace=True)

            print(dfFiltradoPorEstacion)

        else:

            print("la segunda fecha no puede ser mayor a la primera")

    def filtrarValoresDeEstacion(self, estacion,magnitud):
        #PUNTO 10
        #Filtramos el DataFrame por la estación buscada y por la magnitud y convertimos a string las fechas para 
        #crear una nueva  columna llamada MES con los valores correspondientes a los meses 
        
        dfDeEstacionBuscada = (self.DataFrame[(self.DataFrame["ESTACION"] == estacion)& (self.DataFrame["MAGNITUD"] == magnitud)])


        dfDeEstacionBuscada["MES"] = self.DataFrame["FECHA"].dt.strftime("%m")

        return dfDeEstacionBuscada
    
    def calcularMediasMensuales(self):
        #PUNTO 10
        estacion = self.validarEstacion()
        magnitud = self.validarMagnitud()
        dfDeEstacionBuscada= self.filtrarValoresDeEstacion(estacion,magnitud)
        #Agrupamos por mes para que nos saque el valor
    
        dfMediasMensuales = dfDeEstacionBuscada.groupby("MES").mean()

        print(dfMediasMensuales)
    
    def agruparPorEstacion(self,mes,magnitud,df):
        #PUNTO 11

        newDF = (self.DataFrame[(self.DataFrame["MES"] == mes)& (self.DataFrame["MAGNITUD"] == magnitud)])
        newDF = newDF.loc[:,['MES', 'MAGNITUD', 'ESTACION', 'VALOR']]
        newDF.sort_values(['ESTACION'], inplace=True)
        newDF = newDF.groupby(['ESTACION']).mean()

        return newDF

    def createDictionary(self):
        #PUNTO 11

        mes = self.validarMes()
        magnitud= self.validarMagnitud()
        dfAgrupadoPorEstacion = self.agruparPorEstacion(mes, magnitud, self.DataFrame)
        print(dfAgrupadoPorEstacion)
        diccionario = {}
        for i in dfAgrupadoPorEstacion.index:   
            diccionario["Estacion: {}".format(i)] = "Media: {}".format(dfAgrupadoPorEstacion.loc[i, 'VALOR'])
        print(diccionario)

    def agruparPorEstacion(self,magnitud,df):
        #PUNTO 12

        newDF = self.DataFrame[(self.DataFrame['MAGNITUD']==magnitud)]
        newDF = newDF.loc[:,['MES', 'MAGNITUD', 'ESTACION', 'VALOR']]
        newDF.sort_values(['ESTACION'], inplace=True)
        newDF = newDF.groupby(['ESTACION', 'MES']).mean()
        return newDF
    
    def listaDeValores(self, df, estacion):
        return list(df.loc[estacion, 'VALOR'])

    def encontrarEstaciones(self, df, magnitud):
        listaEstaciones = []
        for i in df.index:
            listaEstaciones.append(i[0])
        return list(set(listaEstaciones))
    
    def generateGraphic(self):

        magnitud = self.validarMagnitud()

        newDF = self.agruparPorEstacion(magnitud, self.DataFrame)
        print(newDF)
        estaciones = self.encontrarEstaciones(newDF, magnitud)
        fig, ax = plt.subplots(figsize=(15,7.5))
        plt.title("Gráfico de medias mensuales para cada estación de la magnitud {}".format(magnitud))
        plt.xlabel("Meses")
        plt.ylabel("Media")
        meses = [1,2,3,4,5,6,7,8,9,10,11,12]
        
        for estacion in estaciones:
            valores = self.listaDeValores(newDF, estacion)
            ax.plot(meses, valores, label="Estacion {}".format(estacion))
            
        plt.legend()
        plt.show()
        


x = Emisiones()