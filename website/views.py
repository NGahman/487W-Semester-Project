from sysconfig import get_path
from flask import Blueprint, render_template, Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
import os
from InternalAlgorithm import *

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
            #fileReader = PyPDF2.PdfFileReader(file)
            #page = fileReader.pages[0]
            #print("PDF Text: ")
            #print(page.extract_text())
            #print("---END PDF---")
            MinorArray = getFullfillmentData(file)
            newHtml = "<br><br>"
            #below is bulk of results code. looks ugly in one line right now. should fix later for readibility
            for i, eachMinor in enumerate(MinorArray):
                newHtml += '<center><div><label for="file">'+eachMinor.name+' Progress:</label><br><label>'+ str(int(eachMinor.completion * 100)) + '%</label><progress id="file" value="' + str(int(eachMinor.completion * 100)) +'" max="100"></progress> <button onclick="expand('+ str(i) +')">Details</button><div id='+ str(i) +' style = "background-color:white; padding:50px 0; display:none"><p>Full Requirements: "' + str(list(eachMinor.fullrequirements)) +'</p><p>Completed Requirements: "' + str(list(eachMinor.completedrequirements)) +'</p><p>Remaining Requirements: "' + str(list(eachMinor.failedrequirements)) +'</p></div></div></center><br><br>'


            
        return (render_template("index.html") + newHtml)
    else:
        return (render_template("index.html"))
