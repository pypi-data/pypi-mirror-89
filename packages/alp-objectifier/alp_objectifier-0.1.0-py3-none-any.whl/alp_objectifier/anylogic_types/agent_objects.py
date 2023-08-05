from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement
from alp_objectifier.util import extract_pyval, extract_code
from warnings import warn


## TODO find way of detecting object type (agent/block/etc)
class ObjectClass:
    ''' The package + class names for an embedded object (block/agent/populations) '''
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "ActiveObjectClass")
        self._obj = obj
        self.package_name = obj.PackageName.pyval
        self.class_name = obj.ClassName.pyval
    
    def __str__(self):
        return f"{self.package_name}.{self.class_name}"

    def __repr__(self):
        return str(self)

class ObjectParameterField: ## TODO - should remove any parameters with None value?
    ''' A field for a parameter's value within the properties of an embedded object (block/agent/populations) '''
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Parameter")
        self._obj = obj
        self.name = extract_pyval(obj, "Name")
        self.value, self._value_type, self.unit, self._unit_type = \
            self._get_value_data()
    
    def _get_value_data(self):
        if self._obj.find("Value") is None:
            return None, None, None, None
        val_obj = self._obj.Value
        vtype = val_obj.get("Class")

        value = None # can come in a few different forms
        vcode_obj = val_obj.find("Code") # direct value
        if vcode_obj is not None:
            value = vcode_obj.pyval
        else:
            ebed_obj = val_obj.find("EntityEmbeddedObject") # new object value
            if ebed_obj is not None:
                actobj_obj = ebed_obj.find("ActiveObjectClass")
                if actobj_obj is None:
                    warn("EntityEmbeddedObject has no ActiveObjectClass")
                else:
                    value = ObjectClass(actobj_obj)

        vunit_obj = val_obj.find("Unit")
        vunit = None if vunit_obj is None else vunit_obj.pyval
        vunit_type = None if vunit_obj is None else vunit_obj.get("Class")
        return value, vtype, vunit_obj, vunit_type

    def __str__(self):
        val_str = str(self.value)
        if self.unit is not None:
            val_str += " " + str(self.unit)
        return f"ParameterField[{self.name}: {val_str}]"

    def __repr__(self):
        return str(self)

class Object:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "EmbeddedObject")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.obj_class = ObjectClass(obj.ActiveObjectClass)
        self.parameters = self._get_parameters()

    def __str__(self):
        pop_data = f"[{self.population_size()}]" if self.is_population() else ""
        return f"{self.obj_class} {self.name}{pop_data}"

    def __repr__(self):
        return str(self)

    def _get_parameters(self):
        # NOTE: All objects are ObjectParameterField types except the generic parameter substitute (str)
        params = dict()
        # some blocks - like Enter - have a 'GenericParameterSubstitute' tag that seems to apply to the inherited agent type
        # not sure exactly what this can otherwise be, so add it.
        psub_obj = self._obj.find("GenericParameterSubstitute")
        if psub_obj is not None:
            psubval_obj = psub_obj.find("GenericParameterSubstituteValue")
            if psubval_obj is not None:
                code = extract_code(psubval_obj)
                if code is not None:
                    params['substituteValue'] = code
        params_obj = self._obj.find("Parameters")
        if params_obj is None:
            return params
        for p in params_obj.findall("Parameter"):
            p_field = ObjectParameterField(p)
            params[p_field.name] = p_field
        return params

    def is_by_anylogic(self):
        return self.obj_class.package_name.startswith("com.anylogic")

    def is_population(self):
        return self._obj.ReplicationFlag.pyval

    def population_size(self):
        if not self.is_population():
            return 1
        return self._obj.Replication.Code.pyval

# class BlockObject(Object):
#     def __init__(self, obj: ObjectifiedElement):
#         super().__init__(obj)

# class AgentObject(Object):
#     def __init__(self, obj: ObjectifiedElement):
#         super().__init__(obj)
