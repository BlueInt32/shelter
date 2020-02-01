from flask import Flask
import logging
from flask_restful import  Api
from flask_cors import CORS
from models import db
import endpoints


app = Flask(__name__)

if app.config["ENV"] == "production":
  app.config.from_object("config.ProductionConfig")
else:
  app.config.from_object("config.DevelopmentConfig")

logging.basicConfig(
  format='%(asctime)s %(message)s',
  filename='shelter.log',
  level=logging.INFO,
  datefmt='%m/%d/%Y %I:%M:%S %p')

db.init_app(app)

logging.info('app start')
print(f'ENV is set to: {app.config["ENV"]}')

api = Api(app)
cors = CORS(app)


api.add_resource(endpoints.ElementsListApi, '/api/elements')
api.add_resource(endpoints.ElementApi, '/api/elements/<element_id>')

if __name__ == '__main__':
  app.debug = True
  app.run()
  # app.run(host='0.0.0.0', port=4996)
