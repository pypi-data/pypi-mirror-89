from ..exceptions import assertTag
from .dimensions import Dimension
from .variables import variable_factory, Variable, Collection, Parameter, Stock, Flow, DynamicVariable
from .analyses import Output, DataSet, Statistics, HistogramData, Histogram2DData
from .events import Event, DynamicEvent
from .agent_objects import Object
from .function import Function
from .schedule import Schedule
from .misc import Port
from lxml.objectify import ObjectifiedElement
from warnings import warn
from alp_objectifier.util import extract_pyval

class AgentClass:
    def __init__(self, model, obj: ObjectifiedElement):
        assertTag(obj.tag, "ActiveObjectClass")
        self._model = model
        self._obj = obj
        self.name = obj.Name.pyval
        self._id = obj.Id.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.imports = [] if obj.find("Import") is None else [i for i in obj.Import.pyval.split("\n") if i]
        self.code_fields = self._get_code_dict()
        self.space_info = self._get_space_info()
        self.physical_info = self._get_physical_info()
        self.flowcharts_usage = extract_pyval(obj, "FlowchartsUsage", "ENTITY")
        self.agents = self._get_embedded_objects()
        self.collections, self.parameters, self.variables, self.stocks, self.flows, self.dynamic_variables = self._get_all_variable_types()
        self.ports = self._get_ports()
        self.analyses = self._get_all_analysis_types()
        self.events, self.dynamic_events = self._get_all_event_types()
        self.functions = self._get_functions()
        self.schedules = self._get_schedules()

    def __str__(self):
        return f"AgentClass[{self.name}: {self.flowcharts_usage}]"

    def __repr__(self):
        return str(self)

    def _get_code_dict(self):
        ''' Returns a map of code field names to the contents
        The keys used are the field names, lowercased, with underscores instead of spaces.
        Exception: Agent versus environment step fields have special names. '''
        codes = dict()

        obj = self._obj

        # agent code related fields
        addtl = obj.find("AdditionalClassCode")
        if addtl is not None:
            codes["additional_class_code"] = addtl.pyval
        start = obj.find("StartupCode")
        if start is not None:
            codes["on_startup"] = start.pyval
        destroy = obj.find("DestroyCode")
        if destroy is not None:
            codes["on_destroy"] = destroy.pyval

        # agent event related fields
        agentProps = obj.AgentProperties
        arrival = agentProps.find("OnArrival")
        if arrival is not None: 
            codes["on_arrival"] = arrival.pyval
        enter_block = agentProps.find("OnEnterFlowchartBlock")
        if enter_block is not None:
            codes["on_enter_flowchart_block"] = enter_block.pyval
        exit_block = agentProps.find("OnExitFlowchartBlock")
        if exit_block is not None:
            codes["on_exit_flowchart_block"] = exit_block.pyval
        seize_res = agentProps.find("OnSeizeResource")
        if seize_res is not None:
            codes["on_seize_resource"] = seize_res.pyval
        release_res = agentProps.find("OnReleaseResource")
        if release_res is not None:
            codes["on_release_resource"] = release_res.pyval
        agent_before_step = agentProps.find("BeforeStepCode")
        if agent_before_step is not None:
            codes["on_agent_before_step"] = agent_before_step.pyval
        agent_after_step = agentProps.find("AfterStepCode")
        if agent_after_step is not None:
            codes["on_agent_after_step"] = agent_after_step.pyval

        # step related fields in the environment
        envProps = obj.find("EnvironmentProperties")
        if envProps is not None:
            env_before_step = envProps.find("BeforeStepCode")
            if env_before_step is not None: 
                codes["on_environment_before_step"] = env_before_step.pyval
            env_after_step = envProps.find("AfterStepCode")
            if env_after_step is not None: 
                codes["on_environment_after_step"] = env_after_step.pyval
        
        return codes

    def _get_space_info(self):
        ''' Gets a dict with information about the space type used (Continuous vs Discrete vs GIS) '''
        info = dict()

        envProps = self._obj.find("EnvironmentProperties")
        if envProps is None:
            return info

        space_type = envProps.SpaceType.pyval
        info["type"] = space_type

        # GIS has no other settings; can just stop here
        if space_type == "GIS": ## TODO - maybe add info about the GIS map here since can only have max 1?
            return info
        
        # Continuous and Discrete have much in common
        info["width"] = envProps.WidthCode.pyval
        info["height"] = envProps.HeightCode.pyval
        info["layout_type"] = envProps.LayoutType.pyval
        # only add network settings depending on type (even though all are always provided)
        ntype = envProps.NetworkType.pyval
        info["network_type"] = ntype
        ntype_lower = ntype.lower() # make it easier to search
        if "random" in ntype_lower or "ring" in ntype_lower or "small" in ntype_lower:
            info["connections_per_agent"] = envProps.ConnectionsPerAgentCode.pyval
        if "distance" in ntype_lower:
            info["connections_range"] = envProps.ConnectionsRangeCode.pyval
        if "small" in ntype_lower:
            info["neighbor_link_fraction"] = envProps.NeighborLinkFractionCode.pyval
        if "scale" in ntype_lower:
            info["M"] = envProps.MCode.pyval

        # Continuous-specific
        if space_type == "CONTINUOUS":
            info["z_height"] = envProps.ZHeightCode.pyval
        # Discrete-specific
        elif space_type == "DISCRETE":
            info["columns"] = envProps.ColumnsCountCode.pyval
            info["rows"] = envProps.RowsCountCode.pyval
        return info


    def _get_physical_info(self):
        ''' Returns a dict of axis name to tuple of value and unit '''
        agentProps = self._obj.AgentProperties
        try:
            aLen = agentProps.PhysicalLength
            aWid = agentProps.PhysicalWidth
            aHyt = agentProps.PhysicalHeight
            return {
                "length": (aLen.Code.pyval, aLen.Unit.pyval),
                "width": (aWid.Code.pyval, aWid.Unit.pyval),
                "height": (aHyt.Code.pyval, aHyt.Unit.pyval)
            }
        except AttributeError as e:
            warn(repr(e))
            return None

    def _get_embedded_objects(self):
        embedobjs = []
        embedobjs_obj = self._obj.find("EmbeddedObjects")
        if embedobjs_obj is None:
            return embedobjs
        for embedobj_obj in embedobjs_obj.findall("EmbeddedObject"):
            embedobjs.append(Object(embedobj_obj))
        return embedobjs
        
    def _get_all_variable_types(self):
        ''' Returns sub-classes of variables '''
        variables = self._obj.find("Variables")
        if variables is None:
            return [], [], [], [], [], []
        collects, params, plainvars, stocks, flows, dynvars = [], [], [], [], [], []
        for variable in variables.Variable:
            varobj = variable_factory(variable)
            if isinstance(varobj, Collection):
                collects.append(varobj)
            elif isinstance(varobj, Parameter):
                params.append(varobj)
            elif isinstance(varobj, Variable):
                plainvars.append(varobj)
            elif isinstance(varobj, Stock):
                stocks.append(varobj)
            elif isinstance(varobj, Flow):
                flows.append(varobj)
            elif isinstance(varobj, DynamicVariable):
                dynvars.append(varobj)
            else:
                raise TypeError(f"Unknown class for: {varobj}")
        return collects, params, plainvars, stocks, flows, dynvars

    def _get_ports(self):
        ports = []
        ports_obj = self._obj.find("Ports")
        if ports_obj is None:
            return ports
        for port_obj in ports_obj.findall("Port"):
            ports.append(Port(port_obj))
        return ports

    def _get_all_analysis_types(self):
        ''' Gets a dict of named to list for all outputs, statistics, datasets, and Histogram (1d + 2d) '''
        outputsObj = self._obj.find("Outputs")
        outputs = []
        if outputsObj is not None:
            for o in outputsObj.Output:
                outputs.append(Output(o))
        
        analysisObj = self._obj.find("AnalysisData")
        stats, datasets, histos1D, histos2D = [], [], [], []
        if analysisObj is not None:
            for obj in analysisObj.getchildren():
                if obj.tag == "Statistics":
                    stats.append(Statistics(obj))
                elif obj.tag == "DataSet":
                    datasets.append(DataSet(obj))
                elif obj.tag == "HistogramData":
                    histos1D.append(HistogramData(obj))
                elif obj.tag == "Histogram2DData":
                    histos2D.append(Histogram2DData(obj))
                else:
                    raise ValueError(f"Unknown tag for analysis obj: {obj.tag}")
        
        analyses = dict(zip(
            ["Outputs", "Statistics", "DataSets", "HistogramDatas", "Histogram2DDatas"], 
            [outputs, stats, datasets, histos1D, histos2D]
            ))


    def _get_all_event_types(self):
        ''' Gets a list of all Event and Dynamic Event objects added to the agent '''
        events = self._obj.find("Events")
        eventlist = []
        if events is not None:
            for e in events.Event:
                eventlist.append(Event(e))
        
        dynevents = self._obj.find("DynamicEvents")
        dyneventlist = []
        if dynevents is not None:
            for d in dynevents.DynamicEventClass:
                dyneventlist.append(DynamicEvent(d))

        return eventlist, dyneventlist
    
    def _get_functions(self):
        ''' Gets a list of all function objects added to the agent '''
        functions = self._obj.find("Functions")
        if functions is None:
            return []
        return [Function(f) for f in functions.Function]
    
    def _get_schedules(self):
        ''' Gets a list of all schedule objects added to the agent '''
        schedules = self._obj.find("Schedules")
        if schedules is None:
            return []
        return [Schedule(s) for s in schedules.Schedule]

    def get_parameter(self, identifier, error_on_missing=True):
        ''' Attempts to get the parameter object with the specified identifier (String name or int ID).
        May provide a warning or error (if argument is a boolean value) if one cannot be found.
        This can either be due to a user-error (e.g., spelling) or leftover XML in the ALP file. 
        '''
        if isinstance(identifier, str):
            param = next(filter(lambda p: p.name == identifier, self.parameters ), None)
        else:
            param = next(filter(lambda p: p._id == identifier, self.parameters), None)
        if param is None: # either throw error or warn (or nothing if None)
            # add ID prefix if passed identifier is an int
            pids = [("" if isinstance(identifier, str) else f"[{p._id}]") + p.name for p in self.parameters]
            message = f"Parameter '{identifier}' not found in list of known parameters: {pids}"
            if error_on_missing:
                raise ValueError(message)
            elif error_on_missing == False:
                warn(message)
        return param