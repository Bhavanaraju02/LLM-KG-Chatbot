import re

def extract_entity(uri):
    return re.split(r'[/#]', uri)[-1].replace("_", " ")
