from typing import Union
from lxml.objectify import ObjectifiedElement

def assertTag(obj_tag: Union[str, ObjectifiedElement], expected_tag: str):
    if not isinstance(obj_tag, str):
        obj_tag = obj_tag.tag
    if obj_tag != expected_tag:
        raise WrongTagError(obj_tag, expected_tag)

def assertClass(obj_class: Union[str, ObjectifiedElement], expected_class: str):
    if not isinstance(obj_class, str):
        obj_class = obj_class.get("Class")
    if obj_class is None or obj_class != expected_class:
        raise WrongTagError(obj_class, expected_class)

class WrongTagError(ValueError):
    """Error raised when the wrong tag was used in a constructor """
    def __init__(self, given_tag, expected_tag):
        message = "Expecting an object with the '{}' tag, but was given the '{}' tag"
        super().__init__(message.format(expected_tag, given_tag))

class WrongClassError(ValueError):
    """Error raised when the wrong class is present in the object (or none at all) """
    def __init__(self, given_class, expected_class):
        message = "Provided object has the wrong class - is a '{}', not a '{}'"
        super().__init__(message.format(given_class, expected_class))