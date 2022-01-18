#!/usr/bin/env python
import os
import sys

from images_client import ImagesClient
from utilities import Utilities

if __name__ == '__main__':
    payload_path = ""
    file_name = ""

    dc = ImagesClient()
    Utilities.check_server(dc)

    if len(sys.argv) != 2:
        print("missing file path")
        sys.exit(1)
    else:
        payload_path = sys.argv[1]

    if not os.path.isfile(payload_path):
        print(f'{payload_path} does not exist')
        sys.exit(1)
    else:
        file_name = os.path.basename(payload_path)

    # without label and detection disabled
    payload = {"detection_flag": "False"}
    response = dc.detect_objs(request_body=payload,
                              file_path=payload_path)
    print(response.status_code)
    print(response.json())

    # without label and detection enabled
    payload = {"detection_flag": "True"}
    response = dc.detect_objs(request_body=payload,
                              file_path=payload_path)
    print(response.status_code)
    print(response.json())

    # with label and detection enabled
    payload = {"label": file_name,
               "detection_flag": "True"}
    response = dc.detect_objs(request_body=payload,
                              file_path=payload_path)
    print(response.status_code)
    print(response.json())

    # without label and detection disabled
    url = "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
    payload = {"image_url": url,
               "detection_flag": "False"}
    response = dc.detect_objs(request_body=payload)
    print(response.status_code)
    print(response.json())

    # without label and detection enabled
    url = "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
    payload = {"image_url": url,
               "detection_flag": "True"}
    response = dc.detect_objs(request_body=payload)
    print(response.status_code)
    print(response.json())

    # with label and detection enabled
    url = "https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
    payload = {"label": "wind-farm-538576_640.jpg",
               "image_url": url,
               "detection_flag": "True"}
    response = dc.detect_objs(request_body=payload)
    print(response.status_code)
    print(response.json())
