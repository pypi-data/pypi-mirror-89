import sys
##sys.path.extend("anylogic_types")
from lxml import objectify
from .anylogic_types.model import Model

def convert(alp_file):
    with open(alp_file, "rb") as f:
        content = f.read()
    root = objectify.fromstring(content)
    return Model(root.Model)
