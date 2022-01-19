from os import environ

from imaggo.common.images_client import ImagesClient
from imaggo.common.utils import Utilities


class TestImages:
    @classmethod
    def setup_class(cls):
        cls.dc = ImagesClient()
        Utilities.check_server(cls.dc)

    def test_retrieve_all_image_data(self):
        response = self.dc.retrieve_all_image_data()
        assert(response.status_code == 200)
        assert(response.ok)

    def test_retrieve_image_data_by_id(self):
        response = self.dc.retrieve_image_data_by_id(id=1)
        assert(response.status_code == 200)
        assert(response.ok)

    def test_retrieve_image_data_by_tags(self):
        params = {'objects': "dog,cat"}
        response = self.dc.retrieve_image_data_by_tags(params=params)
        assert(response.status_code == 200)
        assert(response.ok)

    def test_detect_objs_by_path(self):
        payload = {"detection_flag": "False"}
        path = "/".join([environ['HOME'], "demo_images/robot1.jpg"])
        response = self.dc.detect_objs(request_body=payload, file_path=path)
        assert(response.status_code == 200)
        assert(response.ok)

    def test_detect_objs_by_url(self):
        url = (f'https://www.publicdomainpictures.net/en/view-image.php?'
               f'image=356071&picture=dog-under-table')
        payload = {"label": "dog-under-table",
                   "image_path": "",
                   "image_url": url,
                   "detection_flag": "True"}
        response = self.dc.detect_objs(request_body=payload)
        assert(response.status_code == 200)
        assert(response.ok)
