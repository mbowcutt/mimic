import os
from flask import Flask

# Initialize app
app = Flask(__name__)
app.secret_key=os.urandom(24)

from mimic.routes import *

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app.run()
