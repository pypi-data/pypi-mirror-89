from lxml.objectify import ObjectifiedElement
from alp_objectifier.util import extract_pyval

class JavaClass:
    def __init__(self, model, obj: ObjectifiedElement):
        self._model = model
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.text = obj.Text.pyval

    def __str__(self):
        return f"JavaClass[{self.name}]"

    def __repr__(self):
        return str(self)