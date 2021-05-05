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
import random
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
            if llave == "energy":
                mp.put(mapa, "energy-dance", om.newMap(omaptype='RBT',
                                      comparefunction=compareValue))
            elif llave == "tempo":
                mp.put(mapa, "tempo-instru", om.newMap(omaptype='RBT',
                                      comparefunction=compareValue))
            else:
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
            info = {"artist_id": rep["artist_id"], "track_id": rep["track_id"], "created_at": rep["created_at"],
                    llave: rep[llave]}
            if llave == "energy":
                valor_e = float(rep["energy"])
                valor_d = float(rep["danceability"])
                a = mp.get(mapa, "energy-dance")
                mapa_cat = me.getValue(a)
                info["danceability"] = valor_d
                mapa_valor_e = addInternalMap(mapa_cat, info, valor_e, valor_d)
                om.put(mapa_cat, valor_e, mapa_valor_e)

            elif llave == "tempo":
                valor_t = float(rep["tempo"])
                valor_i = float(rep["instrumentalness"])
                a = mp.get(mapa, "tempo-instru")
                mapa_cat = me.getValue(a)
                info["instrumentalness"] = valor_i
                mapa_valor_t = addInternalMap(mapa_cat, info, valor_t, valor_i)
                om.put(mapa_cat, valor_t, mapa_valor_t)
            else:
                valor_cat = float(rep[llave])
                a = mp.get(mapa, llave)
                mapa_cat = me.getValue(a)
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
def addInternalMap(mapa, info, out_value, in_value):
    if om.contains(mapa, out_value):
        c = om.get(mapa, out_value)
        mapa_out_value = me.getValue(c)
        if om.contains(mapa_out_value, in_value):
            d = om.get(mapa_out_value, in_value)
            lista_valor = me.getValue(d)
            lt.addLast(lista_valor, info)
        else:
            lista_valor = lt.newList(datastructure= "SINGLE_LINKED")
            lt.addLast(lista_valor, info)
            om.put(mapa_out_value, in_value, lista_valor)
    else:
        mapa_out_value = om.newMap(omaptype='RBT',
                                    comparefunction=compareValue)
    return mapa_out_value

# Funciones de consulta de datos del map
def repSize(arbol):
    return om.size(arbol)

def treeHeight(arbol):
    return om.height(arbol)

# Funciones de consulta
def caracterizarrep(cat, carac, minimo, maximo):
    mapa = cat["features"]

    if (carac == "energy") or (carac == "tempo"):
        listareps = lt.newList(datastructure= "ARRAY_LIST")
        if carac == "energy":
            a = mp.get(mapa,"energy-dance")
        else:
            a = mp.get(mapa,"tempo-instru")
        m_carac = me.getValue(a)
        m_reps = om.values(m_carac, minimo, maximo)
        for i in lt.iterator(m_reps):
            l_reps = om.valueSet(i)
            for e in lt.iterator(l_reps):
                lt.addLast(listareps, e)
    else:
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
    a = mp.get(mapa, "energy-dance")
    m_energy = me.getValue(a)
    lista_energy = om.values(m_energy, minEnergy, maxEnergy)
    return musica(lista_energy, minDanceability, maxDanceability)

def musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo):
    mapa = cat["features"]
    a = mp.get(mapa, "tempo-instru")
    m_tempo = me.getValue(a)
    lista_tempo = om.values(m_tempo, minTempo, maxTempo)
    return musica(lista_tempo, minInstru, maxInstru)
    
def musica(out_list, min_val, max_val):
    arbol_pistas = om.newMap(omaptype='RBT',
                                      comparefunction=compareValue)
    lista_5_tracks = lt.newList(datastructure="ARRAY_LIST")

    for i in lt.iterator(out_list):
        in_list = om.values(i, min_val, max_val)
        for rep in lt.iterator(in_list):
            for e in lt.iterator(rep):
                track_id = e["track_id"]
                om.put(arbol_pistas, track_id, e)

    numero_tracks = om.size(arbol_pistas)
    if numero_tracks >= 5:
        num = 5
    else:
        num = numero_tracks

    tracks_aleatorios = random.sample(range(0, numero_tracks), num)
    llaves = lt.newList(datastructure="ARRAY_LIST")

    for n in tracks_aleatorios:
        llave = om.select(arbol_pistas, n)
        lt.addLast(llaves, llave)

    for a in lt.iterator(llaves):
        rep = om.get(arbol_pistas, a)
        rep_1 = me.getValue(rep)
        lt.addLast(lista_5_tracks, rep_1)

    return (numero_tracks, lista_5_tracks)

def generosmusicales(cat, listageneros):
    info_generos = lt.newList(datastructure="ARRAY_LIST")
    tot_escuchas = 0

    for gen in listageneros:
        info = caracterizarrep(cat, "tempo", gen["min_tempo"], gen["max_tempo"])
        gen["escuchas"] = info[0]
        tot_escuchas+= gen["escuchas"]
        gen["artistas"] = info[1]
        arbol = info[2]
        lista_id_artistas = lt.newList(datastructure="ARRAY_LIST")
        for i in range(1, 11):
            id_artista = om.select(arbol, i)
            lt.addLast(lista_id_artistas, id_artista)
        gen["id_artistas"] = lista_id_artistas
        lt.addLast(info_generos, gen)

    return (tot_escuchas, info_generos)

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