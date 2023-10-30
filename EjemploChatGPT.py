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
def generar_calendario_aleatorio(equipos):
    random.shuffle(equipos)
    
    if len(equipos) % 2 != 0: #Vemos que tengamos un número de equipos par o asignamos descanso a la lista
        equipos.append("Descanso")

    n = len(equipos) 
    mitad = n // 2 # definimos la mitad de los equipos

    jornadas = [] # creamos una lista vacía para ir agregando las jornadas
    for i in range(n - 1): # iteramos sobre el número de jornadas que se necesitan para que cada equipo juegue contra todos los demás
        mitad1 = equipos[:mitad] # definimos la primera mitad de los equipos
        mitad2 = equipos[mitad:] # definimos la segunda mitad de los equipos
        mitad2.reverse() # invertimos el orden de la segunda mitad para que los equipos no jueguen dos veces seguidas de local o visitante

        emparejamientos = list(zip(mitad1, mitad2)) # creamos una lista de tuplas con los emparejamientos de la jornada
        jornadas.append(emparejamientos)   # agregamos los emparejamientos a la lista de jornadas

        # rotamos los equipos en el sentido de las manecillas del reloj para que jueguen contra distintos rivales en la siguiente jornada
        equipos.insert(1, equipos.pop())
        # mezclamos los equipos para que no se repitan los emparejamientos en las siguientes jornadas
        # random.shuffle(equipos) no estoy muy segura si es un good addition 
    return jornadas # regresamos la lista de jornadas

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
                return 1
            else: # si la ciudad no está agregada, la agregamos
                ciudades.append(ciudad_del_estadio)
                
    # El siguiente criterio de evaluación es la distancia que hay entre estadios.
    # Procuraremos que la distancia recorrida de los visitantes por jornada sea lo más equitativa posible (minimizando la varianza de las distancias).
    var_jornadas = []
    for jornada in calendario:
        distancias = [] # para cada jornada sacaremos las distancias que recorren los visitantes de cada partido.
        for partido in jornada['partidos']:
            distancia = calcular_distancia(partido[0], partido[1])
            distancias.append(distancia)
        var_dist_jor = np.var(distancias) # sacamos la varianza del vector de distancias de la jornada
        var_jornadas.append(var_dist_jor)
        
    # queremos evaluar mejor al calendario que menor varianza promedio muestre.
    return -(np.mean(var_jornadas))

# Función para cruzar dos calendarios
#Ejemplo de variable calendario:
    calendario = [
        {"jornada": 1, "partidos": [["Equipo1", "Equipo2", "EstadioA"], ["Equipo3", "Equipo4", "EstadioB"]]},
        {"jornada": 2, "partidos": [["Equipo2", "Equipo3", "EstadioC"], ["Equipo4", "Equipo1", "EstadioD"]]}
    ]
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

#########################
#ejemplo calendario con equipos y estadios del csv
calendario = [
    {
        "jornada": 1,
        "partidos": [
            ["A.C Milan", "Bologna", "Stadio Diego Armando Maradona"],
            ["Inter de Milan", "Fiorentina", "Mapei Stadium"],
            ["Roma", "Juventus", "Olimpico di Roma"],
            ["Lazio", "Verona", "Carlo Castellani"],
            ["Napoli", "Sassuolo", "Atleti Azzurri d'Italia"],
            ["Salernitana", "Empoli", "Stadio Via del Mare"],
            ["Torino", "Atalanta", "Stadio Olimpico Grande Torino"],
            ["Udinese", "Sassuolo", "Stadio Friuli"],
            ["Genoa", "Lecce", "Luigi Ferraris"],
            ["Monza", "Cagliari", "Stadio Brianteo"]
        ]
    },
    {
        "jornada": 2,
        "partidos": [
            ["A.C Milan", "Inter de Milan", "San Siro Stadium"],
            ["Bologna", "Roma", "Stadio Renato Dall'Ara"],
            ["Fiorentina", "Lazio", "Artemio Franchi"],
            ["Juventus", "Napoli", "Allianz Stadium"],
            ["Verona", "Salernitana", "Marcantonio Bentegodi"],
            ["Empoli", "Torino", "Stadio Via del Mare"],
            ["Atalanta", "Udinese", "Atleti Azzurri d'Italia"],
            ["Sassuolo", "Genoa", "Mapei Stadium"],
            ["Lecce", "Monza", "Stadio Friuli"],
            ["Cagliari", "Frosinone", "Unipol Domus"]
        ]
    },
    {
        "jornada": 3,
        "partidos": [
            ["A.C Milan", "Bologna", "Stadio San Siro"],
            ["Inter de Milan", "Fiorentina", "Stadio Diego Armando Maradona"],
            ["Roma", "Juventus", "Stadio Olimpico"],
            ["Lazio", "Verona", "Stadio Bentegodi"],
            ["Napoli", "Sassuolo", "Carlo Castellani"],
            ["Salernitana", "Empoli", "Stadio Via del Mare"],
            ["Torino", "Atalanta", "Stadio Olimpico Grande Torino"],
            ["Udinese", "Sassuolo", "Stadio Friuli"],
            ["Genoa", "Lecce", "Stadio Luigi Ferraris"],
            ["Monza", "Cagliari", "Stadio Brianteo"]
        ]
    }
]


