import base64
import requests

FLASK_ENDPOINT = 'http://127.0.0.1:5000'


class ImagesClient:
    def _retrieve_image_data(self, base_endpoint, id="", params={}):
        if params:
            response = requests.get(f'{FLASK_ENDPOINT}{base_endpoint}',
                                    params=params)
        else:
            response = requests.get(f'{FLASK_ENDPOINT}{base_endpoint}{id}')
        return response

    def retrieve_all_image_data(self):
        return self._retrieve_image_data('/images')

    def retrieve_image_data_by_tags(self, params={}):
        return self._retrieve_image_data('/images', params=params)

    def retrieve_image_data_by_id(self, id):
        return self._retrieve_image_data('/images/', id=id)

    def _with_file(self, request_body, file_path):
        with open(file_path, 'rb') as file_obj:
            data = base64.b64encode(file_obj.read())
            request_body['data'] = data.decode("utf-8")
        response = requests.post(f'{FLASK_ENDPOINT}/images',
                                 json=request_body)

        return response

    def _with_url(self, request_body):
        response = requests.post(f'{FLASK_ENDPOINT}/images', json=request_body)
        return response

    def detect_objs(self, request_body, file_path=None):
        if file_path:
            response = self._with_file(request_body, file_path)
            return response
        else:
            response = self._with_url(request_body)
            return response
