import json
import os


root_dir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.expanduser(root_dir + '/config.json')
base_url = 'https://wavecountbackendapifunctionapp.azurewebsites.net/api'


def read_config():
    cfg = {}
    if not os.path.exists(filename):
        cfg['base_url'] = base_url
        with open(filename, 'w+') as cfg_file:
            json.dump(cfg, cfg_file, indent=4)
    else:
        with open(filename, 'r') as cfg_file:
            cfg = json.load(cfg_file)
    return cfg


def save_config(cfg):
    with open(filename, 'w') as cfg_file:
        return json.dump(cfg, cfg_file, indent=4)
