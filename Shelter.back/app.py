from flask import Flask
import logging
from flask_restful import  Api
from flask_cors import CORS
from models import db
from endpoints.elements import ElementsListApi
from endpoints.element_detail import ElementApi
from endpoints.tags import TagsSearchApi


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


api.add_resource(ElementsListApi, '/api/elements')
api.add_resource(ElementApi, '/api/elements/<element_id>')
api.add_resource(TagsSearchApi, '/api/tags/search/<search_term>')

if __name__ == '__main__':
  app.debug = True
  app.run()
  # app.run(host='0.0.0.0', port=4996)
