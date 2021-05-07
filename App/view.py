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
import datetime
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
        num = 1
        for tracks in lt.iterator(info[1]):
            track_id = tracks["track_id"]
            energy = tracks["energy"]
            dance = tracks["danceability"]
            print("Track {0}: {1} con energia de {2} y danceabilidad de {3}".format(num, track_id, energy, dance))
            num+=1

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
        num = 1
        for tracks in lt.iterator(info[1]):
            track_id = tracks["track_id"]
            instru = tracks["instrumentalness"]
            tempo = tracks["tempo"]
            print("Track {0}: {1} con energia de {2} y danceabilidad de {3}".format(num, track_id, instru, tempo))
            num+=1

    elif int(inputs[0]) == 6:
        print("\nA continuación se presenta una lista de géneros musicales: ")
        print("0. Crear genero")
        print("\n1. Reggae (Tempo típico de 60 a 90 BPM)")
        print("2. Down-Tempo (Tempo típico de 70 a 100 BPM)")
        print("3. Chill-Out (Tempo típico de 90 a 120 BPM)")
        print("4. Hip-Hop (Tempo típico de 85 a 115 BPM)")
        print("5. Jazz and Funk (Tempo típico de 120 a 125 BPM)")
        print("6. Pop (Tempo típico de 100 a 130 BPM)")
        print("7. R&B (Tempo típico de 60 a 80 BPM)")
        print("8. Rock (Tempo típico de 110 a 140 BPM)")
        print("9. Metal (Tempo típico de 100 a 160 BPM)")
        strgeneros = input("\nIndique los generos que desea consultar separados por coma (Ej: 2,3,4): ")
        generos = strgeneros.split(",")
        listainfo = []

        if "1" in generos:
            dic = {"nombre": "Reggae", "min_tempo": 60, "max_tempo": 90}
            listainfo.append(dic)
        if "2" in generos:
            dic = {"nombre": "Down-Tempo", "min_tempo": 70, "max_tempo": 100}
            listainfo.append(dic)
        if "3" in generos:
            dic = {"nombre": "Chill-Out", "min_tempo": 90, "max_tempo": 120}
            listainfo.append(dic)
        if "4" in generos:
            dic = {"nombre": "Hip-Hop", "min_tempo": 85, "max_tempo": 115}
            listainfo.append(dic)
        if "5" in generos:
            dic = {"nombre": "Jazz and Funk", "min_tempo": 120, "max_tempo": 125}
            listainfo.append(dic)
        if "6" in generos:
            dic = {"nombre": "Pop", "min_tempo": 100, "max_tempo": 130}
            listainfo.append(dic)
        if "7" in generos:
            dic = {"nombre": "R&B", "min_tempo": 60, "max_tempo": 80}
            listainfo.append(dic)
        if "8" in generos:
            dic = {"nombre": "Rock", "min_tempo": 110, "max_tempo": 140}
            listainfo.append(dic)
        if "9" in generos:
            dic = {"nombre": "Metal", "min_tempo": 100, "max_tempo": 160}
            listainfo.append(dic)
        if "0" in generos:
            nombre = input("Ingrese el nombre del genero que desea crear: ")
            min_tempo = float(input("Ingrese el valor mínimo de tempo que desea para este nuevo género: "))
            max_tempo = float(input("Ingrese el valor máximo de tempo que desea para este nuevo género: "))
            dic = {"nombre": nombre, "min_tempo": min_tempo, "max_tempo": max_tempo}

        info = controller.generosmusicales(cat, listainfo)
        escuchas = info[0]
        lista = info[1]
        print("Total de Reproducciones: " + str(escuchas))
        for i in lt.iterator(lista):
            print("\nPara {0} el tempo esta entre {1} y {2} BPM".format(i["nombre"], i["min_tempo"], i["max_tempo"]))
            print("Reproducciones para {0}: {1} con {2} artistas distintos".format(i["nombre"], i["escuchas"], i["artistas"]))
            print("Algunos artistas para {0}".format(i["nombre"]))
            n = 1
            for i in lt.iterator(i["id_artistas"]):
                print("Artista {0}: {1}".format(str(n), i))
                n+=1

    elif int(inputs[0]) == 7:
        h_1 = input("Ingrese el límite inferior del rango de horas que desea consultar en formato 24H (Ej. 23:00:00): ")
        h_2 = input("Ingrese el límite superior del rango de horas que desea consultar en formato 24H (Ej. 23:30:00): ")
        #h_1 = datetime.datetime.strptime(hora_1, '%H:%M:%S')
        #h_2 = datetime.datetime.strptime(hora_2, '%H:%M:%S')
        info = controller.generotiempo(cat, h_1, h_2)

    else:
        sys.exit(0)
sys.exit(0)
