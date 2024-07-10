from flask import Flask, render_template

sachin = Flask(__name__)

@sachin.route("/")
def index():
    return "welcome"

@sachin.route("/grras/")
def grras():
    return "grras "

@sachin.route("/form/")
def form():
    return render_template("form.html")

@sachin.route("/info/<name>/<city>/<int:age>/<course>/")
def info(name, city, age, course):
    
    information={
        "NAME":name,
        "CITY":city,
        "AGE":age,
        "COURSE":course
    }
    return render_template("info.html", information=information)

if __name__ == "__main__":
    sachin.run(debug=True, passthrough_errors=True, use_debugger=False, use_reloader=False)
