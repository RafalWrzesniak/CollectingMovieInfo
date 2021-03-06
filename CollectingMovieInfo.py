import os
import sys
import time
import urllib.request as ur
import urllib.parse as up
import PIL.ImageGrab
from Connect_with_MySQL import Connect_with_SQL, insert_into_db, chceck_in_db, movieTB

bold = '\033[1;34m' + '\033[1m'
red = '\033[91m' + '\033[1m'
end = '\033[0m'
path = "E:\\Rafał\\Filmy"
# path = "Z:\\Filmy2"


def hdd_searching(path):
    # "F:\Studia\Python"
    cur_dir = os.getcwd()
    if cur_dir != path:
        os.chdir(path)
        cur_dir = os.getcwd()

    global movieList
    movieList = os.listdir(cur_dir)
    if '00DONE' in movieList:
        movieList.remove('00DONE')
    if 'Thumbs.db' in movieList:
        movieList.remove('Thumbs.db')
    if 'desktop.ini' in movieList:
        movieList.remove('desktop.ini')
    # print(bold + 'Lista filmów:\n' + end, movieList, "\n")
    os.chdir("E:\\Studia\\Python")


def internet_searching(movie_title, cursor):

    global movieDict
    movieDict = {}

    def URLChanging(link):
        global passit
        passit = True
        try:
            global respData
            req = ur.Request(link)
            respo = ur.urlopen(req)
            respData = respo.read().decode('utf-8')
            respData = str(respData)
            if '&oacute;' in respData:
                respData = respData.replace('&oacute;', 'ó')
            if '&quot;' in respData:
                respData = respData.replace('&quot;', '"')
            if '&eacute;' in respData:
                respData = respData.replace('&quot;', 'e')
            if ';' in respData:
                respData = respData.replace(';', '')
            if '%C5%84' in respData:
                respData = respData.replace('%C5%84', 'ń')
            if 'u0142' in respData:
                respData = respData.replace('u0142', 'ł')
            if '&ouml' in respData:
                respData = respData.replace('&ouml', 'o')
            if '&nbsp' in respData:
                respData = respData.replace('&nbsp', ' ')
            if '&ndash ' in respData:
                respData = respData.replace('&ndash ', '- ')
        except Exception as e:
            print(red + 'Failed to decode movie name: ' + end + movie_title)
            passit = False
            # print(e)
            # print("Całość: " + str(round(time.time() - start, 2)) + " [s]")
            # print(200 * '+' + '\n')

    class FilmKlasa:

        gatunek = []
        kraj = []
        rezyser = []

        # Getting movie data
        def tytul(self):
            # tytul = [respData[respData.index('<title>') + len('<title>'):
            #             respData.index('<title>') + len('<title>') + len(szukanaFraza)]]
            tytul = [respData[respData.index('<title>') + len('<title>'):respData.index('</title>', respData.index('<title>'))-17]]
            return tytul

        def rokProdukcji(self):
            rokProdukcji = [respDataTemp[respDataTemp.index('firstLaunched:"')+len('firstLaunched:"'):
                            respDataTemp.index('"', respDataTemp.index('firstLaunched:"')+len('firstLaunched:"'))]]
            return rokProdukcji

        def czasTrwania(self):
            try:
                czasTrwania = [int(respDataTemp[respDataTemp.index('datetime="PT')+len('datetime="PT'):
                                    respDataTemp.index('M"', respDataTemp.index('datetime="PT')+len('datetime="PT'))])]
            except Exception:
                czasTrwania = [0]
            return czasTrwania

        def Gatunek_Produkcja_Rezyseria(self):
            movieTempDict = {'Gatunek': [self.gatunek, 'gatunek'], 'Produkcja': [self.kraj, 'countries'],
                             'Reżyseria': [self.rezyser, 'director']}

            def DataSearching(keyword, outputList):
                searchBegin = respDataTemp.index(keyword)
                while searchBegin < respDataTemp.index('</ul>', respDataTemp.index(keyword)):
                    gatIndexStop = respDataTemp.index('</a>', searchBegin)
                    gatIndexStart = respDataTemp.index('>', gatIndexStop - 35) + 1
                    if '<' not in respDataTemp[gatIndexStart:gatIndexStop] and ',' not in respDataTemp[gatIndexStart:
                    gatIndexStop] and respDataTemp[gatIndexStart:gatIndexStop].count(' ') < 2 and len(respDataTemp[gatIndexStart:gatIndexStop]) > 0:
                        outputList.append(respDataTemp[gatIndexStart:gatIndexStop])
                    searchBegin = gatIndexStop + len('</a></li></ul>')

            for name in movieTempDict:
                try:
                    DataSearching(movieTempDict[name][1], movieTempDict[name][0])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(red + str(e) + end + " " + name + " in movie: " + red + respDataTemp[respDataTemp.index('<title>') + len('<title>'):
                              respDataTemp.index('<title>') + len('<title>') + len(szukanaFraza)] + end)
                    print(exc_type, exc_tb.tb_lineno)

            return self.gatunek, self.kraj, self.rezyser

        # Getting movie description
        def movieDesc(self):
            try:
                descStart = respDataTemp.index('"text">', respDataTemp.index('filmPlot')) + len('"text">')
                descStop = respDataTemp.index('<', descStart)
                movieDesc = [respDataTemp[descStart:descStop]]
            except Exception:
                movieDesc = ['Ten film nie ma jeszcze zarysu fabuły...']
            return movieDesc

        def cast(self):
            # Moving to the cast URL
            URLChanging(castURL)
            respDataTemp = respData[50000:]
            # Getting cast data
            cast = []
            searchBegin = respDataTemp.index('/cast/crew">twórcy')
            actorStart = respDataTemp.index('person/', searchBegin) + len('person/')
            actorStop = respDataTemp.index('",', actorStart)
            for actor in range(3):
                cast.append(respDataTemp[actorStart:actorStop])
                cast[actor] = cast[actor].replace('.', ' ')
                cast[actor] = cast[actor].replace('+', ' ')
                try:
                    actorStart = respDataTemp.index('person/', actorStop) + len('person/')
                    actorStop = respDataTemp.index('",', actorStart)
                except:
                    actorStart = 0
                    actorStop = 1
                if '-' in cast[actor]:
                    cast[actor] = cast[actor][0:cast[actor].index('-')]
            return cast

    # Printing
    def resultPrinting():
        print("\n")
        for key in movieDict:
            print(key + ':', end=" ")
            if len(movieDict[key]) > 1:
                for value in movieDict[key]:
                    if value != movieDict[key][-1]:
                        print(bold + value + end + ',', end=" ")
                    else:
                        print(bold + value + end)
            else:
                if key == 'Długość':
                    print(bold + str(movieDict[key][0] // 60) + ' godz. ' + str(movieDict[key][0] % 60) + ' min.' + end)
                elif key == 'Filmweb link':
                    print(movieDict[key][0])
                elif key == 'Opis':
                    print('\n' + movieDict[key][0])
                else:
                    print(bold + movieDict[key][0] + end)

        # print("Całość: " + str(round(time.time() - start, 2)) + " [s]")
        # print('\n')
        # print(200 * '+' + '\n')

    szukanaFraza = movie_title  # 'Most szpiegów'
    if ' -' in szukanaFraza:
        szukanaFraza = szukanaFraza.replace(' -', ':')

    # Searching in DB
    szukanaFrazaEn = up.urlencode({szukanaFraza: ''})
    internetDateBaseURL = 'http://www.filmweb.pl/search?q='+szukanaFrazaEn[0:-1]

    URLChanging(internetDateBaseURL)

    respDataTemp = respData
    respDataTemp = respDataTemp[28000:respDataTemp.index('getToKnowClick')]
    respDataReduced = respDataTemp
    removedIndexes = 0

    try:
        titleIndexStop = respDataTemp.index('</h3>')
        titleIndexStart = respDataTemp.index('title">', titleIndexStop-100) + len('title">')
        charAmountInput = {}
        for character in szukanaFraza:
            charAmountInput[character] = szukanaFraza.count(character)

        avaibleTargets = {}

        # Searching for proper title URL
        continueSearching = True

        while continueSearching:
            charAmountTarget = {}
            corelation1 = 0
            corelation2 = 0

            if len(respDataReduced[titleIndexStart:titleIndexStop]) > 2:
                for character in respDataReduced[titleIndexStart:titleIndexStop]:
                    charAmountTarget[character] = respDataReduced[titleIndexStart:titleIndexStop].count(character)

                for character in charAmountTarget:
                    if character in charAmountInput and charAmountTarget[character] == charAmountInput[character]:
                        corelation1 += 1

                for character in charAmountInput:
                    if character in charAmountTarget and charAmountTarget[character] == charAmountInput[character]:
                        corelation2 += 1

                corelation1 = round((corelation1 / (len(respDataReduced[titleIndexStart:titleIndexStop])+0.0001)), 4)
                corelation2 = round(corelation2 / len(szukanaFraza), 4)
                corelation = (corelation1 + corelation2) / 2
                # print(respDataReduced[titleIndexStart:titleIndexStop] + ': ' + str(round(corelation*100, 2)) + '%')
                if corelation > 0.3 and respDataReduced[titleIndexStart:titleIndexStop] not in avaibleTargets:
                    avaibleTargets[respDataReduced[titleIndexStart:titleIndexStop]] = [corelation, titleIndexStart, removedIndexes]

            try:
                while True:
                    respDataReduced = respDataReduced[titleIndexStop+5:]
                    removedIndexes = removedIndexes + titleIndexStop + 5
                    titleIndexStop = respDataReduced.index('</h3>') #, titleIndexStop + len('</h3>'))
                    titleIndexStart = respDataReduced.index('title">') + len('title">')
                    if abs(titleIndexStop - titleIndexStart) < 100 \
                            and '="' not in respDataReduced[titleIndexStart:titleIndexStop]\
                            and '</' not in respDataReduced[titleIndexStart:titleIndexStop]:
                        break

            except Exception as e:
                continueSearching = False

        tempScore = 0
        # print(avaibleTargets)
        for posibl in avaibleTargets:
            if avaibleTargets[posibl][0] > tempScore:
                titleIndexStart = avaibleTargets[posibl][1] + avaibleTargets[posibl][2]
                tempScore = avaibleTargets[posibl][0]
        movieIndexStart = respDataTemp.index('href="', titleIndexStart - 100) + len('href="')
        movieIndexStop = respDataTemp.index('"><h3', movieIndexStart)
        # print(respData[movieIndexStart:movieIndexStop])
        movieURL = ['http://www.filmweb.pl' + respDataTemp[movieIndexStart:movieIndexStop]]
        castURL = movieURL[0] + '/cast/actors'

    except Exception as e:
        print(red + 'Failed to find: ' + end + szukanaFraza)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # print(e)
        # print(exc_type, exc_tb.tb_lineno)
        movieDict = {'Tytuł': [szukanaFraza], 'Długość': [], 'Premiera': [], 'Gatunek': [],
                     'Produkcja': [], 'Reżyseria': [], 'Obsada': [], 'Filmweb link': [], 'Opis': []}
        # print("Całość: " + str(round(time.time() - start, 2)) + " [s]")
        # print(200 * '+' + '\n')
        return False, 'n_in_db'
    # print("Szukanie tytułu: " + str(round(time.time() - start, 2)) + " [s]")

    if chceck_in_db(movieTB, 'filmweb_link', movieURL[0], cursor):
        return False, 'in_db'
    URLChanging(movieURL[0])
    respDataTemp = respData[60000:]
    if passit:
        try:
            film = FilmKlasa()
            film.Gatunek_Produkcja_Rezyseria()
        except Exception as e:
            return False, 'n_in_db'
        # Creating final dictionary
        movieDict = {'Tytuł': film.tytul(), 'Długość': film.czasTrwania(), 'Premiera': film.rokProdukcji(),
                     'Gatunek': film.gatunek, 'Produkcja': film.kraj, 'Reżyseria': film.rezyser, 'Obsada': film.cast(),
                     'Filmweb link': movieURL, 'Opis': film.movieDesc()}
        for name in movieDict:
            if movieDict[name] == []:
                movieDict[name] = ['-']
        if '"' in movieDict['Tytuł'][0]:
            movieDict['Tytuł'][0] = movieDict['Tytuł'][0].replace('"', "'")
        if '"' in movieDict['Opis'][0]:
            movieDict['Opis'][0] = movieDict['Opis'][0].replace('"', "'")
        resultPrinting()
        return True, 'n_in_db'

    else:
        movieDict = {'Tytuł': [szukanaFraza], 'Długość': [], 'Premiera': [], 'Gatunek': [],
                     'Produkcja': [], 'Reżyseria': [], 'Obsada': [], 'Filmweb link': [], 'Opis': []}
        return False, 'n_in_db'


def saving_into_file(wholeList):
    # Preparing file
    while True:
        try:
            saveFile = open('Output.csv', 'w')
            saveFile.close()
            break
        except Exception:
            os.system("TASKKILL /IM EXCEL.EXE")
            time.sleep(1)

    for printTitles in wholeList[0]:
        saveFile = open('Output.csv', 'a')
        saveFile.write(printTitles + ';')
    saveFile.write('\n\n')
    saveFile.close()

    # Saving data
    saveFile = open('Output.csv', 'a')

    for movieDict1 in wholeList:
        for key in movieDict1:

            if len(movieDict1[key]) > 1:
                for value in movieDict1[key]:
                    saveFile.write(str(value))
                    if value != movieDict1[key][-1]:
                        saveFile.write(', ')
                saveFile.write(';')
            elif movieDict1[key] != []:
                if key == 'Długość':
                    saveFile.write(str(movieDict1[key][0] // 60) + ' godz. ' + str(movieDict1[key][0] % 60) +
                                   ' min.' + ';')
                else:
                    saveFile.write(str(movieDict1[key][0]) + ';')
        saveFile.write('\n')
    saveFile.close()
    os.system("E:\Studia\Python\Output.csv")


def screenshot_taking(film, desc_len):
    try:
        desc_len = len(desc_len[0])
        time.sleep(0.33)
        im = PIL.ImageGrab.grab(bbox=(80, 800, desc_len*7.87, 990))
        os.chdir(path + "\\" + film)
        # os.chdir("C:\\Users\\Rafal\\Desktop")
        im.save(film + ".png")
    except Exception as e:
        print("Exception in screentshot taking function: " + str(e))
        pass



'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


def main():
    print("*** " + bold + "THE PROGRAM HAS STARTED" + end + " ***\n")
    err_file = open('Output_err.txt', 'w')
    err_file.close()
    Astart = time.time()
    mydb = Connect_with_SQL()
    cursor = mydb.cursor()
    hdd_searching(path)
    # movieList = ["Piekło Pocztowe", "Most szpiegów", "Hudson Hawk", "Szklana pułapka 4", "Kiler", "Wilk"]
    # movieList = ["Niemożliwe"]
    wholeList = []
    for film in movieList[0:]:
        global start
        start = time.time()
        if not chceck_in_db(movieTB, 'title', film, cursor):
            res_internet_searching = internet_searching(film, cursor)
            if res_internet_searching[0]:
                if len(wholeList) == 0 or movieDict != wholeList[-1]:
                    wholeList.append(movieDict)
                screenshot_taking(film, movieDict['Opis'])
                insert_into_db(movieDict, cursor, mydb)
                print(200 * '+')
            elif res_internet_searching[1] == 'in_db':
                print('Movie ' + bold + film + end + ' already exists in DataBase')
            else:
                err_file = open('Output_err.txt', 'a')
                err_file.write(film + '\n')
                err_file.close()
        else:
            print('Movie ' + bold + film + end + ' already exists in DataBase')

    # saving_into_file(wholeList)
    print(bold + "\nExecution time: " + end + str(round(time.time() - Astart, 2)) + " [s].", bold, "New movies amount: "
          + end + str(len(wholeList)))
    os.chdir("E:\\Studia\\Python")


main()

