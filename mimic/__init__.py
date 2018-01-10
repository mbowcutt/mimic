import os
from flask import Flask
#import logging

# Initialize app
app = Flask(__name__)
app.secret_key=os.urandom(24)
#logging.basicConfig(filename='mimic/app.log',level=logging.INFO)

from mimic.routes import *

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app.run()
