import os

from flask import Flask, request
from flask_restx import Api, Resource
from werkzeug.exceptions import abort
from werkzeug.middleware.proxy_fix import ProxyFix

from db import db
from request_handler import Request_Handler

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB_PATH = os.path.join(app.instance_path, 'imaggo.sqlite3')

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=DB_PATH,
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_PATH}'
)

db.init_app(app)

with app.app_context():
    db.create_all()

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Imaggo API',
          description=(f'A service that ingests user images, analyzes them for'
                       f' object detection, and returns the enhanced'
                       f' content.'),)

ns = api.namespace('Images', description='Image Operations')


@api.route('/images', methods=['GET', 'POST'])
class Images(Resource):
    def post(self):
        handler = Request_Handler()
        request_body = request.get_json()

        if request_body.get('data'):
            response = handler.detect_objs(request_body)
            return response
        elif request_body.get("image_url"):
            response = handler.detect_objs_by_url(request_body)
            return response
        else:
            abort(400, (f"provide 'image_data' or 'image_url' in the json "
                        "body of the request"))

    def get(self):
        handler = Request_Handler()
        if request.args:
            response = handler.get_images(request.args)
            return response
        else:
            response = handler.get_images()
            return response


@api.route('/images/<imageId>', methods=['GET'])
@api.param("imageId", "image identifier")
class ImagesByID(Resource):
    def get(self, imageId):
        handler = Request_Handler()
        response = handler.get_images(id=imageId)
        return response


if __name__ == '__main__':
    app.run(debug=True)
