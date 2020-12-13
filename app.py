from flask import Flask, render_template, request, get_template_attribute, url_for
from werkzeug.utils import secure_filename
import os
from render import buildFileSplit, getPage, translatePath


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))+"//upload"


@app.route("/")
def index():
    return render_template("index.html", logList=getLogNames())





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



@app.route('/logs/<logName>/<int:page>')
def logView(logName, page):
    logHtml = getPage(os.path.join(app.config['UPLOAD_FOLDER'], logName), page)
    nOP = getNumberOfPages(logName)
    return render_template('log_view.html', logName=logName, logHtml=logHtml, numOfPages=nOP)




def getLogNames():
    def filterfunc(x):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],x)):
            return 1
        else:
            return 0
    
    files =  os.listdir(app.config['UPLOAD_FOLDER'])
    f_files = filter(filterfunc, files)
    return list(f_files)



def getNumberOfPages(logName):
   new_path = translatePath(os.path.join(app.config['UPLOAD_FOLDER'], logName))
   return len(os.listdir(new_path))


if __name__ == '__main__':
    app.run(debug=True)
    

