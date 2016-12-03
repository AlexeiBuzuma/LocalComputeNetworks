import logging
import json
import os

from sft.constants import APP_DATA_DIR


LOG = logging.getLogger(__name__)
STORAGE_PATH = os.path.join(APP_DATA_DIR, '.client_data.json')


def save_client_data(data_dict):
    try:
        with open(STORAGE_PATH, 'w') as outfile:
            json.dump(data_dict, outfile)
    except Exception as e:
        LOG.warning("Couldn't save client state: %r" % e)


def load_client_data():
    try:
        with open(STORAGE_PATH, 'r') as infile:
            data_dict = json.load(infile)
        return data_dict
    except Exception:
        pass
    return None


def delete_client_data():
    try:
        os.remove(STORAGE_PATH)
    except OSError:
        pass
