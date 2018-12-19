import mysql.connector as sql
bold = '\033[1;34m' + '\033[1m'
end = '\033[0m'
dbname = 'all_about_movies'
movieTB = 'movies'
genreTB = 'genres'
genreBridge = 'genreBridge'
castTB = 'cast'
castBridge = 'castBridge'
prodTB = 'production'
prodBridge = 'prodBridge'


# main:
def Connect_with_SQL():
    connect_with_server()
    if connect_with_server:
        sql.connect(host="localhost", user="Windxore", passwd="maslo")
        print('Connected with server')
    else:
        print('Failed to connect with database')
    mydb = db_connecting()
    cursor = mydb.cursor()
    check_table_existence(cursor)
    return mydb
# Connect_with_SQL()


def connect_with_server():
    try:
        sql.connect(host="localhost", user="Windxore", passwd="maslo")
        return True
    except:
        return False


def db_connecting():
    mydb = sql.connect(host="localhost", user="Windxore", passwd="maslo")
    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")
    for db in cursor:
        if db == (dbname,):
            mydb = sql.connect(host="localhost", user="Windxore", passwd="maslo", database=dbname)
            print('Connected with database ' + bold + dbname + end)
            return mydb
    cursor.execute("CREATE DATABASE " + dbname)
    mydb = sql.connect(host="localhost", user="Windxore", passwd="maslo", database=dbname)
    print('Databese ' + bold + dbname + end + ' created and connected with')
    return mydb


def check_table_existence(cursor):

    tables_to_make = ["CREATE TABLE " + movieTB + " (idmovie INT NOT NULL AUTO_INCREMENT, title VARCHAR(255) NOT NULL,"
                                                  " length TIME, premiere DATE, direction VARCHAR(255),"
                                                  " description LONGTEXT, filmweb_link VARCHAR(255),"
                                                  " PRIMARY KEY (idmovie));",
                      "CREATE TABLE " + genreTB + " (idgenre INT NOT NULL AUTO_INCREMENT, genre VARCHAR(45) NOT NULL, "
                                                  "PRIMARY KEY (idgenre));",
                      "CREATE TABLE " + genreBridge + " (idgenre INT NOT NULL, idmovie INT NOT NULL);",
                      "CREATE TABLE " + castTB + " (idactor INT NOT NULL AUTO_INCREMENT, actor VARCHAR(255) NOT NULL, "
                                                 "PRIMARY KEY (idactor));",
                      "CREATE TABLE " + castBridge + " (idactor INT NOT NULL, idmovie INT NOT NULL);",
                      "CREATE TABLE " + prodTB + " (idprod INT NOT NULL AUTO_INCREMENT, country VARCHAR(255) NOT NULL,"
                                                 " PRIMARY KEY (idprod));",
                      "CREATE TABLE " + prodBridge + " (idprod INT NOT NULL, idmovie INT NOT NULL);"]

    for table in tables_to_make:
        try:
            cursor.execute(table)
            # print('Table ' + bold + table[13:table.index(' (')] + end + ' created')
        except:
            # print('Table ' + bold + table[13:table.index(' (')] + end + ' exists')
            pass
    print('All tables are ready\n')


def chceck_in_db(table, column, element, cursor):
    movie_in_db = False
    cursor.execute("SELECT " + column + " FROM " + table + ";")
    for link in cursor:
        if link == (element,):
            movie_in_db = True
            # print('Movie ' + bold + movieDict['Tytuł'][0] + end + ' already exists in the DataBase\n')
    if movie_in_db:
        return True
    else:
        return False


def insert_into_db(movieDict, cursor, mydb):

    try:
        if chceck_in_db(movieTB, 'filmweb_link', movieDict['Filmweb link'][0], cursor):
            return
    except IndexError:
        cursor.execute("INSERT INTO " + movieTB + ' (idmovie, title) VALUES(NULL, "' + movieDict['Tytuł'][0] + '");')
        return

    cursor.execute("INSERT INTO " + movieTB + ' (idmovie, title, length, premiere, direction, description,'
                                              ' filmweb_link) VALUES(NULL, "'
                   + movieDict['Tytuł'][0] + '", "'
                   + str(movieDict['Długość'][0] // 60) + ":" + str(movieDict['Długość'][0] % 60) + '", "'
                   + str(movieDict['Premiera'][0]) + '", "'
                   + movieDict['Reżyseria'][0] + '", "'
                   + movieDict['Opis'][0] + '", "'
                   + movieDict['Filmweb link'][0] + '");')
    mydb.commit()

    cursor.execute("SELECT idmovie FROM " + movieTB + " where filmweb_link = '" + movieDict['Filmweb link'][0] + "';")
    for mid in cursor:
        movieid = str(mid[0])

    for genre in movieDict['Gatunek']:
        if not chceck_in_db(genreTB, 'genre', genre, cursor):
            cursor.execute("INSERT INTO " + genreTB + " (idgenre, genre) VALUES(NULL, '" + genre + "');")
            mydb.commit()
        cursor.execute("SELECT idgenre FROM " + genreTB + " where genre = '" + genre + "';")
        for gid in cursor:
            genreid = str(gid[0])
        cursor.execute("INSERT INTO " + genreBridge + " (idgenre, idmovie) VALUES(" + genreid + ", " + movieid + ");")
        mydb.commit()

    for prod in movieDict['Produkcja']:
        if not chceck_in_db(prodTB, 'country', prod, cursor):
            cursor.execute("INSERT INTO " + prodTB + " (idprod, country) VALUES(NULL, '" + prod + "');")
            mydb.commit()
        cursor.execute("SELECT idprod FROM " + prodTB + " where country = '" + prod + "';")
        for pid in cursor:
            prodid = str(pid[0])
        cursor.execute("INSERT INTO " + prodBridge + " (idprod, idmovie) VALUES(" + prodid + ", " + movieid + ");")
        mydb.commit()

    for actor in movieDict['Obsada']:
        if not chceck_in_db(castTB, 'actor', actor, cursor):
            cursor.execute("INSERT INTO " + castTB + " (idactor, actor) VALUES(NULL, '" + actor + "');")
            mydb.commit()
        cursor.execute("SELECT idactor FROM " + castTB + " where actor = '" + actor + "';")
        for aid in cursor:
            actorid = str(aid[0])
        cursor.execute("INSERT INTO " + castBridge + " (idactor, idmovie) VALUES(" + actorid + ", " + movieid + ");")
        mydb.commit()
