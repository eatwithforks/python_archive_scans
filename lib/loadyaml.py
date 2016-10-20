import os
import yaml


PORTAL_CONFIG = os.path.join(os.path.dirname(__file__), '../configs/portal.yml')

def load_portal():
    """This method load the portal.yml"""
    return yaml.load(file(PORTAL_CONFIG, 'r'))
