#!/usr/bin/python2.7.10
# -*-coding:Latin-1 -
from flask import Flask, render_template, request, session
import os
import requests, base64, json, calendar, datetime, sys
from save import initialisation_db, ajouter_album,get_all_album,is_present_in_db,delete_table_content

app = Flask(__name__)
conn, cursor = initialisation_db()
spotify_url = 'https://api.spotify.com/v1/'
#reload(sys)
#sys.setdefaultencoding('utf8')



@app.route('/')
def index():
    print("Bienvenue à l'index")
    token = get_token()
    release = get_all_new_releases(token)
    get_artist_from_id(token, '2jFnPm8VeSO19i6B8blXB5')
    browse_all(token, release, conn, cursor)
    array = get_all_album(conn,cursor)
    return render_template('index.html', resultat=array, conn=conn, cursor=cursor)

@app.route('/delete', methods=['POST', 'GET'])
def button_press():
    delete_table_content(conn,cursor)
    return render_template('delete.html');

#acces au token
def get_token():
    r = requests.post('https://accounts.spotify.com/api/token',
    data = {'grant_type':'client_credentials'},
    headers = {'Authorization':
    'Basic ' +  base64.b64encode('03e693cfd1f54c03b5b0ac4edbd1354b:3b701d5fa70043e4a6c2aa59e580c2c6')})

    res = json.loads(r.content)
    token = res["access_token"]
    return token


def get_album(token, abum_id):
    album = requests.get(spotify_url + "albums/" + album_id,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(album.content)
    return res



def get_new_releases(token, offset):
    releases = requests.get(spotify_url + 'browse/new-releases?country=FR&limit=50&offset='+str(offset),
    headers = {'Authorization':
    'Bearer '+ token})
    return releases

def get_all_new_releases(token):
    compteur = 0
    resultat = []
    while(compteur <500):
        res = get_new_releases(token, compteur)
        compteur += 50
        resultat.append(res)
    return resultat

def get_album_genre(token, album_id):
    album = requests.get(spotify_url + "albums/" +album_id,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(album.content)
    return res["genres"]

def get_artist_genre(token, artist_id):
    artist = requests.get(spotify_url + "artists/"+artist_id,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(artist.content)
    return res["genres"]

def is_rap_genre(token, artist_id):
    artist_genre = get_artist_genre(token, artist_id)
    array_rap = ["hip hop", "rap", "french rap", "trap", "french hip hop", "irish hip hop", "trap français", "belgian hip hop", "trap music", "pop rap", "gangster rap"]
    for genre in artist_genre:
        if(genre.encode('utf-8').strip() in array_rap):
            return True
    return False



def get_artist_from_id(token, id_artist):
    artist = requests.get(spotify_url + "artists/"+id_artist,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(artist.content)
    return res


def get_author_of_album(album):
    """
    input : l'item en json définissant un album en particulier
    output : un array contenant l'ensemble des artistes présents sur cet album
    """
    array_artists = []
    for artist in album["artists"]:
        array_artists.append(artist["name"])
    return array_artists

def get_release_date(album):
    """
    input : l'item en json définissant un album en particulier
    output : la date de sortie
    """
    return(album["release_date"].encode('utf-8').strip())


def get_album_info(album):
    """
    input : l'item en json définissant un album en particulier
    output : dictionnaire avec chaque valeur à insérer dans la base de données"
    """
    info = {'main_artist':get_author_of_album(album)[0],
    'nom_album':album["name"],
    'type':album['album_type'],
    'release_date':album['release_date'],
    'uri':album['uri'],
    'id_spotify':album['id']
    }
    return info

def browse_all(token, liste_json, conn, cursor):
    """
    Cette fonction permet d'écrire dans une string l'ensemble des objets
    présents dans la liste de json passés en entrés de la fonction
    """
    chaine = ""
    resultat = []
    for element in liste_json:
    #element = liste_json[0]
        res = json.loads(element.content)
        truc = res["albums"]
        truc2 = truc["items"]
        for album in truc2:
            info = get_album_info(album)
            if(is_rap_genre(token, album["artists"][0]["id"].encode('utf-8').strip())):
                #ca je le garde pour l'instant ahah
                # chaine += "Nom de l'album : " + album["name"].encode('utf-8').strip() + " -- Nom des artistes présents : "
                # array_artists = get_author_of_album(album)
                # number_of_artist = len(array_artists)
                # for i in range(number_of_artist):
                #     if (i == (number_of_artist-1)):
                #         chaine += array_artists[i].encode('utf-8').strip()
                #     else:
                #         chaine += array_artists[i].encode('utf-8').strip()+" feat "
                # chaine += " -- Date de sortie : " + get_date_sortie(album)
                # chaine += " -- Genre de l'album :"
                # array_genre = get_artist_genre(token, album["artists"][0]["id"].encode('utf-8').strip())
                # for genre in array_genre:
                #         chaine += genre.encode('utf-8').strip() + " "
                # resultat.append(chaine)
                # chaine = ""
                ajouter_album(conn, cursor, info)
    if(is_present_in_db(conn, cursor, "44ihbsNXtt1hWP8PJtBgSP")):
        print("starfoulah deja present")
    return True
