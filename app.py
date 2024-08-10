import os
import uuid
import main
import ProjectVariables
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = { 'txt', 'jpg' }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/")
def hello():
    # return "Hello, World!"
    return render_template("index.html")

@app.route("/user/<uuid:user_id>")
def user_page(user_id):
    with open(f'static/books/{user_id}/preview_page.html', mode='r') as f:
        page = f.read()
    return page
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        style = request.form.get('style')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_id = str(uuid.uuid4())
            book_name = filename.split('.')[0]
            os.makedirs('./static/books/' + user_id)
            path = './static/books/' + user_id + '/' + filename
            file.save(path)
            main.processing(user_uuid=user_id, book_name=book_name, style=style)
            return redirect(url_for('user_page', user_id=user_id))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Загрузка нового файла</h1>
    <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <br><br>
    <label for="style">Стиль:</label>
    <select id="style" name="style">
        <option value="KANDINSKY">Кандинский</option>
        <option value="UHD">Детальное фото</option>
        <option value="ANIME">Аниме</option>
        <option value="DEFAULT">Свой стиль</option>
    </select>
    <br><br>
    <input type=submit value=Отправить>
    </form>
    '''

app.run("0.0.0.0", "8888")