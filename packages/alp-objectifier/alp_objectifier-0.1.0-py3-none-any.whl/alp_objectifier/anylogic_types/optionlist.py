from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement
from alp_objectifier.util import extract_pyval

class OptionList:
    def __init__(self, model, obj: ObjectifiedElement):
        assertTag(obj.tag, "OptionList")
        self._model = model
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.options = []
        for opt in obj.Option:
            nameObj = opt.find("Name")
            if nameObj is not None:
                self.options.append(nameObj.pyval)

    def __str__(self):
        return f"OptionList[{self.name}: x{len(self.options)}]"

    def __repr__(self):
        return str(self)