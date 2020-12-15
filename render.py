#Импортируем модуль os, для работы с директориями и путями  
import os


SPLITTER = [[0, 19],[21, 40], [42, 48]]
MAX_NUM_ROWS = 100


#Превращаем необработанную строку в сроку Html,
def line2htmlRow(line):
    #Если строка меньше 57, то скорее всего там только сообщение
    if len(line) < 57:
        pass
        return "<tr><td></td><td></td><td></td><td>"+line+"</td></tr>\n"
    #Иначе делим на столбцы, используя информацию из сплиттера
    else:    
        S = SPLITTER
        outline = "<tr>"
        for i in range(0,len(S)):
            outline += "<td>" + line[S[i][0]:S[i][1]].strip() + "</td>"
        #Последний столбец не имеет фиксированной длины и идет до конца
        outline += "<td>" + line[S[len(S)-1][1]:].strip() + "</td></tr>\n"
        return outline
    return ""



#Делим лог на страницы
def buildFileSplit(path):
    new_path = translatePath(path)

    if os.path.exists(new_path) and os.path.isdir(new_path):
        return True
    else:
        os.mkdir(new_path)

    page_num = 1

    with open(path) as file_handler:
        line = "test"
        startPoint = findStartPoint(file_handler)
        file_handler.seek(startPoint)
        while line != "":
            with open(os.path.join(new_path, str(page_num)+".tmp"), "w") as new_file:
                for _ in range(0, MAX_NUM_ROWS): 
                    line = getLine(file_handler)
                    if line == "": break
                    new_line = line2htmlRow(line)
                    new_file.write(new_line)

                page_num += 1


#Вернуть страницу лога
def getPage(path, page):
    new_path = translatePath(path)

    with open(os.path.join(new_path, str(page)+".tmp"), "r") as f:
        return f.read()

        
#Преобразовать из имени лога, путь до папки с обработанными страницами
def translatePath(path):
    basename = os.path.basename(path).replace(".","_")
    dirname = os.path.dirname(path)
    new_path = os.path.join(dirname, basename)
    return new_path


#Получить строку из файла
def getLine(file_handler):
    ch = file_handler.read(1)
    line = ""
    while ch != "" and ch != "\n":
        line += ch
        ch = file_handler.read(1)
    return line


#Получить начало лога, некоторые логи читают с начала мусорные байты
def findStartPoint(file_handler):
    ch = file_handler.read(1)
    startByte = 0
    while not ch.isdigit():
        ch = file_handler.read(1)
        startByte += 1
    return startByte