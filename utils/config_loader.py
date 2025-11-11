import yaml 
import os 
from typing import Dict

def load_config(config_path: str = "config/config.yaml") -> Dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f) 

    return config