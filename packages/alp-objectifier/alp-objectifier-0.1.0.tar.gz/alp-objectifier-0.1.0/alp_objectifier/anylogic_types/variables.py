from ..exceptions import assertTag
from ..util import extract_code
from lxml.objectify import ObjectifiedElement
from alp_objectifier.exceptions import assertClass
from alp_objectifier.util import extract_pyval

def variable_factory(obj: ObjectifiedElement):
    assertTag(obj.tag, "Variable")
    clazz = obj.get("Class")
    
    if clazz == "PlainVariable":
        return Variable(obj)
    elif clazz == "Parameter":
        return Parameter(obj)
    elif clazz == "CollectionVariable":
        return Collection(obj)
    elif clazz == "StockVariable":
        return Stock(obj)
    elif clazz == "Flow":
        return Flow(obj)
    elif clazz == "AuxVariable":
        return DynamicVariable(obj)
    else:
        raise TypeError(f"Unknown variable class: {clazz}")

class GenericVar:
    def __init__(self, obj: ObjectifiedElement, expected_class: str):
        assertTag(obj.tag, "Variable")
        assertClass(obj, expected_class)

        self._obj = obj
        self.name = obj.Name.pyval
        self._id = obj.Id.pyval
        self.description = extract_pyval(obj, "Description", "")
        unit_obj = obj.find("Unit")
        if unit_obj is not None:
            self.sd_unit = unit_obj.pyval

class Variable(GenericVar):
    def __init__(self, obj: ObjectifiedElement):
        super().__init__(obj, "PlainVariable")
        
        props = obj.Properties
        self.type = props.Type.pyval
        init_val = props.find("InitialValue")
        self.initial_value = None if init_val is None else extract_code(init_val)
        self.access = props.get("AccessType")
        self._is_static = props.get("StaticVariable") == "true"
        self._is_constant = props.get("Constant") == "true"

    def __str__(self):
        return f"Variable[{self.name}: {self.type}]"

    def __repr__(self):
        return str(self)

    def is_static(self):
        return self._is_static

    def is_constant(self):
        return self._is_constant

    def is_access_default(self):
        return self.access == "default"

    def is_access_public(self):
        return self.access == "public"

    def is_access_private(self):
        return self.access == "private"

    def is_access_protected(self):
        return self.access == "private"

class Collection(GenericVar):
    def __init__(self, obj: ObjectifiedElement):
        super().__init__(obj, "CollectionVariable")
        
        props = obj.Properties
        self.type = props.CollectionClass.pyval
        self.element_type = props.ElementClass.pyval
        if self.is_map():
            self.value_element_type = props.ValueElementClass.pyval
        self.access = props.get("AccessType")
        self._is_static = props.get("StaticVariable") == "true"
        init_val = props.find("CollectionInitializer")
        self.initial_value = None if init_val is None else extract_code(init_val)

    def __str__(self):
        return f"Collection[{self.name}: {self.type}]"

    def __repr__(self):
        return str(self)

    def is_map(self):
        return "Map" in self.type or "Hashtable" in self.type

    def has_value_element_type(self):
        return self.is_map()

    def is_static(self):
        return self._is_static

class Parameter(GenericVar):
    def __init__(self, obj: ObjectifiedElement):
        super().__init__(obj, "Parameter")

        props = obj.Properties
        self.parameter_type = props.get("ModificatorType") # static, dynamic, or action
        self.type = None if self.is_action() else props.Type.pyval
        self.default_value = self._get_default_value()
        unit = props.UnitType.pyval
        if unit != "NONE":
            self.unit = props.UnitType.pyval
        if not self.is_static():
            self.arguments = self._get_method_arguments()
        self.editor_type = props.ParameterEditor.EditorContolType.pyval

    def __str__(self):
        return f"Parameter[{self.name}: {self.type} = {self.default_value}]"

    def __repr__(self):
        return str(self)

    def _get_default_value(self):
        val = extract_code(self._obj.Properties.find("DefaultValue"))
        if val is None: # user left blank; set defaults for primitive types
            if self.type == 'boolean':
                val = False
            elif self.type in ['byte', 'short', 'int', 'long', 'float', 'double']:
                val = 0
        return val
    
    def _get_method_arguments(self):
        ''' Returns a list of arguments in the form: (name, type) '''
        args = []
        for arg in self._obj.Properties.findall("MethodArgument"):
            args.append( (arg.Name.pyval, arg.Type.pyval) )
        return args

    def is_static(self):
        return self.parameter_type == "STATIC"

    def is_dynamic(self):
        return self.parameter_type == "DYNAMIC"

    def is_action(self):
        return self.parameter_type == "ACTION"

class Stock(GenericVar):
    def __init__(self, obj: ObjectifiedElement):
        super().__init__(obj, "StockVariable")
        
        props = obj.Properties
        self.is_array = props.get("Array") == "false"
        self.equation_style = props.EquationStyle.pyval
        initval_obj = props.find("InitialValue")
        if initval_obj is not None:
            self.initial_value = initval_obj.pyval
        expr_obj = props.find("Expression")
        if expr_obj is not None:
            self.expression = expr_obj.pyval
        self.has_shadow = props.find("Shadow") is not None

    def __str__(self):
        return f"Stock[{self.name}: {self.initial_value}]"

    def __repr__(self):
        return str(self)


class Flow(GenericVar):
    def __init__(self, obj: ObjectifiedElement):
        super().__init__(obj, "Flow")

        props = obj.Properties
        self.has_shadow = props.find("Shadow") is not None
        self.is_dependent = props.get("External") == "true"
        self.is_constant = props.get("Constant") == "true"
        self.is_array = props.get("Array") == "true"

        if self.is_constant:
            self.value = props.Value.pyval
        elif self.is_array:
            self.formula = [form.pyval for form in props.findall("Expression")]
        else:
            self.formula = extract_pyval(props, "Formula")


    def __str__(self):
        output = None
        try:
            output = str(self.formula)
        except:
            try:
                output = str(self.value)
            except:
                pass
        return f"Flow[{self.name}: {output}]"
    
    def __repr__(self):
        return str(self)


class DynamicVariable(GenericVar):
    def __init__(self, obj: ObjectifiedElement):
        super().__init__(obj, "AuxVariable")

        props = obj.Properties
        self.is_dependent = props.get("External") == "true"
        self.is_constant = props.get("Constant") == "true"
        self.is_array = props.get("Array") == "true"

        if self.is_constant:
            self.value = extract_pyval(props, "Value")
        elif self.is_array:
            self.formula = [form.pyval for form in props.findall("Expression")]
        else:
            self.formula = extract_pyval(props, "Formula")

        self.has_shadow = props.find("Shadow") is not None

    def __str__(self):
        if self.is_constant:
            val = self.value
        else:
            val = self.formula
        return f"DynamicVariable[{self.name}: {val}]"
    
    def __repr__(self):
        return str(self)

    def has_formula(self):
        return not self.is_constant
    
    def has_value(self):
        return self.is_constant



