from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement
from alp_objectifier.util import extract_pyval

class Dimension:
    def __init__(self, model, obj: ObjectifiedElement):
        assertTag(obj.tag, "Dimension")
        self._model = model
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.type = obj.Type.pyval
        self.super_dimension = self._get_superdim()
        self.range = obj.Range.pyval if obj.Range else None
        self.elements = [Element(o) for o in obj.iter("Element")]

        self._delete_irrelevant_fields()

    def __str__(self):
        return f"Dimension[{self.name}: {self.type}]"

    def __repr__(self):
        return str(self)

    def _get_superdim(self):
        superdim_obj = self._obj.find("SuperDimension")
        if superdim_obj is None:
            return None
        return f"{superdim_obj.PackageName.pyval}.{superdim_obj.ClassName.pyval}"

    def _delete_irrelevant_fields(self):
        if self.super_dimension is None:
            del self.super_dimension
        
        if self.type == "range":
            del self.elements
        else:
            del self.range
    
    def is_range(self):
        return self.type == "range"
    
    def is_enumeration(self):
        return not self.is_range()
    
    def has_super_dimension(self):
        result = False
        try:
            result = self.super_dimension is not None
        except:
            pass
        return result
        

class Element:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Element")
        self._obj = obj
        if obj.find("Name") is not None: # stand-alone dimension
            self.super_class = None
            self.name = obj.Name.pyval
            self.value = obj.Value.pyval
        else: # is a sub-dimension
            self.super_class = f"{obj.PackageName.pyval}.{obj.ClassName.pyval}"
            self.name = obj.ItemName.pyval
            self.value = None # TODO - find way to inherit value
    
    def __str__(self):
        return f"Element[{self.name}: {self.value}]"

    def __repr__(self):
        return str(self)
