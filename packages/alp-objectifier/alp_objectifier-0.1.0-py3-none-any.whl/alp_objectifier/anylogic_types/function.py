from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement
from alp_objectifier.util import extract_pyval

class Function:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Function")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        unit_obj = obj.find("Unit")
        if unit_obj is not None:
            self.sd_unit = unit_obj.pyval
        self.return_type = extract_pyval(obj, "ReturnModificator", None)
        self.access = obj.get("AccessType")
        self.is_static = obj.get("StaticFunction") == "true"
        self.arguments = self._get_arguments()
        self.body = extract_pyval(obj, "Body", "")

    def __str__(self):
        arg_strs = ", ".join([f"{a[1]} {a[0]}" for a in self.arguments])
        return f"Function[{self.name}({arg_strs}) -> {self.return_type}]"

    def __repr__(self):
        return str(self)

    def _get_arguments(self):
        ''' Returns a list of (name, type) arguments in the function '''
        args = []
        try:
            for arg in self._obj.Parameter:
                args.append((arg.Name.pyval, arg.Type.pyval))
        except: # no 'Parameter' tags
            pass
        return args

    def is_access_default(self):
        return self.access == "default"

    def is_access_public(self):
        return self.access == "public"

    def is_access_private(self):
        return self.access == "private"

    def is_access_protected(self):
        return self.access == "private"