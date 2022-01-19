import base64
import json
import os

import requests
from flask import jsonify

from common.utils import Utilities
from db import Image, Object, db

IMAGGA_TAGS_ENDPOINT = "https://api.imagga.com/v2/tags"
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]


class Request_Handler():
    def insert_tags(self, image, response):
        tag_list = []

        response_dict = json.loads(response.content.decode('utf-8'))

        result = response_dict.get('result')
        if result:
            tag_list = result.get('tags')

        for current in tag_list:
            tag = current.get('tag').get('en')
            object = Object(name=tag)
            image.objects.append(object)
            db.session.commit()

    def insert_image(self, db, label=None, data=None):
        data_payload = None
        if not label:
            label = Utilities.name_gen()

        if data:
            data_payload = data.encode()

        image = Image(data=data_payload, label=label)
        db.session.add(image)
        db.session.commit()

        return image

    def detect_objs(self, request_body):
        label = request_body.get("label")
        image_data = request_body.get('data')

        image = self.insert_image(db, label=label, data=image_data)

        detection_flag = request_body.get('detection_flag')
        if detection_flag:
            if detection_flag.upper() == "TRUE":
                response = requests.post(
                    IMAGGA_TAGS_ENDPOINT,
                    auth=(API_KEY, API_SECRET),
                    data={'image': base64.b64decode(image_data.encode())})

                self.insert_tags(image, response)

        return jsonify(image=image.to_dict())

    def detect_objs_by_url(self, request_body):
        label = request_body.get("label")

        image = self.insert_image(db, label=label)

        detection_flag = request_body.get('detection_flag')
        if detection_flag:
            if detection_flag.upper() == "TRUE":
                image_url = request_body.get("image_url")
                response = requests.get(
                    f'{IMAGGA_TAGS_ENDPOINT}?image_url={image_url}',
                    auth=(API_KEY, API_SECRET))

                self.insert_tags(image, response)

        return jsonify(image=image.to_dict())

    def get_images(self, args=None, id=None):
        if args:
            filters = args.to_dict().get('objects').split(",")

            obj_match = Object.query.filter(Object.name.in_(filters))

            results = [f'{Image.query.get(obj.image_id)} tag={obj.name}'
                       for obj in obj_match]

            return jsonify(results=results)
        elif id:
            image = Image.query.get(id)
            if image:
                return jsonify(image=image.to_dict())
            return jsonify("{}")
        else:
            all_images = Image.query.all()

            results = [img.to_dict() for img in all_images]

            return jsonify(images=results)
