from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_schedule")
def add_schedule():
    return render_template("wis_input.html")


@app.route("/view_schedule")
def view_schedule():
    return render_template("wis_result.html")


@app.route("/add_materials_list")
def add_materials_list():
    return render_template("kns_input.html")


@app.route("/view_materials_list")
def add_materials_list():
    return render_template("kns_result.html")


if __name__ == '__main__':
    app.run(debug=True)
