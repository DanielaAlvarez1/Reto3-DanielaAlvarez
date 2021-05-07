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
                                    comparefunction=compareValue)
    cat['sentiment'] = mp.newMap(11,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    cat["genres"] = mp.newMap(11,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    return cat

# Funciones para agregar informacion al catalogo
def addCategories(cat, rep):
    m = cat["features"]
    n_categories = 9
    for key in rep:
        if n_categories > 0:
                mp.put(m, key, om.newMap(omaptype='RBT',
                                      comparefunction=compareValue))
        else:
            break
        n_categories-=1

def addRep(cat, rep):
    addRepFeatures(cat, rep)
    addRepGenre(cat, rep)

def addRepFeatures(cat, rep):
    m = cat["features"]
    n_categories = 9
    date = datetime.datetime.strptime(rep["created_at"], '%Y-%m-%d %H:%M:%S')
    info = {"artist_id": rep["artist_id"], "track_id": rep["track_id"], "created_at": date}
    for key in rep:
        if n_categories > 0:
            if key == "danceability":
                info["energy"] = rep["energy"]
            if key == "instrumentalness":
                info["tempo"] = rep["tempo"]
            cat_value = float(rep[key])
            info[key] = cat_value
            a = mp.get(m, key)
            m_categorie = me.getValue(a)
            m_categorie_new = addMapKey(m_categorie, cat_value, info)
            mp.put(m, key, m_categorie_new)
        else:
            break
        n_categories-=1        
    return cat

def addRepGenre(cat, rep):
    m = cat["genres"]
    tempo = float(rep["tempo"])
    hour = datetime.datetime.strptime(rep["created_at"][11:], '%H:%M:%S')
    date = datetime.datetime.strptime(rep["created_at"], '%Y-%m-%d %H:%M:%S')
    info = {"artist_id": rep["artist_id"], "track_id": rep["track_id"], "created_at": date, "user_id": rep["user_id"]}
    if (tempo >= 60) and (tempo <= 90):
        name = "Reggae"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 70) and  (tempo <= 100):
        name = "Down-Tempo"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 90) and  (tempo <= 120):
        name = "Chill-Out"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 85) and  (tempo <= 115):
        name = "Hip-Hop"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 120) and  (tempo <= 125):
        name = "Jazz and Funk"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 100) and  (tempo <= 130):
        name = "Pop"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 60) and  (tempo <= 80):
        name = "R&B"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 110) and  (tempo <= 140):
        name = "Rock"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)
    if (tempo >= 100) and  (tempo <= 160):
        name = "Metal"
        a = mp.get(m, name)
        m_genre = me.getValue(a)
        m_genre_new = addMapKey(m_genre, hour, info)
        mp.put(m, name, m_genre_new)

def addHashtag(cat, rep):
    m = cat["hashtags"]
    hour = datetime.datetime.strptime(rep["created_at"][11:], '%H:%M:%S')
    date = datetime.datetime.strptime(rep["created_at"], '%Y-%m-%d %H:%M:%S')
    info = {"user_id": rep["user_id"], "track_id": rep["track_id"], "created_at": date}
    addMapKey(m, hour, info)

def addSentiment(cat, sent):
    m = cat["sentiment"]
    if sent["vader_avg"] == "":
        vader_avg = 0.0
    else:
        vader_avg = float(sent["vader_avg"])
    hashtag = sent["hashtag"]
    mp.put(m, hashtag, vader_avg)

# Funciones para creacion de datos
def addMapKey(c_map, value, info):
    if om.contains(c_map, value):
        a = om.get(c_map, value)
        l_value = me.getValue(a)
    else:
        l_value = lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(l_value, info)
    om.put(c_map, value, l_value)
    return c_map

def addGenre(cat):
    m = cat["genres"]
    genres = ["Reggae", "Down-Tempo", "Chill-Out", "Hip-Hop", "Jazz and Funk", "Pop", "R&B", 
            "Rock", "Metal"]
    for i in genres:
        m_genre = om.newMap(omaptype= "RBT",
                        comparefunction=compareValue)
        mp.put(m, i, m_genre)

# Funciones de consulta de datos del map
def repSize(arbol):
    return om.size(arbol)

def treeHeight(arbol):
    return om.height(arbol)

# Funciones de Consulta
def caracterizarrep(cat, carac, minimo, maximo):
    m = cat["features"]
    a = mp.get(m, carac)
    m_carac = me.getValue(a)
    l_reps = om.values(m_carac, minimo, maximo)

    t_artists = om.newMap(omaptype='RBT',
                            comparefunction=compareValue)
    num_reps = 0

    for lists in lt.iterator(l_reps):
        size = lt.size(lists)
        num_reps+=size
        for reps in lt.iterator(lists):
            artist = reps["artist_id"]
            if om.contains(t_artists, artist):
                c = om.get(t_artists, artist)
                l_artist = me.getValue(c)
            else:
                l_artist = lt.newList(datastructure="SINGLE_LINKED")
            lt.addLast(l_artist, reps)
            om.put(t_artists, artist, l_artist)

    artists = om.size(t_artists)
    return (num_reps, artists, t_artists)

def musicafestejar(cat, minEnergy, maxEnergy, minDanceability, maxDanceability):
    m = cat["features"]
    m_reps = om.newMap(omaptype='RBT',
                            comparefunction=compareValue)
    m_tracks = om.newMap(omaptype='RBT',
                            comparefunction=compareValue)

    a = mp.get(m, "energy")
    m_energy = me.getValue(a)
    l_energy = om.values(m_energy, minEnergy, maxEnergy)
    for lists in lt.iterator(l_energy):
        for e in lt.iterator(lists):
            om.put(m_reps, e["track_id"], "")
    
    b = mp.get(m, "danceability")
    m_dance = me.getValue(b)
    l_dance = om.values(m_dance, minDanceability, maxDanceability)
    for lists in lt.iterator(l_dance):
        for e in lt.iterator(lists):
            if om.contains(m_reps, e["track_id"]):
                om.put(m_tracks, e["track_id"], e)

    n_tracks = om.size(m_tracks)
    if n_tracks >= 5:
        num = 5
    else:
        num = n_tracks

    random_tracks = random.sample(range(0, n_tracks), num)
    keys = lt.newList(datastructure="ARRAY_LIST")
    l_tracks = lt.newList(datastructure="ARRAY_LIST")

    for n in random_tracks:
        key = om.select(m_tracks, n)
        lt.addLast(keys, key)

    for a in lt.iterator(keys):
        rep = om.get(m_tracks, a)
        rep_info = me.getValue(rep)
        lt.addLast(l_tracks, rep_info)

    return (n_tracks, l_tracks)

def musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo):
    m = cat["features"]
    m_reps = om.newMap(omaptype='RBT',
                            comparefunction=compareValue)
    m_tracks = om.newMap(omaptype='RBT',
                            comparefunction=compareValue)

    a = mp.get(m, "tempo")
    m_tempo = me.getValue(a)
    l_tempo = om.values(m_tempo, minTempo, maxTempo)
    for lists in lt.iterator(l_tempo):
        for e in lt.iterator(lists):
            om.put(m_reps, e["track_id"], "")
    
    b = mp.get(m, "instrumentalness")
    m_instru = me.getValue(b)
    l_instru = om.values(m_instru, minInstru, maxInstru)
    for lists in lt.iterator(l_instru):
        for e in lt.iterator(lists):
            if om.contains(m_reps, e["track_id"]):
                om.put(m_tracks, e["track_id"], e)

    n_tracks = om.size(m_tracks)
    if n_tracks >= 5:
        num = 5
    else:
        num = n_tracks

    random_tracks = random.sample(range(0, n_tracks), num)
    keys = lt.newList(datastructure="ARRAY_LIST")
    l_tracks = lt.newList(datastructure="ARRAY_LIST")

    for n in random_tracks:
        key = om.select(m_tracks, n)
        lt.addLast(keys, key)

    for a in lt.iterator(keys):
        rep = om.get(m_tracks, a)
        rep_info = me.getValue(rep)
        lt.addLast(l_tracks, rep_info)

    return (n_tracks, l_tracks)

def generosmusicales(cat, listgenres):
    l_genres = lt.newList(datastructure="ARRAY_LIST")
    tot_reps = 0

    for gen in listgenres:
        info = caracterizarrep(cat, "tempo", gen["min_tempo"], gen["max_tempo"])
        gen["escuchas"] = info[0]
        tot_reps+= gen["escuchas"]
        gen["artistas"] = info[1]
        tree = info[2]
        l_id_artists = lt.newList(datastructure="ARRAY_LIST")
        for i in range(1, 11):
            id_artist = om.select(tree, i)
            lt.addLast(l_id_artists, id_artist)
        gen["id_artistas"] = l_id_artists
        lt.addLast(l_genres, gen)

    return (tot_reps, l_genres)

# Funciones utilizadas para comparar elementos dentro de una lista
def compareValue(val1, val2):
    if (val1 == val2):
        return 0
    elif (val1 > val2):
        return 1
    else:
        return -1

def compareRefValue(dic1, dic2):
    if (dic1["ref"] == dic2["ref"]):
        return 0
    elif (dic1["ref"] > dic2["ref"]):
        return 1
    else:
        return -1