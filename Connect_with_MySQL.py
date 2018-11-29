import mysql.connector as sql
bold = '\033[1;34m' + '\033[1m'
end = '\033[0m'
dbname = 'all_about_movies'
tbname = 'movies'


# main:
def Connect_with_SQL():
    connect_with_server()
    if connect_with_server:
        sql.connect(host="localhost", user="********", passwd="********")
        print('Connected with server')
    else:
        print('Failed to connect with database')
    mydb = db_connecting()
    cursor = mydb.cursor()
    check_table_existence(cursor)
# Connect_with_SQL()


def connect_with_server():
    try:
        sql.connect(host="localhost", user="********", passwd="********")
        return True
    except:
        return False


def db_connecting():
    mydb = sql.connect(host="localhost", user="********", passwd="********")
    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")
    for db in cursor:
        if db == (dbname,):
            mydb = sql.connect(host="localhost", user="********", passwd="********", database=dbname)
            print('Connected with database ' + bold + dbname + end)
            return mydb
    cursor.execute("CREATE DATABASE " + dbname)
    mydb = sql.connect(host="localhost", user="********", passwd="********", database=dbname)
    print('Databese ' + bold + dbname + end + ' created and connected with')
    return mydb


def check_table_existence(cursor):
    try:
        cursor.execute("CREATE TABLE " + tbname + " (id INT NOT NULL AUTO_INCREMENT, tytul VARCHAR(255) NOT NULL, "
                                                  "dlugosc TIME NOT NULL, premiera DATE NOT NULL, "
                                                  "gatunek  VARCHAR(255) NOT NULL, produkcja VARCHAR(255) NOT NULL, "
                                                  "rezyseria VARCHAR(255) NOT NULL, obsada VARCHAR(255) NOT NULL, "
                                                  "opis LONGTEXT NOT NULL, filmweb_link VARCHAR(255) NOT NULL, "
                                                  "PRIMARY KEY (id))")
        print('Table ' + bold + tbname + end + ' created\n')
    except:
        print('Table ' + bold + tbname + end + ' exists\n')



