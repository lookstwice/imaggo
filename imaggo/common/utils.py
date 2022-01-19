import sys
import uuid
from datetime import datetime
from time import time

import magic
import requests


class Utilities:
    @staticmethod
    def check_server(client):
        try:
            client.retrieve_image_data_by_id(id="")
        except requests.exceptions.ConnectionError:
            print("Flask Server Is Not Running")
            sys.exit(1)

    @staticmethod
    def get_mime_type(file_path):
        try:
            mime_type = magic.from_file(file_path).split(" ")[0]
        except (FileNotFoundError, IndexError):
            return None
        return mime_type

    @staticmethod
    def name_gen(name_base="image"):
        epoch_time = time()
        month_year = datetime.fromtimestamp(epoch_time).strftime('%m_%Y')
        return (f'{name_base.replace(".", "_")}_{month_year}_'
                f'{str(epoch_time).replace(".", "_")}')

    @staticmethod
    def id_gen(id_base="image"):
        return "-".join([id_base.replace(".", "-"), str(uuid.uuid4())])
