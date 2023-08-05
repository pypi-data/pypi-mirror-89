from ..exceptions import assertTag
from .agent_class import AgentClass
from .optionlist import OptionList
from .dimensions import Dimension
from .java_class import JavaClass
from .resources import Library, Resource, RequiredLibrary
from .experiments import experiment_factory, Experiment
from lxml.objectify import ObjectifiedElement
from typing import List, Dict, Any
from warnings import warn
from alp_objectifier.util import extract_pyval

class Model:
    def __init__(self, obj: ObjectifiedElement, remove_nonexists: bool = False):
        assertTag(obj.tag, "Model")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.package = obj.JavaPackageName.pyval
        self.time_unit = obj.ModelTimeUnit.pyval

        # print(f"Creating model {self.package}.{self.name}")

        self.option_lists = self._get_option_lists()
        self.dimensions = self._get_dimensions()
        self.agents = self._get_agents()
        self.database_info = self._get_database_info()
        self.experiments = self._get_experiments()
        self.java_classes = self._get_java_classes()
        self.libraries = self._get_libraries()
        self.resources = self._get_resources()
        self.required_libs = self._get_required_libs()

        if remove_nonexists:
            self.remove_empties()

    def __str__(self):
        return f"Model[{self.name}]"

    def __repr__(self):
        return str(self)

    def _get_option_lists(self) -> List[OptionList]:
        olists = self._obj.find("OptionLists")
        if olists is None:
            return []
        return [OptionList(self, o) for o in olists.OptionList]

    def _get_dimensions(self) -> List[Dimension]:
        dims = self._obj.find("Dimensions")
        if dims is None:
            return []
        return [Dimension(self, d) for d in dims.Dimension]
    
    def _get_agents(self) -> List[AgentClass]:
        objclasses = self._obj.find("ActiveObjectClasses")
        if objclasses is None:
            return []
        return [AgentClass(self, a) for a in objclasses.ActiveObjectClass]
    
    def _get_database_info(self) -> Dict[str, Any]:
        info = dict()
        db = self._obj.find("Database")
        if db is None:
            return info
        db["is_logging"] = db.Logging.pyval

        # fill out import settings
        import_settings = dict()
        isettings = db.ImportSettings
        if isettings is not None:
            ext_conn = isettings.find("ExternalConnection")
            if ext_conn is not None:
                db_type = ext_conn.DatabaseType.pyval
                import_settings["database_type"] = db_type
                if db_type == "EXCEL_ACCESS":
                    ifile = None
                    try:
                        ifile = ext_conn.ResourceReference.ClassName.pyval
                    except AttributeError as e: # older way of referencing
                        try:
                            ifile = ext_conn.DbFileName.pyval
                        except AttributeError as e: # apparently no excel file name reference? 
                            pass
                        
                    if ifile is None:
                        warn("May have a corrupted database: input denoted as excel file but cannot find a referenced file. Setting value as None.")
                    import_settings["input_file"] = ifile
        db["import_settings"] = import_settings

        # fill out export settings
        export_settings = dict()
        esettings = db.ExportSettings
        # export tag may exist but nothing inside
        if esettings is not None:
            eresource = esettings.find("ExportExcelResourceReference")
            if eresource is not None: 
                export_settings["output_file"] = eresource.ClassName.pyval
            # user may have 0 or more table references
            tables_exporting = []
            try:
                for tab_ref in esettings.TableReference:
                    tables_exporting.append(tab_ref.ClassName.pyval)
            except:
                pass
            export_settings["tables_exporting"] = tables_exporting
        db["export_settings"] = export_settings

        return info
    
    def _get_experiments(self) -> List[Experiment]:
        exps = self._obj.find("Experiments")
        if exps is None:
            return []
        return [experiment_factory(self, exp) for exp in exps.getchildren() if exp.tag != "comment"]

    def _get_java_classes(self) -> List[JavaClass]:
        jclasses = self._obj.find("JavaClasses")
        if jclasses is None:
            return []
        return [JavaClass(self, j) for j in jclasses.JavaClass]

    def _get_libraries(self) -> List[Library]:
        libs = self._obj.find("Libraries")
        if libs is None:
            return []
        return [Library(self, lib) for lib in libs.Library]

    def _get_resources(self) -> List[Resource]:
        res = self._obj.find("ModelResources")
        if res is None:
            return []
        return [Resource(self, r) for r in res.Resource]

    def _get_required_libs(self) -> List[RequiredLibrary]:
        reqlibs = []
        try:
            for rlib in self._obj.RequiredLibraryReference:
                reqlibs.append(RequiredLibrary(self, rlib))
        except: # no required library references
            pass
        return reqlibs

    def remove_empties(self):
        for name,val in vars(self).items():
            if not val:
                _ = vars(self).pop(name)
