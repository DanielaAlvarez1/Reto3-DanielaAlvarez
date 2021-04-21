﻿"""
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
    loadFeatures(cat, features)
    loadHashtags(cat, hashtags)
    loadSentiment(cat, sentiment)

def loadFeatures(cat, features):
    ffile = cf.data_dir + "subsamples-small" + "\\" + features
    print(ffile)
    input_file = csv.DictReader(open(ffile, encoding="utf-8"),
                                delimiter=",")
    a = True
    for rep in input_file:
        while a:
            model.addCategories(cat, rep)
            a = False
        add = model.addRep(cat, rep)
    return cat

def loadHashtags(cat, hashtags):
    pass
def loadSentiment(cat, sentiment):
    pass
# Funciones para consulta de datos del map
def repSize(arbol):
    return model.repSize(arbol)

def treeHeight(arbol):
    return model.treeHeight(arbol)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def caracterizarrep(cat, carac, minimo, maximo):
    return model.caracterizarrep(cat, carac, minimo, maximo)
