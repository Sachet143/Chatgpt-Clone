from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["GET", "POST"])
def qa():
    data = {"result": "Hey"}
    if request == "POST":
        return jsonify(data)
    return jsonify(data)
    # return render_template("index.html")

app.run(debug=True)