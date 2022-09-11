from sysconfig import get_path
from flask import Blueprint, render_template, request
import PyPDF2

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == ('POST'):
        print("POSTED")
        data = request.form.get('transcript_input')
        print(data)
        if data is None:
            print("File seen as NoneType")
        else:
            #file = open(data, 'rb')
            fileReader = PyPDF2.PdfFileReader(data)
            page = fileReader.pages[0]
            print(page.extract_text())
        
    return render_template("index.html")