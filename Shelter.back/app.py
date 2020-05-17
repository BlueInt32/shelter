from flask import Flask
import logging
from flask_restful import Api
from flask_cors import CORS
from models import db
from endpoints.elements import ElementsListApi
from endpoints.element_detail import ElementDetailApi
from endpoints.element_file import ElementFileApi, ElementThumbnailFileApi
from endpoints.image_links_api import ImageLinksApi
from endpoints.image_files_api import ImageFilesApi
from endpoints.video_links_api import VideoLinksApi
from endpoints.video_files_api import VideoFilesApi
from endpoints.web_links_api import WebLinksApi
from endpoints.tags import TagsSearchApi
from flask import got_request_exception


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


def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug('Got exception during processing: %s', exception)
    print(exception)


got_request_exception.connect(log_exception, app)

api.add_resource(ElementsListApi, '/api/elements')
api.add_resource(ImageLinksApi, '/api/image-links')
api.add_resource(ImageFilesApi, '/api/image-files')
api.add_resource(VideoLinksApi, '/api/video-links')
api.add_resource(VideoFilesApi, '/api/video-files')
api.add_resource(WebLinksApi, '/api/web-links')
api.add_resource(ElementDetailApi, '/api/elements/<element_id>')
api.add_resource(ElementFileApi, '/api/elements/file/<element_id>')
api.add_resource(ElementThumbnailFileApi,
                 '/api/elements/thumbnail/<element_id>')
api.add_resource(TagsSearchApi, '/api/tags/search/<search_term>')

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=4996)
