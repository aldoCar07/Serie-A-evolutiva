# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:20:53 2023
Title: Serie A calendario
@author: aldoe
"""
import pandas as pd
import random
import math
import numpy as np

# Creamos dataframe de estadios desde cero
data = {
    'Team': ['A.C Milan', 'Inter de Milan', 'Roma', 'Lazio', 'Napoli', 'Fiorentina', 'Juventus', 'Verona', 'Bologna',
             'Genoa', 'Lecce', 'Salernitana', 'Torino', 'Udinese', 'Atalanta', 'Sassuolo', 'Empoli', 'Monza', 'Cagliari',
             'Frosinone'],
    'City': ['Milan', 'Milan', 'Roma', 'Roma', 'Napoli', 'Firenze', 'Torino', 'Verona', 'Bologna', 'Genova', 'Lecce',
             'Salerno', 'Torino', 'Udine', 'Bergamo', 'Reggio Emilia', 'Empoli', 'Monza', 'Cagliari', 'Frosinone'],
    'Stadium': [
        'San Siro Stadium', 'San Siro Stadium', 'Olimpico di Roma', 'Olimpico di Roma',
        'Stadio Diego Armando Maradona', 'Artemio Franchi', 'Allianz Stadium', 'Marcantonio Bentegodi',
        "Stadio Renato Dall'Ara", 'Luigi Ferraris', 'Stadio Via del Mare', 'Arechi',
        'Stadio Olimpico Grande Torino', 'Stadio Friuli', "Atleti Azzurri d'Italia", 'Mapei Stadium', 'Carlo Castellani',
        'Stadio Brianteo', 'Unipol Domus', 'Benito Stirpe'
    ],
    'Latitude': [45.478489, 45.478489, 41.933964, 41.933964, 40.827967, 43.7751569, 45.10566624, 45.43454493,
                 44.48871971, 44.40985669, 40.35916523, 40.64033077, 45.03838318, 46.07562803, 45.70533051, 44.7088305,
                 43.72249711, 45.57633103, 39.1998673, 41.633987],
    'Longitude': [9.12215, 9.12215, 12.454297, 12.454297, 14.193008, 11.27602056, 7.637997448, 10.96785113,
                  11.30579878, 8.951452861, 18.20533251, 14.82099672, 7.650005733, 13.20008087, 9.675163966, 10.64316409,
                  10.95299619, 9.304832114, 9.1383365, 13.322092]
}
estadios_df = pd.DataFrame(data) #este es el dataframe con toda la información

# Función para calcular la distancia entre dos estadios (puedes usar la distancia Euclidiana)
def calcular_distancia(equipo1, equipo2):
    radio_tierra_km = 6371.0
   
    # Convertir latitudes y longitudes de grados a radianes
    latitud1, longitud1= estadios_df[estadios_df['Team'] == equipo1][['Latitude', 'Longitude']].values[0]
    latitud2, longitud2= estadios_df[estadios_df['Team'] == equipo2][['Latitude', 'Longitude']].values[0]
   
    #Convertimos a radianes porqué así va la formula
    latitud1 = math.radians(latitud1)
    longitud1 = math.radians(longitud1)
    latitud2 = math.radians(latitud2)
    longitud2 = math.radians(longitud2)

    # Diferencia entre las latitudes y longitudes
    diferencia_latitud = latitud2 - latitud1
    diferencia_longitud = longitud2 - longitud1

    # Fórmula de la distancia haversine
    a = math.sin(diferencia_latitud / 2)**2 + math.cos(latitud1) * math.cos(latitud2) * math.sin(diferencia_longitud / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calcular la distancia
    distancia = radio_tierra_km * c

    return distancia

# Inicialización de la población
def inicializar_poblacion(num_calendarios):
    poblacion = []
    for _ in range(num_calendarios):
        # Genera un calendario aleatorio
        calendario = generar_calendario_aleatorio()
        poblacion.append(calendario)
    return poblacion

# Generar jornadas de partidos de ida
#Nota: Usar un dataframe auxiliar cómo se muestra a continuación, NO el original
# selected_columns = ['Team', 'City', 'Stadium']
#df_aux = df[selected_columns]
#generar_jornadas(df_aux)
def generar_jornadas(dataframe):
    # Crear una copia del DataFrame para trabajar con ella
    df = dataframe.copy()

    # Crear un DataFrame para almacenar las jornadas
    jornadas = pd.DataFrame(columns=['Jornada', 'Equipo Local', 'Equipo Visitante', 'Estadio'])

    estadios = list(df['Stadium'])
    
    # Iterar a través de las jornadas #ponerle 20 para que salgan 19 jornadas
    for jornada in range(1, 20):
        # Barajar los equipos
        df = df.sample(frac=1)

        # Iterar a través de los partidos de la jornada
        for i in range(0, 20, 2):
            equipo_local = df.iloc[i]['Team']
            equipo_visitante = df.iloc[i + 1]['Team']
            
            estadio=''#esto solo es para ponerlo en vacio
            
            new_row={'Jornada': jornada, 'Equipo Local': equipo_local, 'Equipo Visitante': equipo_visitante, 'Estadio': estadio}

            jornadas = pd.concat([jornadas, pd.DataFrame([new_row])], ignore_index=True)
            
        # Este for itera sobre cada fila del dataframe y le pone el nombre del estadio del equipo local
    for index, row in jornadas.iterrows():
        target_name = row['Equipo Local']
        nuevo_estadio = df.loc[df['Team'] == target_name, 'Stadium'].values[0]
        jornadas.at[index,'Estadio']=nuevo_estadio

    return jornadas

#Generar jornadas de partidos de vuelta
#Nota: Importante usar una COPIA del método anterior cómo primer parámetro
# Ejemplo: jornadas_generadas= generar_jornadas(estadios_df)
# df_copia = jornadas_generadas.copy()
# jornadas_generadas2= jornadas_vuelta(df_copia, df_aux)
def jornadas_vuelta(df,df_original):
    #aquí volteas los valores de local y visitante del dataframe anterior
    temp_values = df['Equipo Local'].copy() 
    df['Equipo Local'] = df['Equipo Visitante'] 
    df['Equipo Visitante'] = temp_values
    
    # Itera sobre cada fila del dataframe
    for index, row in df.iterrows():
        target_name = row['Equipo Local']
        nuevo_estadio = df_original.loc[df_original['Team'] == target_name, 'Stadium'].values[0]
        df.at[index,'Estadio']=nuevo_estadio
        
        new_jornada=row['Jornada']+19
        df.at[index,'Jornada']=new_jornada
    
    return df

#a estos método de ida y vuelta faltan los auxiliares que concatenan y resetean el indice
# Concatena ida y vuelta
#result_vertical = pd.concat([jornadas_generadas, jornadas_generadas2], axis=0)
# Resetea el indice
#df_final = result_vertical.reset_index(drop=True)
#df_final es el dataframe con las 2 jornadas pegadas

#este método pasa de dataframe a una lista de diccionarios
def transformador(df):
    calendario_transformed = []

    for jornada, group in df.groupby('Jornada'):
        partidos = []
        for _, row in group.iterrows():
            partido = [row['Equipo Local'], row['Equipo Visitante'], row['Estadio']]
            partidos.append(partido)

        jornada_dict = {'jornada': jornada, 'partidos': partidos}
        calendario_transformed.append(jornada_dict)

    return calendario_transformed 

def imprimir_calendario(jornadas): # función para imprimir el calendario
    for i, jornada in enumerate(jornadas, start=1): # iteramos sobre las jornadas
        print("\n"+f"Jornada {i}:") # imprimimos el número de jornada
        for partido in jornada: # iteramos sobre los partidos de la jornada
            equipo_local, equipo_visitante = partido # un partido es una tupla con dos equipos, aquí los asignamos a dos variables
            if "Descanso" in partido: # si hay un descanso, imprimimos que hay descanso
                print(f"Descanso")
            else: # si no hay descanso, imprimimos el partido
                print(f"{equipo_local} vs {equipo_visitante}")


# Define una función de aptitud para evaluar los calendarios, entre menor sea el valor de aptitud, mejor es el calendario
def evaluar_calendario(calendario):
    # Implementa la función de evaluación para evaluar el calendario de partidos
    # Vamos a evaluar de forma negativa si hay dos partidos en la misma ciudad en la misma jornada
    for jornada in calendario:  #para cada jornada del calendario se hará la evaluación
        ciudades = [] #agregamos las ciudades en las que se juegan los partidos de la jornada (al final debería haber 10 distintos)
        for partido in jornada['partidos']:
            ciudad_del_estadio = (estadios_df[estadios_df['Stadium'] == partido[2]]).head(1)['City'].values[0] #chorizo para sacar el string de la ciudad en la que se juega un partido de la jornada
            if(ciudad_del_estadio in ciudades): # si la ciudad ya está agregada, habrá al menos dos partidos en la misma ciudad, así que evaluamos con 1
                return -1000
            else: # si la ciudad no está agregada, la agregamos
                ciudades.append(ciudad_del_estadio)
                
    # El siguiente criterio de evaluación es la distancia que hay entre estadios.
    # Procuraremos que la distancia recorrida de los visitantes por jornada sea lo más equitativa posible (minimizando la varianza de las distancias).
    std_jornadas = []
    for jornada in calendario:
        distancias = [] # para cada jornada sacaremos las distancias que recorren los visitantes de cada partido.
        for partido in jornada['partidos']:
            distancia = calcular_distancia(partido[0], partido[1])
            distancias.append(distancia)
        std_dist_jor = np.std(distancias) # sacamos la varianza del vector de distancias de la jornada
        std_jornadas.append(std_dist_jor)
        
    # queremos evaluar mejor al calendario que menor varianza promedio muestre.
    return -(np.mean(std_jornadas))



# Función para cruzar dos calendarios    
def cruzar_calendarios(calendario1, calendario2):
    # Crear un calendario vacío 
    nuevo_calendario = []
    # Puntos de cruce
    punto_de_cruce = len(calendario1) // 2
    # Tomar la primera mitad del calendario1
    nuevo_calendario.extend(calendario1[:punto_de_cruce])
    # Tomar la segunda mitad del calendario2
    nuevo_calendario.extend(calendario2[punto_de_cruce:])
    return nuevo_calendario

# Definir una función para mutar un calendario
#Recibe un arreglo con el calendario y un valor numérico con la probabilidad de mutación 
def mutar_calendario(calendario, probabilidad_mutacion):
    for jornada in calendario:
        #factor aleatorio que decide si se muta o no
        if random.random() < probabilidad_mutacion:
            # Realizar una mutación en la jornada
            # Por ejemplo, intercambiar dos partidos de lugar en la misma jornada
            # podríamos meterle otras mutaciones además de estas
            num_partidos = len(jornada["partidos"])
            if num_partidos >= 2: #esa condición solo para asegurarse de haber metido una jornada con más de dos partidos
                idx1, idx2 = random.sample(range(num_partidos), 2) #agarras dos partidos 
                jornada["partidos"][idx1], jornada["partidos"][idx2] = jornada["partidos"][idx2], jornada["partidos"][idx1]

# Algoritmo evolutivo
def algoritmo_evolutivo(num_generaciones, tamano_poblacion, tasa_cruce, tasa_mutacion):
    poblacion = inicializar_poblacion(tamano_poblacion)

    for generacion in range(num_generaciones):
        # Evaluar la aptitud de la población actual
        poblacion_evaluada = [(calendario, evaluar_calendario(calendario)) for calendario in poblacion]

        # Seleccionar a los mejores calendarios
        poblacion_evaluada.sort(key=lambda x: x[1], reverse=False)
        mejores_calendarios = [cal[0] for cal in poblacion_evaluada[:int(tamano_poblacion * 0.2)]] #elegir el mejor 20% de los calendarios

        nueva_generacion = []

        # Cruzar y mutar para crear la nueva generación
        while len(nueva_generacion) < tamano_poblacion:
            padre1, padre2 = random.sample(mejores_calendarios, 2)
            hijo = cruzar_calendarios(padre1, padre2)
            hijo = mutar_calendario(hijo, tasa_mutacion)
            nueva_generacion.append(hijo)

        poblacion = nueva_generacion

    # Devolver el mejor calendario encontrado
    poblacion_evaluada = [(calendario, evaluar_calendario(calendario)) for calendario in poblacion]
    mejor_calendario, mejor_aptitud = max(poblacion_evaluada, key=lambda x: x[1])
    
    return mejor_calendario, mejor_aptitud

# Ejecutar el algoritmo evolutivo
mejor_calendario, mejor_aptitud = algoritmo_evolutivo(num_generaciones=100, tamano_poblacion=50, tasa_cruce=0.8, tasa_mutacion=0.1)
print("Mejor calendario encontrado:")
print(mejor_calendario)
print("Aptitud del mejor calendario:", mejor_aptitud)

#################33
#####################3
#######################3
#######################33
#CALENDARIO DE PRUEBA CON ESTADIOS REALES
calendario = [
    {
        "jornada": 1,
        "partidos": [
            ["A.C Milan", "Inter de Milan", "San Siro Stadium"],
            ["Roma", "Lazio", "Olimpico di Roma"],
            ["Napoli", "Fiorentina", "Stadio Diego Armando Maradona"],
            ["Juventus", "Verona", "Allianz Stadium"],
            ["Bologna", "Genoa", "Stadio Renato Dall'Ara"],
            ["Lecce", "Salernitana", "Arechi"],
            ["Udinese", "Torino", "Stadio Friuli"],
            ["Atalanta", "Sassuolo", "Atleti Azzurri d'Italia"],
            ["Empoli", "Monza", "Carlo Castellani"],
            ["Cagliari", "Frosinone", "Unipol Domus"]
        ]
    },
    {
        "jornada": 2,
        "partidos": [
            ["A.C Milan", "Roma", "Stadio Diego Armando Maradona"],
            ["Inter de Milan", "Lazio", "Artemio Franchi"],
            ["Napoli", "Juventus", "Allianz Stadium"],
            ["Fiorentina", "Verona", "Marcantonio Bentegodi"],
            ["Bologna", "Genoa", "Luigi Ferraris"],
            ["Lecce", "Salernitana", "Stadio Via del Mare"],
            ["Udinese", "Torino", "Stadio Friuli"],
            ["Atalanta", "Sassuolo", "Mapei Stadium"],
            ["Empoli", "Monza", "Stadio Brianteo"],
            ["Cagliari", "Frosinone", "Benito Stirpe"]
        ]
    },
    {
        "jornada": 3,
        "partidos": [
            ["A.C Milan", "Napoli", "San Siro Stadium"],
            ["Inter de Milan", "Fiorentina", "Olimpico di Roma"],
            ["Roma", "Juventus", "Stadio Diego Armando Maradona"],
            ["Lazio", "Verona", "Allianz Stadium"],
            ["Bologna", "Genoa", "Stadio Renato Dall'Ara"],
            ["Lecce", "Salernitana", "Arechi"],
            ["Udinese", "Torino", "Stadio Friuli"],
            ["Atalanta", "Sassuolo", "Atleti Azzurri d'Italia"],
            ["Empoli", "Monza", "Carlo Castellani"],
            ["Cagliari", "Frosinone", "Unipol Domus"]
        ]
    }
]




