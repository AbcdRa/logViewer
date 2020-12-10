from flask import Flask, render_template, request, get_template_attribute, url_for
from werkzeug.utils import secure_filename
import os
from render import render_table


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))+"//upload"




def getLogNames():
    return os.listdir(app.config['UPLOAD_FOLDER'])



@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html', message="")
    elif request.method == "POST":
        f = request.files["logfile"]
        if f.filename in getLogNames():
            message = "Не удалось заргузить лог " + f.filename + ", лог с таким именем существует "
        else:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            message = "Лог " + f.filename + " успешно загружен"
        return render_template("upload.html", message=message)

@app.route('/<logName>')
def main():
    logList = getLogNames()
    return render_template('index.html', logList=logList)




if __name__ == '__main__':
    app.run(debug=True)
    

