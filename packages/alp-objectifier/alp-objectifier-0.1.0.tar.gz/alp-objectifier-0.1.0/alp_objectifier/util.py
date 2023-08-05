import re
from lxml.objectify import ObjectifiedElement
from datetime import datetime, timedelta
from warnings import warn
from .constants import AgentRefLocationTypes

AS_AGENT, AS_VARIABLE, AS_PROPERTY, IN_CODE = AgentRefLocationTypes._order

def extract_pyval(root_obj: ObjectifiedElement, tag_name, default=None):
    ''' Tries to get the pyval of the given tag in the root element object, \
        otherwise returning the default. '''
    obj = root_obj.find(tag_name)
    return default if obj is None else obj.pyval

def extract_code(obj: ObjectifiedElement):
    ''' Tries to get the 'Code' tag from the provided object.
    If it cannot, it's assumed to be pulled from a database, 
        in which case, it extracts the data from the column. 
    'obj' is assumed to be an 'InitialValue' tag (or similar)'''
    if obj is None:
        #warn("Passed object (to get the value out of) was None")
        return None

    value = None
    try:
        value = obj.Code.pyval
    except: # assumed to be a database reference
        # 'ColumnReference' will either be directly in object or under 'Value' tag
        col = obj.find("ColumnReference")
        if col is None:
            col = obj.Value.ColumnReference
        value = f"{col.ClassName.pyval}.{col.ItemName.pyval}"
    return value

def add_class_var_if_tag_exists(_self, var_name, root_obj, tag_name): ## TODO distribute this around code
    ''' Only adds the given variable name to the class if the object has the tag. '''
    val = extract_pyval(root_obj, tag_name)
    if val is not None:
        _self.__dict__[var_name] = val

def to_datetime(value):
    ''' Converts the given time to a datetime object, 
    handling values > datetime.datetime(3001, 1, 19, 1, 59, 59) '''
    dt = None
    try:
        dt = datetime.fromtimestamp(value)
    except:
        # assumed milliseconds, divide by 1k and try again.
        try:
            value /= 1000.0
            dt = datetime.fromtimestamp(value)
        except:
            # assumed > year 3001. Find the difference since that year and add it
            dt_yr3001 = datetime(3001, 1, 1)
            epoch_yr3001 = dt_yr3001.timestamp()

            epoch_diff = value - epoch_yr3001
            dt = dt_yr3001 + timedelta(seconds=epoch_diff)


def get_possible_classes(model):
    ''' Gets the name of all Agent types and Java classes - both in just the type and package reference. '''
    possible_names = []
    for agent in model.agents:
        possible_names.append(agent.name)
    for clazz in model.java_classes:
        possible_names.append(clazz.name)
    return possible_names

def get_class_connections(model, in_code=False):
    ''' Finds all the uses of classes (Agents + Java) in the agents.
    Optionally checks for any class names in the agents' code fields (via regex patterns).
    Returns a mapping from agent types to a set of tuples containing: (location type, agent inside).
    Where "location type" can be one of the following:
        "agent" -> single or population of agents
        "variable" -> the set type of a Variable, Parameter, or Collection
        "property" -> the value of a property inside a block (e.g., agent type in Source block)
        "code" -> found within a code field
    Note: This is _NOT_ definitive or absolute. There may be other unhandled cases, such as extended agents.
    '''
    

    connections = dict()
    classes = get_possible_classes(model)
    for agent in model.agents:
        connections[agent.name] = set()
        # look thru all embedded agents (blocks, single agents, populations)
        for embed_agent in agent.agents:
            if embed_agent.obj_class.class_name in classes:
                # found an embedded agent (single or population) directly in agent, make connection
                connections[agent.name].add((AS_AGENT, embed_agent.obj_class.class_name))
            for name, p_value in embed_agent.parameters.items():
                if isinstance(p_value, str):
                    # Can be exact match (like in agent type dropdown for source)
                    if p_value in classes:
                        # found an agent type as a parameter value, make connection
                        connections[agent.name].add((AS_PROPERTY, p_value))
                    # Can also be a code field
                    elif in_code:
                        for c in classes:
                            # 3 ways to detect use in code (where 'C' is the class name)
                            # 1. Var type declaration: `C myvar = ...;`
                            # 2. Type casting: `(C)code`
                            # 3. New var constructor: `new C(`
                            if re.search(f"{c}\s+[\w_]+.+?=.+?;|\({c}\)\s*\w+|new {c}\(", p_value):
                                connections[agent.name].add((IN_CODE, c))
                elif p_value._value_type == "EntityCodeValue":
                    # found an agent type as a parameter value, make connection
                    if p_value.value is None:
                        warn(f"In {model.name}, agent {agent.name}, embed obj {embed_agent.name}, EntityCodeValue was None")
                    else:
                        connections[agent.name].add((AS_PROPERTY, p_value.value.class_name))
                elif p_value._value_type == "CodeValue":
                    # check for manually constructed agents inside of parameter value
                    # (e.g., Custom agent constructor in Source block: `new Car(...)`)
                    code = p_value.value
                    if not isinstance(code, str) or "new" not in code:
                        continue
                    for c in classes:
                        if f"new {c}(" in code:
                            # found, make connection
                            connections[agent.name].add((AS_PROPERTY, c))
        # look thru all variables
        for var in agent.variables:
            if var.type in classes:
                # type matches known class, make connection
                connections[agent.name].add((AS_VARIABLE, var.type))
        # look thru all collections
        for collect in agent.collections:
            if collect.element_type in classes:
                # element matches, make connection
                connections[agent.name].add((AS_VARIABLE, collect.element_type))
            if collect.is_map() and collect.value_element_type in classes:
                # value matches (collection is a map), make connection
                connections[agent.name].add((AS_VARIABLE, collect.value_element_type))
        # look thru all parameters
        for param in agent.parameters:
            if param.type in classes:
                # parameter has known type, make connnection
                connections[agent.name].add((AS_VARIABLE, param.type))
        # optionally look thru callbacks of agent
        if in_code:
            for _, code in agent.code_fields.items():
                for c in classes:
                    # 3 ways to detect use in code (where 'C' is the class name)
                    # 1. Var type declaration: `C myvar = ...;`
                    # 2. Type casting: `(C)code`
                    # 3. New var constructor: `new C(`
                    if re.search(f"{c}\s+[\w_]+.+?=.+?;|\({c}\)\s*\w+|new {c}\(", code):
                        connections[agent.name].add((IN_CODE, c))
    return connections

def class_connections_to_edge_list(connections, loctype_as_int=False):
    ''' Converts the dictionary of outputs from `get_class_connections` to a list of directed edges.
    Each edge points to the agent that the source node resides inside, along with the location type.
        E.g., The edge: [Person, Main, "agent"] indicates a single or population of Person agents inside of Main.
    Passing True to the extra argument converts the location type to an integer (for possibly easier post-processing)
    '''
    edges = []
    for parent_agent,vals in connections.items():
        for loc_type, child_agent in vals:
            loc = AgentRefLocationTypes.to_index(loc_type) if loctype_as_int else loc_type
            edges.append([child_agent, parent_agent, loc])
    return edges


