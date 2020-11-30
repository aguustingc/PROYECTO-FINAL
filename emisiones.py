import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from datetime import datetime
# En codigos.py estan las listas y diccionarios que usamos en el Notebook.
import codigos

# Tamaño a la figura
rcParams['figure.figsize'] = 15, 7

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
    
    
    '''
    GRUPO 1
    '''
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




    '''
    GRUPO 2
    '''
    def ContaminantePorEstacion(self,estacion, contaminante):
        # Ejercicio 9
        dDescripcion = self.DataFrame.loc[:, ["ESTACION","MAGNITUD","VALOR"]]
        df9=dDescripcion.loc[(dDescripcion["ESTACION"]==estacion) & (dDescripcion["MAGNITUD"]==contaminante),:]
        print("Estación:", codigos.estaciones[estacion])
        print("Contaminante:", codigos.contaminantes[contaminante])
        print(df9["VALOR"].describe())

    def ListaValoresPorEstacion(self,estacion, contaminante):
        # Ejercicio 10
        dDescripcion = self.DataFrame.loc[:, ["ESTACION","MAGNITUD", "VALOR"]]
        df10=dDescripcion.loc[(dDescripcion["ESTACION"]==estacion) & (dDescripcion["MAGNITUD"]==contaminante), :]
        print("Estación:", codigos.estaciones[estacion])
        print("Contaminante:", codigos.contaminantes[contaminante])
        print(df10["VALOR"].to_list())
    

    def SerieTiempoEstacion(self,estacion, fecha_inicio, fecha_final):
        #Ejercicio 11

        # 1. Filtrar el DataFrame por el rango de fechas
    
        inicio = datetime.strptime(fecha_inicio , '%d/%m/%Y')
        final = datetime.strptime(fecha_final , '%d/%m/%Y')
        df10 = self.DataFrame.loc[(self.DataFrame["ESTACION"]==estacion) &\
                       (self.DataFrame["FECHA"]>=inicio) &\
                       (self.DataFrame["FECHA"]<=final), :]
    
        # 2. Guardar las magnitudes UNICAS que habian en el 
        # rango de fechas del DataFrame
        magnitudes = df10["MAGNITUD"].drop_duplicates().to_list()
    
        # 3. Filtrar por Magnitudes y guardar DFs en una lista.
        dfs_magnitudes = []
        for magnitud in magnitudes:
            filtro = df10.loc[df10["MAGNITUD"] == magnitud, :]
            filtro.reset_index(inplace=True)
            dfs_magnitudes.append(filtro)

        # 4. Plotear DataFrames en un mismo grafico.
        fig, ax = plt.subplots()
        plt.xticks(rotation=90)
        for df in dfs_magnitudes:
            ax.plot(df["FECHA"], df["VALOR"], label=codigos.contaminantes[df["MAGNITUD"][0]])
        plt.legend()    
        return plt.show()           

    def obtenerDiccionarioDeMagnitud(self,mes, magnitud):
        # Ejercicio 12
        estacionesCentrales = {35: "Plaza del Carmen",38: "Cuatro caminos",
        11: "Av. Ramon y Cajal", 15: "Pza. Castilla", 47: "Mendez Alvaro", 48: "P°. Castellana",
        49: "Retiro", 50: "Pza. Castilla", 60: "Tres Olivos"} 

        estacionesNoCentrales = { 1: "P. Recoletos", 2: "Glta. de Carlos V", 4: "Pza. de España", 39: "Barrio del pilar",
        6: "Pza. Dr. Marañon", 7: "Pza. M. de Salamanca", 8: "Escuelas aguirre", 9: "Pza. Luca de Tena", 12: "Pza. Manuel Becerra", 40: "Vallecas", 14: "Pza. Fdez. Ladreda", 16: "Arturo Soria", 17: "Villaverde Alto", 18: "Calle Farolito", 19: "Huerta Castañeda", 36: "Morataz", 21: "Pza. Cristo Rey", 22: "P°. Fontones", 23: "Final C/ Alcala", 24: "Casa de campo", 25: "Santa Eugenia", 26: "Urb. Embajada (Barajas)", 27: "Barajas", 54: "Ensanche Vallecas", 55: "Urb. Embajada (Barajas)", 56: "Plaza Eliptica", 57: "Sanchincharro", 58: "El Pardo", 59: "Parque Juan Carlos 1°"}
 

        dFinal = {"CENTRALES":{},"NO_CENTRALES":{}}
        # Diccionario compuesto vacío

        # 1. Filtra DataFrame por mes y magnitud
        df12 = self.DataFrame.loc[(self.DataFrame["MES"]==mes) & (self.DataFrame["MAGNITUD"]==magnitud), ["ESTACION","VALOR"]]

        # 2. Calculo la media de los valores de dicha magnitud en dicho mes
        df12 = df12.groupby("ESTACION").mean()
        d = df12.to_dict()["VALOR"]

        # 3. De pertenecer a una de las dos calificaciones(Centrales, No Centrales), 
        # lo guardo en el sub-diccionario correspondiente
        for k, v in d.items():
            if k in estacionesCentrales:
                dFinal["CENTRALES"][k] = v
            elif k in estacionesNoCentrales: 
                dFinal["NO_CENTRALES"][k] = v

        print(dFinal)


    '''
    GRUPO 3
    '''
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