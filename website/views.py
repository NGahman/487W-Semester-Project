from sysconfig import get_path
from flask import Blueprint, render_template, Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
import os

UPLOAD_FOLDER = "C:\\Users\\scott\\OneDrive\\Documents\\MinorProject\\website\\UPLOAD_FOLDER" #   <---- change depending on desired upload folder path
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == ('POST'):
        print("POSTED")

        # check if the post request has the file part
        print(request.files)
        if 'transcript_input' not in request.files:
            print("No file part")
            flash('No file part')
            return redirect(request.url)
        file = request.files['transcript_input']

        if file.filename == '':
            print("No selected file")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("Processing...")
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  <--- this would allow the pdf to be saved somewhere
            #file = open(data, 'rb')
            fileReader = PyPDF2.PdfFileReader(file)
            page = fileReader.pages[0]
            print("PDF Text: ")
            print(page.extract_text())
            print("---END PDF---")
        
    return render_template("index.html")
