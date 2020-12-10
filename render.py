#Создает html-таблицу из файла
SPLITTER = [[0, 18],[21, 48], [48, 57]]
NUM_LINES_ON_PAGE = 100

#path-путь до файла
def render_table(path, i=1):
    with open(path) as file_handler:
        outHtml = "<table>"
        for line in file_handler:
            outHtml += line2htmlRow(line)
        return outHtml+"</table>"


def line2htmlRow(line):
    if len(line) > 57:
        S = SPLITTER
        outline = "<tr>"
        for i in range(0,len(S)):
            outline += "<td>" + line[S[i][0]:S[i][1]].strip() + "</td>"
        #Последний столбец не имеет фиксированной длины и идет до конца
        outline += "<td>" + line[S[len(S)-1][1]:].strip() + "</td></tr>"
        return outline
    return ""



