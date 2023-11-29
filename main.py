import os
import time
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv, dotenv_values

import openai

openai.api_key = "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"

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
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response)
            data = {"question": question, "answer": response.choices[0].text}
            mongo.db.chats.insert_one({"question": question, "answer": response.choices[0].text})
            return jsonify(data)
    data = {"result": "Thank you I am just a machine"}

    return jsonify(data)

app.run(debug=True)