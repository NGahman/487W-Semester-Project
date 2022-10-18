from website import create_app
from flask import render_template

app = create_app()



if __name__ == '__main__':
    app.run(debug=True)

# @app.route("/psu") #deterrmines url extension
# def index():
#     return render_template("index.html")

# @app.route("/process", methods ["POST", "GET"]) #deterrmines url extension
# def submit():
#     transcript = request.form["transcript_input"] #may not work for saving file
#     return render_template("index.html")