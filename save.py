#!/usr/bin/python2.7.10
# -*-coding:Latin-1 -
import sqlite3

def initialisation_db():
    """
    Initialise la base de donnée
    """
    conn = sqlite3.connect('released.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS albums (artist text, nom_album text, type text, release_date text, uri text, id_spotify text)''')
    conn.commit()
    return (conn, cursor);

def ajouter_album(conn, cursor,info_album):
    array = []
    artist = info_album['main_artist']
    nom_album = info_album['nom_album']
    type = info_album['type']
    release_date = info_album['release_date']
    uri = info_album['uri']
    id_spotify = info_album['id_spotify']
    array.append(artist)
    array.append(nom_album)
    array.append(type)
    array.append(release_date)
    array.append(uri)
    array.append(id_spotify)
    cursor.execute('''INSERT INTO albums VALUES (?,?,?,?,?,?)''', array )
    conn.commit()
    return True

def get_all_album(conn, cursor):
    result = []
    for row in cursor.execute('''SELECT * from albums'''):
        result.append(row)
    return result

def is_present_in_db(conn, cursor, id):
    if (cursor.execute('''SELECT * from albums WHERE id_spotify = (?)''', (id,))):
        return True
    return False

def delete_table_content(conn,cursor):
    cursor.execute('''DELETE FROM albums''')
    conn.commit()
    return True
