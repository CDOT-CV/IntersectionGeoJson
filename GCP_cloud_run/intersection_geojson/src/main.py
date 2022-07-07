from flask import Flask
from flask_restful import Api
import os
import logging

log_level = os.environ.get('LOGGING_LEVEL', 'INFO')
logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

app = Flask(__name__) 
api = Api(app)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)