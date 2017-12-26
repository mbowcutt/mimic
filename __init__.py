from flask import Flask
import markovify
app = Flask(__name__)

@app.route("/")
def mimicme():
    return "OK"

@app.route("/read")
def read():
    return "read"

@app.route("/speak")
def speak():
    return "spoke"

@app.route("/upload")
def upload():
    return "upload"

if __name__ == "__main__":
    app.run()