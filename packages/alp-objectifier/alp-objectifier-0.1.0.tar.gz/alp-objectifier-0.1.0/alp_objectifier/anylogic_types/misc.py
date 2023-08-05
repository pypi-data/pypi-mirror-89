from lxml.objectify import ObjectifiedElement
from alp_objectifier.exceptions import assertTag

class Port:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj, "Port")
        self._obj = obj
        self.name = obj.Name.pyval
        self.incoming_type = obj.IncomingMessageType.pyval
        self.outgoing_type = obj.OutgoingMessageType.pyval
        self.is_custom_port = obj.CustomPort.pyval
        if self.is_custom_port:
            self.constructor_code = obj.ConstructorCode.pyval
