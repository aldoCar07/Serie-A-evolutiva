# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:20:53 2023
Title: Serie A calendario
@author: aldoe
"""
import pandas as pd
import random
import math

# Cargar datos de estadios y equipos desde el archivo CSV
estadios_df = pd.read_csv("estadios.csv")

# Función para calcular la distancia entre dos estadios (puedes usar la distancia Euclidiana)
def calcular_distancia(equipo1, equipo2):
    radio_tierra_km = 6371.0
    # Convertir latitudes y longitudes de grados a radianes
    #falta referenciar por equipo
    latitud1, longitud1= estadios_df[estadios_df['Team'] == equipo1][['Latitude', 'Longitude']].values[0]
    latitud2, longitud2= estadios_df[estadios_df['Team'] == equipo2][['Latitude', 'Longitude']].values[0]
    
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

# Generar un calendario de partidos aleatorio
def generar_calendario_aleatorio():
    # Implementa la lógica para generar un calendario aleatorio
    pass

# Define una función de aptitud para evaluar los calendarios
def evaluar_calendario(calendario):
    # Implementa la función de evaluación para evaluar el calendario de partidos
    # Vamos a evaluar de forma negativa si hay dos partidos en la misma ciudad en la misma jornada
    for jornada in calendario:  #para cada jornada del calendario se hará la evaluación
        ciudades = [] #agregamos las ciudades en las que se juegan los partidos de la jornada (al final debería haber 10 distintos)
        for partido in jornada['partidos']:
            ciudad_del_estadio = (estadios_df[estadios_df['Stadium'] == partido[2]]).head(1)['City'].values[1] #chorizo para sacar el string de la ciudad en la que se juega un partido de la jornada
            if(ciudad_del_estadio in ciudades): # si la ciudad ya está agregada, habrá al menos dos partidos en la misma ciudad, así que evaluamos con -1
                return -1
            else:
                ciudades.append(ciudad_del_estadio)
                
    # El siguiente criterio de evaluación es la distancia que hay entre estadios.
    # Procuraremos que la distancia recorrida de los equipos por jornada sea lo más equitativa posible.
    
    pass

# Función para cruzar dos calendarios
#Ejemplo de variable calendario:
    #calendario = [
    #    {"jornada": 1, "partidos": [["Equipo1", "Equipo2", "EstadioA"], ["Equipo3", "Equipo4", "EstadioB"]]},
    #    {"jornada": 2, "partidos": [["Equipo2", "Equipo3", "EstadioC"], ["Equipo4", "Equipo1", "EstadioD"]]}
    #]
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
        poblacion_evaluada.sort(key=lambda x: x[1], reverse=True)
        mejores_calendarios = [cal[0] for cal in poblacion_evaluada[:int(tamano_poblacion * 0.2)]]

        nueva_generacion = []

        # Cruzar y mutar para crear la nueva generación
        while len(nueva_generacion) < tamano_poblacion:
            padre1, padre2 = random.sample(mejores_calendarios, 2)
            hijo = cruzar_calendarios(padre1, padre2)
            hijo = mutar_calendario(hijo)
            nueva_generacion.append(hijo)

        poblacion = nueva_generacion

    # Devolver el mejor calendario encontrado
    mejor_calendario, mejor_aptitud = max(poblacion_evaluada, key=lambda x: x[1])
    return mejor_calendario, mejor_aptitud

# Ejecutar el algoritmo evolutivo
mejor_calendario, mejor_aptitud = algoritmo_evolutivo(num_generaciones=100, tamano_poblacion=50, tasa_cruce=0.8, tasa_mutacion=0.1)
print("Mejor calendario encontrado:")
print(mejor_calendario)
print("Aptitud del mejor calendario:", mejor_aptitud)

