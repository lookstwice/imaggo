from doctest import Example
from email.policy import default
import base64
import os

from itsdangerous import base64_encode

from flask import Flask, request
from flask_restx import Api, Resource, fields
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

example_url = (f'https://www.publicdomainpictures.net/en/view-image.php?'
               f'image=356071&picture=dog-under-table')
example_data = base64_encode("TEST_DATA").decode("utf-8")

request_model = api.model('POST', {
    'label': fields.String(title="label", description='image label',
                           example="example.jpg", required=False),
    'data': fields.String(title="data", description='image data',
                          example=example_data, required=False),
    'image_url': fields.Url(title="image url", example=example_url,
                            required=False),
    'detection_flag': fields.String(title="detection flag", example="True",
                                    required=False),
})


@api.route('/images', methods=['GET', 'POST'])
class Images(Resource):
    @api.doc(model=request_model)
    @api.doc(responses={200: 'Success', 400: 'Bad Request'})
    def post(self):
        handler = Request_Handler()
        request_body = request.get_json()

        if request_body:
            image_data = request_body.get('data')
            image_url = request_body.get("image_url")
            
            if image_data:
                response = handler.detect_objs(request_body)
                return response
            elif image_url:
                response = handler.detect_objs_by_url(request_body)
                return response
            else:
                abort(400, (f"provide 'image_data' or 'image_url' in the json "
                            "body of the request"))
        else:
            abort(400, f'json request body: {request_body}')
            
    @api.param("objects", "obj1,obj2,obj3", _in="query")
    @api.doc(responses={200: 'Success'})
    def get(self):
        handler = Request_Handler()
        if request.args:
            response = handler.get_images(request.args)
            return response
        else:
            response = handler.get_images()
            return response


@api.route('/images/<imageId>', methods=['GET'])
class ImagesByID(Resource):
    @api.param("imageId", "image identifier", type=int, _in="path")
    @api.doc(responses={200: 'Success'})
    def get(self, imageId):
        handler = Request_Handler()
        response = handler.get_images(id=imageId)
        return response


if __name__ == '__main__':
    app.run(debug=True)
