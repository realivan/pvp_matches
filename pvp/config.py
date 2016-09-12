#!/usr/bin/python
# coding: utf8

import sqlite3


def insert_match(num):
    try:
        cur.execute("INSERT INTO matches (player_number) VALUES (%s)" % num)
        conn.commit()
        return True
    except:
        return False


def insert_db(data):
    try:
        for key in data:
            cur.execute('INSERT INTO players (id_match, player_number, player_nick, ip) VALUES (?, ?, ?, ?)', key)
        conn.commit()
        return True
    except:
        return False

conn = sqlite3.connect('db_matches')
cur = conn.cursor()
# создаем таблицу для списка матчей
table = "CREATE TEMPORARY TABLE matches (id int auto_increment primary key, player_number int)"
cur.execute(table)
# вставляем данные о первом матче
insert_match(4)
# создаем таблицу содержащую данные об игроках учавствующих в матче
table = "CREATE TEMPORARY TABLE players (id int auto_increment primary key, id_match int, player_number int, player_nick char, ip char)"  # номер матча, порядковый номер в матче, ник, ip игрока
cur.execute(table)
