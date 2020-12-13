import os
#Создает html-таблицу из файла
SPLITTER = [[0, 19],[21, 45], [46, 57]]
MAX_NUM_ROWS = 100




def line2htmlRow(line):
    if len(line) > 57:
        S = SPLITTER
        outline = "<tr>"
        for i in range(0,len(S)):
            outline += "<td>" + line[S[i][0]:S[i][1]].strip() + "</td>"
        #Последний столбец не имеет фиксированной длины и идет до конца
        outline += "<td>" + line[S[len(S)-1][1]:].strip() + "</td></tr>\n"
        return outline
    return ""



def buildFileSplit(path):
    basename = os.path.basename(path).replace(".","_")
    dirname = os.path.dirname(path)

    new_path = os.path.join(dirname, basename)

    if os.path.exists(new_path) and os.path.isdir(new_path):
        return True
    else:
        os.mkdir(new_path)

    page_num = 1

    with open(path) as file_handler:
        line = "test"
        while line != "":
            with open(os.path.join(new_path, str(page_num)+".tmp"), "w") as new_file:
                for _ in range(0, MAX_NUM_ROWS): 
                    line = file_handler.readline()
                    new_line = line2htmlRow(line)
                    new_file.write(new_line)
                page_num += 1


def getPage(path, page):
    basename = os.path.basename(path).replace(".","_")
    dirname = os.path.dirname(path)

    new_path = os.path.join(dirname, basename)

    with open(os.path.join(new_path, str(page)+".tmp"), "r") as f:
        return f.read()