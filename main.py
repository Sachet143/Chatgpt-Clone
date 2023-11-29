import os
import time
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv, dotenv_values

import bardapi

bard = bardapi.Bard()

load_dotenv()

MY_DATABASE_PASSWORD = os.getenv("MY_DATABASE_PASSWORD")

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sachet143:{}@mongoyoutube.zvwln5d.mongodb.net/chatgpt".format(MY_DATABASE_PASSWORD)
mongo = PyMongo(app)


@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats = [chat for chat in chats]
    print(mychats)
    return render_template("index.html", mychats = mychats)

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        if chat:
            data = {"result": f"{chat['answer']}"}
            return jsonify(data)
        else:
            prompt = question
            mongo.db.chats.insert_one({"question": question, "answer": bard.generate(question)})
            data = {"question": question, "answer": bard.generate(question)}
            time.sleep(2)
            return jsonify(data)
    data = {"result": "Thank you I am just a machine"}

    return jsonify(data)

app.run(debug=True)