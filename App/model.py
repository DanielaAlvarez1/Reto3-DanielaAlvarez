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
    info = { "track_id": rep["track_id"],"created_at": date, "user_id": rep["user_id"]}
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
    date = datetime.datetime.strptime(rep["created_at"][11:], '%H:%M:%S')
    info = { "track_id": rep["track_id"], "created_at": date, "hashtag": rep["hashtag"]}
    addMapKey(m, rep["track_id"], info)

def addSentiment(cat, sent):
    m = cat["sentiment"]
    if sent["vader_avg"] == "":
        vader_avg = 100
    else:
        vader_avg = float(sent["vader_avg"])
    hashtag = sent["hashtag"].lower()
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

def musica(cat, carac_1, carac_2, min_1, max_1, min_2, max_2):
    m = cat["features"]
    m_reps = mp.newMap(4000,
                        maptype='PROBING',
                        loadfactor=0.5)
    m_tracks = om.newMap(omaptype='RBT',
                            comparefunction=compareValue)

    a = mp.get(m, carac_1)
    m_1 = me.getValue(a)
    l_1 = om.values(m_1, min_1, max_1)
    for lists in lt.iterator(l_1):
        for e in lt.iterator(lists):
            mp.put(m_reps, e["track_id"], "")
    
    b = mp.get(m, carac_2)
    m_2 = me.getValue(b)
    l_2 = om.values(m_2, min_2, max_2)
    for lists in lt.iterator(l_2):
        for e in lt.iterator(lists):
            if mp.contains(m_reps, e["track_id"]):
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

def musicafestejar(cat, minEnergy, maxEnergy, minDanceability, maxDanceability):
    return musica(cat, "energy", "danceability", minEnergy, maxEnergy, minDanceability, maxDanceability)

def musicaestudiar(cat, minInstru, maxInstru, minTempo, maxTempo):
    return musica(cat, "tempo", "instrumentalness", minTempo, maxTempo, minInstru, maxInstru)

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

def generotiempo(cat, hora_1, hora_2):
    m_g = cat["genres"]
    l_gen_name = mp.keySet(m_g)
    l_gen_reps = lt.newList(datastructure="ARRAY_LIST")
    l_max_tracks_genres = ""
    max_reps_genre = 0
    tot_reps = 0
    for gen in lt.iterator(l_gen_name):
        a = mp.get(m_g, gen)
        m_gen = me.getValue(a)
        l_reps = om.values(m_gen, hora_1, hora_2)
        reps = 0
        l_gen = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareValue)
        for e in lt.iterator(l_reps):
            size = lt.size(e)
            reps+=size
            for i in lt.iterator(e):
                if lt.isPresent(l_gen, i["track_id"]) == 0:
                    lt.addLast(l_gen, i["track_id"])
        if reps > max_reps_genre:
            max_reps_genre = reps
            l_max_tracks_genres = l_gen
        tot_reps+=reps
        dic = {"nombre": gen, "reps": reps}
        lt.addLast(l_gen_reps, dic)

    unique_tracks = lt.size(l_max_tracks_genres)
    sorted_gen = sortReps(l_gen_reps, compareReps)
    top_genre = lt.getElement(sorted_gen, 0)

    r = lt.newList(datastructure="ARRAY_LIST")
    m_h = cat["hashtags"]
    m_s = cat["sentiment"]
    for i in lt.iterator(l_max_tracks_genres):
        num_hashtags = 0
        sum_vader = 0
        a = om.get(m_h, i)
        l_hashtags = me.getValue(a)
        for e in lt.iterator(l_hashtags):
            h = e["hashtag"].lower()
            if (e["created_at"] >= hora_1) and (e["created_at"] <= hora_2):
                if mp.contains(m_s, h):
                    b = mp.get(m_s, h)
                    vader = me.getValue(b)
                    if vader != 100:
                        num_hashtags+=1
                        sum_vader+=vader
        if num_hashtags == 0:
            num_hashtags = 1
        vader_avg = sum_vader/num_hashtags
        dic = {}
        dic["track_id"] = i
        dic["numero hashtags"] = num_hashtags
        dic["vader promedio"] = vader_avg
        lt.addLast(r, dic)

    sorted_ht = sortReps(r, compareTrackHashtags)
    top_tracks = lt.subList(sorted_ht, 1, 10)

    return (tot_reps, sorted_gen, unique_tracks, top_tracks)

# Funciones utilizadas para comparar elementos dentro de una lista
def compareValue(val1, val2):
    if (val1 == val2):
        return 0
    elif (val1 > val2):
        return 1
    else:
        return -1

def compareTrackIds(dic1, dic2):
    if (dic1["track_id"] == dic2["track_id"]):
        return 0
    elif (dic1["track_id"] > dic2["track_id"]):
        return 1
    else:
        return -1

def compareTrackHashtags(track1, track2):
     if int(track1["numero hashtags"]) > int(track2["numero hashtags"]):
        return True
     else:
        return False    

def compareReps(track1, track2):
     if int(track1["reps"]) > int(track2["reps"]):
        return True
     else:
        return False    

# Funciones de Ordenamiento 
def sortReps(lst, comparefunction):
    sorted_list = sa.sort(lst, comparefunction)
    return sorted_list