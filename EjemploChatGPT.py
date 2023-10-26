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

# Inicialización de la población
def inicializar_poblacion(num_calendarios):
    poblacion = []
    for _ in range(num_calendarios):
        # Genera un calendario aleatorio
        calendario = generar_calendario_aleatorio()
        poblacion.append(calendario)
    return poblacion

# Función para calcular la distancia entre dos estadios (puedes usar la distancia Euclidiana)
def calcular_distancia(equipo1, equipo2):
    radio_tierra_km = 6371.0
    # Convertir latitudes y longitudes de grados a radianes
    #falta referenciar por equipo
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

# Define una función de aptitud para evaluar los calendarios
def evaluar_calendario(calendario):
    # Implementa la función de evaluación para evaluar el calendario de partidos
    pass

# Definir una función para cruzar dos calendarios
def cruzar_calendarios(calendario1, calendario2):
    # Implementa la lógica de cruce entre dos calendarios
    pass

# Definir una función para mutar un calendario
def mutar_calendario(calendario):
    # Implementa la lógica de mutación en un calendario
    pass

# Generar un calendario de partidos aleatorio
def generar_calendario_aleatorio():
    # Implementa la lógica para generar un calendario aleatorio
    pass

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

