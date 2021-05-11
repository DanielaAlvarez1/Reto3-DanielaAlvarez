"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import time
import tracemalloc
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    cat = model.initCatalog()
    return cat
# Funciones para la carga de datos
def loadData(cat, hashtags, features, sentiment):
    loadHashtags(cat, hashtags)
    loadFeatures(cat, features)
    loadSentiment(cat, sentiment)

def loadFeatures(cat, features):
    ffile = cf.data_dir + "subsamples-small" + "\\" + features
    input_file = csv.DictReader(open(ffile, encoding="utf-8"),
                                delimiter=",")
    a = True
    for rep in input_file:
        if a:
            model.addCategories(cat, rep)
            model.addGenre(cat)
            a = False
        add = model.addRep(cat, rep)
    print("Se cargó el archivo de Context-Features")
    return cat

def loadHashtags(cat, hashtags):
    hfile = cf.data_dir + "subsamples-small" + "\\" + hashtags
    input_file = csv.DictReader(open(hfile, encoding="utf-8"),
                                delimiter=",")
    for rep in input_file:
        model.addHashtag(cat, rep)
    print("Se cargó el archivo de Track-Hashtags")

def loadSentiment(cat, sentiment):
    sfile = cf.data_dir + "subsamples-small" + "\\" + sentiment
    input_file = csv.DictReader(open(sfile, encoding="utf-8"),
                                delimiter=",")
    for sent in input_file:
        model.addSentiment(cat, sent)
    print("Se cargó el archivo de Sentiment Values")

# Funciones para consulta de datos del map
def repSize(arbol):
    return model.repSize(arbol)

def treeHeight(arbol):
    return model.treeHeight(arbol)

# Funciones de medición de tiempo y memeoria 
def tiempomemoria(funcion):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    info = funcion

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory, info

def getTime():
    return float(time.perf_counter()*1000)


def getMemory():
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory = delta_memory/1024.0
    return delta_memory

# Funciones de consulta sobre el catálogo
def caracterizarrep(cat, carac, minimo, maximo):
    return tiempomemoria(model.caracterizarrep(cat, carac, minimo, maximo))

def musicafestejar(cat, minEnergy, maxEnergy, minDanceability, maxDanceability):
    return tiempomemoria(model.musicafestejar(cat, minEnergy, maxEnergy, minDanceability, maxDanceability))

def musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo):
    return tiempomemoria(model.musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo))

def generosmusicales(cat, listageneros):
    return tiempomemoria(model.generosmusicales(cat, listageneros))

def generotiempo(cat, hora_1, hora_2):
    return tiempomemoria(model.generotiempo(cat, hora_1, hora_2))