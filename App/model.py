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
import datetime
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

    cat['features'] = mp.newMap(17,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    cat['hashtags'] = om.newMap(omaptype='RBT',
                                    comparefunction=compareDates)
    cat['sentiment'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareValue)
    return cat
# Funciones para agregar informacion al catalogo
def addCategories(cat, rep):
    mapa = cat["features"]
    num_cat = 9
    for llave in rep:
        if num_cat > 0:
            mp.put(mapa, llave, om.newMap(omaptype='RBT',
                                      comparefunction=compareValue))
        else:
            break
        num_cat-=1

def addRep(cat, rep):
    mapa = cat["features"]
    num_cat = 9
    for llave in rep:
        if num_cat > 0:
            valor_cat = float(rep[llave])
            a = mp.get(mapa, llave)
            mapa_cat = me.getValue(a)
            info = {"artist_id": rep["artist_id"], "track_id": rep["track_id"], "created_at": rep["created_at"],
                    "energy": rep["energy"], "danceability": rep["danceability"], "tempo": rep["tempo"], 
                    "instrumentalness": rep["instrumentalness"]}
            if om.contains(mapa_cat, valor_cat):
                c = om.get(mapa_cat, valor_cat)
                lista_valor = me.getValue(c)
                lt.addLast(lista_valor, info)
            else:
                lista_valor = lt.newList(datastructure='SINGLE_LINKED')
                lt.addLast(lista_valor, info)
                om.put(mapa_cat, valor_cat, lista_valor)
        else:
            break
        num_cat-=1
    return cat

def addHashtag(cat, rep):
    mapa = cat["hashtags"]
    fecha = rep["created_at"]
    date = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    om.put(mapa, date, rep)

def addSentiment(cat, sent):
    mapa = cat["sentiment"]
    vader_avg = sent["vader_avg"]
    hashtag = sent["hashtag"]
    om.put(mapa, vader_avg, hashtag)

# Funciones para creacion de datos

# Funciones de consulta de datos del map
def repSize(arbol):
    return om.size(arbol)

def treeHeight(arbol):
    return om.height(arbol)

# Funciones de consulta
def caracterizarrep(cat, carac, minimo, maximo):
    mapa = cat["features"]
    a = mp.get(mapa, carac)
    m_carac = me.getValue(a)
    listareps = om.values(m_carac, minimo, maximo)
    arbol_artistas = om.newMap(omaptype='RBT',
                                      comparefunction=compareValue)
    eventos_escucha = 0

    for listas in lt.iterator(listareps):
        tamaño = lt.size(listas)
        eventos_escucha+=tamaño
        for reps in lt.iterator(listas):
            artista = reps["artist_id"]
            if om.contains(arbol_artistas, artista):
                c = om.get(arbol_artistas, artista)
                lista_artista = me.getValue(c)
                lt.addLast(lista_artista, reps)
            else:
                lista_artista = lt.newList(datastructure="SINGLE_LINKED")
                lt.addLast(lista_artista, reps)
                om.put(arbol_artistas, artista, lista_artista)

    artistas = om.size(arbol_artistas)
    return (eventos_escucha, artistas, arbol_artistas)

def musicafestejar(cat, minEnergy, maxEnergy, minDanceability, maxDanceability):
    mapa = cat["features"]
    a = mp.get(mapa, "energy")
    m_energy = me.getValue(a)
    lista_energy = om.values(m_energy, minEnergy, maxEnergy)
    lista_e = lt.newList(datastructure="ARRAY_LIST", cmpfunction= compareTracksids)
    for i in lt.iterator(lista_energy):
        for rep in lt.iterator(i):
            lt.addLast(lista_e, rep)
    b = mp.get(mapa, "danceability")
    m_danceability = me.getValue(b)
    lista_danceability = om.values(m_danceability, minDanceability, maxDanceability)
    lista_d = lt.newList(datastructure="ARRAY_LIST", cmpfunction= compareTracksids)
    for e in lt.iterator(lista_danceability):
        for rep in lt.iterator(e):
            lt.addLast(lista_d, rep)
    return musica(lista_e, lista_d)

def musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo):
    mapa = cat["features"]
    a = mp.get(mapa, "instrumentalness")
    m_instru = me.getValue(a)
    lista_instru = om.values(m_instru, minInstru, maxInstru)
    b = mp.get(mapa, "tempo")
    m_tempo = me.getValue(b)
    lista_tempo = om.values(m_tempo, minTempo, maxTempo)
    lista_t = lt.newList(datastructure="ARRAY_LIST")
    for e in lt.iterator(lista_tempo):
        for rep in lt.iterator(e):
            lt.addLast(lista_t, rep)
    return musica(lista_instru, lista_t)
    
def musica(lista1, lista2):
    arbol_pistas = om.newMap(omaptype='RBT',
                                      comparefunction=compareValue)
    lista_5_tracks = lt.newList(datastructure="ARRAY_LIST")

    n = 5
    for reps in lt.iterator(lista1):
        if lt.isPresent(lista2, reps) > 0:
            track_id = reps["track_id"]
            om.put(arbol_pistas, track_id, reps)
            while n>0:
                lt.addLast(lista_5_tracks, reps)
                print(".")
                n-= 1

    numero_tracks = om.size(arbol_pistas)
    return (numero_tracks, lista_5_tracks)

# Funciones utilizadas para comparar elementos dentro de una lista
def compareValue(val1, val2):
    if (val1 == val2):
        return 0
    elif (val1 > val2):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareTracksids(rep1, rep2):
    if (rep1["track_id"] == rep2["track_id"]):
        return 0
    elif (rep1["track_id"] > rep2["track_id"]):
        return 1
    else:
        return -1

# Funciones de ordenamiento