"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

hashtags = "user_track_hashtag_timestamp-small.csv"
features = "context_content_features-small.csv"
sentiment = "sentiment_values.csv"
cat = None

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Crear Catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Caracterizar las reproducciones")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")
    print("7- Indicar el género musical mas escuchado en el tiempo")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cat = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("\nCargando información ....")
        controller.loadData(cat, hashtags, features, sentiment)

    elif int(inputs[0]) == 3:
        carac = input("Ingrese la característica de contenido que desea consultar: ").lower().replace(" ","")
        minimo = float(input("Ingrese el valor mínimo de característica: "))
        maximo = float(input("Ingrese el valor máximo de característica: "))
        info = controller.caracterizarrep(cat, carac, minimo, maximo)
        print("\nLa característica {0} estuvo entre {1} y {2} para: ".format(carac, minimo, maximo))
        print("\nTotal de Reproducciones: " + str(info[0]))
        print("Artistas Únicos: " + str(info[1]))
        print("\nPara resolver este requerimiento, se creó un RBT donde las llaves fueron los artistas\
 y los valores fueron los eventos de escucha.")
        print("\nLa información de dicho arbol se presenta a continuación:")
        print('Elementos cargados: ' + str(controller.repSize(info[2])))
        print('Altura del arbol: ' + str(controller.treeHeight(info[2])))

    elif int(inputs[0]) == 4:
        minEnergy = float(input("Ingrese el valor mínimo de Energy que desea en las pistas: "))
        maxEnergy = float(input("Ingrese el valor máximo de Energy que desea en las pistas: "))
        minDanceability = float(input("Ingrese el valor mínimo de Danceability que desea en las pistas: "))
        maxDanceability = float(input("Ingrese el valor máximo de Danceability que desea en las pistas: "))
        info = controller.musicafestejar(cat, minEnergy, maxEnergy, minDanceability, maxDanceability)
        print("\nEnergy estuvo entre {0} y {1}".format(minEnergy, maxEnergy))
        print("Danceability estuvo entre {0} y {1}".format(minDanceability, maxDanceability))
        print("Total de pistas únicas en eventos: " + str(info[0]))
        print("\nUnique tracks")
        num = 5
        for tracks in lt.iterator(info[1]):
            track_id = tracks["track_id"]
            energy = tracks["energy"]
            dance = track["danceability"]
            print("Track {0}: {1} con energia de {2} y danceabilidad de {3}".format(num, track_id, energy, dance))
            num-=1

    elif int(inputs[0]) == 5:
        minInstru = float(input("Ingrese el valor mínimo de Instrumentalness que desea en las pistas: "))
        maxInstru = float(input("Ingrese el valor máximo de Instrumentalness que desea en las pistas: "))
        minTempo = float(input("Ingrese el valor mínimo de Tempo que desea en las pistas: "))
        maxTempo = float(input("Ingrese el valor máximo de Tempo que desea en las pistas: "))
        info = controller.musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo)
        print("\nInstrumentalness estuvo entre {0} y {1}".format(minInstru, maxInstru))
        print("Tempo estuvo entre {0} y {1}".format(minTempo, maxTempo))
        print("Total de pistas únicas en eventos: " + str(info[0]))
        print("\nUnique tracks")
        num = 5
        for tracks in lt.iterator(info[1]):
            track_id = tracks["track_id"]
            instru = tracks["instrumentalness"]
            tempo = track["tempo"]
            print("Track {0}: {1} con energia de {2} y danceabilidad de {3}".format(num, track_id, instru, tempo))
            num-=1
    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
