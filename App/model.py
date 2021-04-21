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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    cat = {'features': None,
            'hashtags':None,
            'sentiment': None}

    cat['features'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    addCategories(cat['features'])
    cat['hashtags'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    cat['sentiment'] = mp.newMap(10000,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    return cat
# Funciones para agregar informacion al catalogo
def addCategories(map):
    mp.put(map, "instrumentalness", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "liveness", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "speechiness", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "danceability", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "valence", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "tempo", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "acousticness", lt.newList(datastructure= 'SINGLE_LINKED'))
    mp.put(map, "energy", lt.newList(datastructure= 'SINGLE_LINKED'))

def addRep(cat, rep):
    pass

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
