from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement

class Library:
    def __init__(self, model, obj: ObjectifiedElement):
        assertTag(obj.tag, "Library")
        self._model = model
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = "" if not obj.find("Description") else obj.Description.pyval
        ## TODO - entries are just IDs - would need a way to search for objs
        self.version = (obj.VersionMajor.pyval, obj.VersionMinor.pyval, obj.VersionBuild.pyval)
        self.provider = obj.Provider.pyval

    def __str__(self):
        return f"Library[{self.name}]"

    def __repr__(self):
        return str(self)

class Resource:
    def __init__(self, model, obj: ObjectifiedElement):
        assertTag(obj.tag, "Resource")
        self._model = model
        self._obj = obj
        self.path = obj.Path.pyval
        self.referenced = obj.ReferencedFromUserCode.pyval

    def __str__(self):
        return f"Resource[{self.path}]"

    def __repr__(self):
        return str(self)

class RequiredLibrary:
    def __init__(self, model, obj: ObjectifiedElement):
        assertTag(obj.tag, "RequiredLibraryReference")
        self._model = model
        self._obj = obj
        self.library_name = obj.LibraryName.pyval
        self.version = (obj.VersionMajor.pyval, obj.VersionMinor.pyval, obj.VersionBuild.pyval)

    def __str__(self):
        return f"RequiredLibrary[{self.library_name}]"

    def __repr__(self):
        return str(self)

