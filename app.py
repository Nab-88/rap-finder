#!/usr/bin/python2.7.10
# -*-coding:Latin-1 -
from flask import Flask, render_template, request, session
import os
import requests, base64, json, calendar, datetime, sys
from save import initialisation_db, ajouter_album,get_album_all,is_present_db,delete_table_content

app = Flask(__name__)
conn, c = initialisation_db()
# app.secret_key = os.urandom(24)
# Session(app)
reload(sys)
sys.setdefaultencoding('utf8')



@app.route('/')
def index():
    print("Bienvenue à l'index")
    for el in c:
        print(el)
    token = get_token()
    release = get_new_all(token)
    parcourir_all(token, release, conn, c)
    array = get_album_all(conn,c)
    return render_template('index.html', resultat=array, conn=conn, c=c)

@app.route('/delete', methods=['POST', 'GET'])
def button_press():
    delete_table_content(conn,c)
    print(get_album_all(conn,c))
    print("OVEEEER")
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


#test d'une requete
def get_album(token, id_test):
    album = requests.get("https://api.spotify.com/v1/albums/"+id_test,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(album.content)
    return res



def get_new(token, offset):
    release = requests.get('https://api.spotify.com/v1/browse/new-releases?country=FR&limit=50&offset='+str(offset),
    headers = {'Authorization':
    'Bearer '+ token})
    return release

def get_new_all(token):
    compteur = 0
    resultat = []
    while(compteur <500):
    #while(compteur<50):
        res = get_new(token, compteur)
        compteur += 50
        resultat.append(res)
    return resultat

def get_album_genre(token, album_id):
    album = requests.get("https://api.spotify.com/v1/albums/"+album_id,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(album.content)
    print res
    return res["genres"]

def get_artist_genre(token, artist_id):
    artist = requests.get("https://api.spotify.com/v1/artists/"+artist_id,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(artist.content)
    print res["genres"]
    return res["genres"]

def is_rap_artist(token, artist_id):
    array_genre = get_artist_genre(token, artist_id)
    array_rap = ["hip hop", "rap", "french rap", "trap", "french hip hop", "irish hip hop", "trap français", "belgian hip hop", "trap music", "pop rap", "gangster rap"]
    for genre in array_genre:
        if(genre.encode('utf-8').strip() in array_rap):
            return True
    return False



def get_artist_from_id(token, id_artist):
    artist = requests.get("https://api.spotify.com/v1/artists/"+id_artist,
    headers = {'Authorization':
    'Bearer '+ token})
    res = json.loads(artist.content)
    print res
    return res


def get_author_of_album(json_album):
    """
    input : l'item en json définissant un album en particulier
    output : un array contenant l'ensemble des artistes présents sur cet album
    """
    array_artists = []
    for artist in json_album["artists"]:
        array_artists.append(artist["name"])
    return array_artists

def get_date_sortie(json_album):
    """
    input : l'item en json définissant un album en particulier
    output : la date de sortie
    """
    releaseDate = json_album["release_date"].encode('utf-8').strip()
    return releaseDate

def get_info(json_album):
    """
    input : l'item en json définissant un album en particulier
    output : dictionnaire avec chaque valeur à insérer dans la base de données"
    """
    info = {'main_artist':"",'nom_album':"",'type':"",'release_date':"",'uri':"",'id_spotify':""}
    info['main_artist'] = get_author_of_album(json_album)[0]
    info['nom_album'] = json_album["name"]
    info['type'] = json_album['album_type']
    info['release_date'] = json_album['release_date']
    info['uri'] = json_album['uri']
    info['id_spotify'] = json_album['id']
    return info

def parcourir_all(token, liste_json, conn, c):
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
            info = get_info(album)
            if(is_rap_artist(token, album["artists"][0]["id"].encode('utf-8').strip())):
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
                ajouter_album(conn, c, info)
    if(is_present_db(conn, c, "44ihbsNXtt1hWP8PJtBgSP")):
        print("starfoulah deja present")
    return True
