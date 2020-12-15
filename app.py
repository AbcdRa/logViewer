import os
from flask import Flask, render_template
from flask import request, get_template_attribute
from flask import url_for, redirect
from werkzeug.utils import secure_filename
from render import buildFileSplit, getPage, translatePath


#Создаем приложение и назначаем папку для загруженных логов
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))+"//upload"


#Рендерим начальную страницу
@app.route("/")
def index():
    return render_template("index.html", logList=getLogNames())


#Логика загрузки файла
@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html', message="")
    elif request.method == "POST":
        f = request.files["logfile"]
        if f.filename in getLogNames():
            message = "Не удалось заргузить лог " + f.filename + ", лог с таким именем существует "
        else:
            new_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(new_path)
            message = "Лог " + f.filename + " успешно загружен"
            buildFileSplit(new_path)
        return render_template("upload.html", message=message)


#Переменные для восстановления текущего просматриваемого лога
currentPage = 0
currentName = ""


#Логика просмотра лога
@app.route('/logs/<logName>/<int:page>')
def logView(logName, page):
    global currentPage, currentName
    currentPage = page
    currentName = logName

    logHtml = getPage(os.path.join(app.config['UPLOAD_FOLDER'], logName), page)

    nOP = getNumberOfPages(logName)
    pSR = pageSelectorRange(page, nOP)
    logInfo = {"logHtml":logHtml, "numOfPages":nOP, "logName":logName, "currentPage":page, "pSR":pSR}
    return render_template('log_view.html', logInfo=logInfo)


#Восстановление текущего лога
@app.route('/relative')
def relative():
    global currentPage, currentName
    if currentPage == 0 or currentName =="":
        return redirect("/")
    else:
        return redirect("/logs/"+currentName+"/"+str(currentPage))
    




def getLogNames():
    def filterfunc(x):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],x)):
            return 1
        else:
            return 0
    
    files =  os.listdir(app.config['UPLOAD_FOLDER'])
    f_files = filter(filterfunc, files)
    return list(f_files)


#Вернуть количество стрвниц лога
def getNumberOfPages(logName):
   new_path = translatePath(os.path.join(app.config['UPLOAD_FOLDER'], logName))
   return len(os.listdir(new_path))


#Вернуть page selector
def pageSelectorRange(currentPage, numOfPages):
    DEFAULT_RANGE = 5

    startPoint = currentPage-DEFAULT_RANGE
    startPoint = startPoint if startPoint>1 else 1
    endPoint = currentPage+DEFAULT_RANGE
    endPoint = endPoint if endPoint<numOfPages else numOfPages
    return range(startPoint, endPoint+1)


#Запускаем приложение
if __name__ == '__main__':
    app.run(debug=True)
    

