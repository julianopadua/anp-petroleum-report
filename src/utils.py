# utils.py

import os
import yaml

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # build full paths
    for key in config.get('paths', {}):
        config['paths'][key] = os.path.join(script_dir, config['paths'][key])

    return config
