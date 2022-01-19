#!/usr/bin/env python
from imaggo.common.images_client import ImagesClient
from imaggo.common.utils import Utilities

if __name__ == '__main__':
    dc = ImagesClient()
    Utilities.check_server(dc)

    response = dc.retrieve_all_image_data()
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_tags(params={'objects': "sun,wind"})
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_tags(params={'objects': "danger"})
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_id(3)
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_id(98)
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_tags(params={'objects': "HEB"})
    print(response.status_code)
    print(response.json())

    response = dc.retrieve_image_data_by_tags(params={'objects': ""})
    print(response.status_code)
    print(response.json())
