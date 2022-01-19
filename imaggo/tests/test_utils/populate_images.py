#!/usr/bin/env python
import os
import sys

from imaggo.common.images_client import ImagesClient
from imaggo.common.utils import Utilities

if __name__ == '__main__':
    temp_entry = None

    dc = ImagesClient()
    Utilities.check_server(dc)

    if len(sys.argv) != 2:
        print("missing image directory")
        sys.exit(1)
    else:
        image_dir = sys.argv[1]

    if not os.path.isdir(image_dir):
        print(f'{image_dir} does not exist')
        sys.exit(1)
    else:
        dir = os.scandir(image_dir)
        for dir_entry in dir:
            temp_entry = dir_entry

            # with label and detection enabled
            payload = {"label": dir_entry.name,
                       "detection_flag": "True"}
            response = dc.detect_objs(request_body=payload,
                                      file_path=dir_entry.path)
            print(response.status_code)
            print(response.json())

    # without label and detection disabled
    payload = {"detection_flag": "False"}
    response = dc.detect_objs(request_body=payload,
                              file_path=temp_entry.path)
    print(response.status_code)
    print(response.json())

    # without label and detection enabled
    payload = {"detection_flag": "True"}
    response = dc.detect_objs(request_body=payload,
                              file_path=temp_entry.path)
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
    url = (f'https://www.publicdomainpictures.net/en/view-image.php?'
           f'image=384460&picture=tank-amx-30')
    label = url.split("picture=")[-1]
    payload = {"label": label,
               "image_url": url,
               "detection_flag": "True"}
    response = dc.detect_objs(request_body=payload)
    print(response.status_code)
    print(response.json())
