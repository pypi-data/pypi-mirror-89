from .variables import variable_factory, Variable, Collection, Parameter
from .analyses import Output, DataSet, Statistics, HistogramData, Histogram2DData
from .function import Function
from ..util import to_datetime
from lxml.objectify import ObjectifiedElement
from datetime import datetime
from warnings import warn
from alp_objectifier.util import extract_code, extract_pyval

def experiment_factory(model, obj: ObjectifiedElement):
    # Don't assert tag since each experiment has their own tag
    if "experiment" not in obj.tag.lower():
        raise ValueError(f"Tag does not indicate an experiment ({obj.tag}); assumed to be wrong object type")
    tag_abbv = obj.tag[:5].lower()
    if   tag_abbv == "simul":
        return SimExperiment(model, obj)
    elif tag_abbv == "compa":
        return CompareRunsExperiment(model, obj)
    elif tag_abbv == "param":
        return VariationExperiment(model, obj)
    elif tag_abbv == "optim":
        return OptimizationExperiment(model, obj)
    elif tag_abbv == "custo":
        return CustomExperiment(model, obj)
    elif tag_abbv == "reinf":
        return ReinforcementLearningExperiment(model, obj)
    else: # default to generic
        warn(f"Unidentified experiment: {obj.tag}")
        return Experiment(model, obj)
    

class Experiment:
    def __init__(self, model, obj: ObjectifiedElement):
        self._model = model
        self._obj = obj
        self.type = obj.tag.replace("Experiment", "")
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.toplevel_agent = self._get_toplevel_agent()
        if self.toplevel_agent is None and not self.is_experiment_custom():
            warn(f"Experiment '{self.name}' ({self.type}) could not find a top-level agent.")

        self.time_properties = self._get_time_info()
        self.rng_type, self.rng_value = self._get_rng_fields()
        self.args = self._get_args()

        self.imports = [] if obj.find("Import") is None else [i for i in obj.Import.pyval.split("\n") if i]
        self.code_fields = self._get_code_dict()

        self.collections, _, self.variables = self._get_all_variable_types()
        self.analyses = self._get_all_analysis_types()
        self.functions = self._get_functions()

    def __str__(self):
        tla = None if self.toplevel_agent is None else self.toplevel_agent.name # None if custom
        return f"{self.type}[{self.name}: {tla}]"

    def __repr__(self):
        return str(self)

    def _get_toplevel_agent(self):
        return next(filter(
            lambda a: str(a._id) == self._obj.get("ActiveObjectClassId"), self._model.agents
            ), None)

    def _get_time_info(self):
        info = dict()

        if self._obj.find("ModelTimeProperties") is None: # custom experiments
            return info

        props = self._obj.ModelTimeProperties
        opt = props.StopOption.pyval
        info["stop_mode"] = opt
        info["start_time"] = props.InitialTime.pyval
        info["start_date"] = to_datetime(props.InitialDate.pyval)
        if "time" in opt.lower():
            info["stop_time"] = props.FinalTime.pyval
            info["stop_date"] = None
        elif "date" in opt.lower():
            info["stop_time"] = None
            info["stop_date"] = to_datetime(props.FinalDate.pyval)
        else: # never
            info["stop_time"] = None
            info["stop_date"] = None
        
        if props.find("AdditionalStopCondition") is not None:
            addtl_conditions = []
            for cond_obj in props.AdditionalStopCondition:
                condition = {"enabled": cond_obj.Enabled.pyval, "expression": cond_obj.Expression.pyval}
                addtl_conditions.append(condition)
            info["additional_experiment_stop_conditions"] = addtl_conditions
        return info
        
    def _get_rng_fields(self):
        rng_obj = self._obj.find("RandomNumberGenerationType")
        if rng_obj is None: # custom experiments
            return None, None
        rng_type = rng_obj.pyval
        rng_value = None
        if "fixed" in rng_type:
            rng_value = self._obj.SeedValue.pyval
        elif "random" in rng_type:
            rng_value = None
        elif "custom" in rng_type:
            rng_value = self._obj.CustomGeneratorCode.pyval
        else:
            raise ValueError(f"Unhandled type: {rng_type}")
        return rng_type, rng_value

    def _get_args(self):
        cla = self._obj.find("CommandLineArguments")
        vma = self._obj.find("VmArgs")
        return {"commandline": None if cla is None else cla.pyval, 
                    "java": None if vma is None else vma.pyval}

    def _get_code_dict(self):
        ''' Returns a map of code field names to the contents
        The keys used are the field names, lowercased, with underscores instead of spaces.
        '''
        codes = dict()
        obj = self._obj

        addtl = obj.find("AdditionalClassCode")
        if addtl is not None:
            codes["additional_class_code"] = addtl.pyval
        
        initsetup = obj.find("InitialSetupCode")
        if initsetup is not None:
            codes["initial_experiment_setup"] = initsetup.pyval
        
        preexp = obj.find("BeforeEachExperimentRunCode")
        if preexp is not None:
            codes["before_each_experiment_run"] = preexp.pyval
        
        presim = obj.find("BeforeSimulationRunCode")
        if presim is not None:
            codes["before_simulation_run"] = presim.pyval

        postsim = obj.find("AfterSimulationRunCode")
        if postsim is not None:
            codes["after_each_experiment"] = postsim.pyval

        postiter = obj.find("AfterIterationCode")
        if postiter is not None:
            codes["after_iteration"] = postiter.pyval

        postexp = obj.find("AfterExperimentCode")
        if postexp is not None:
            codes["after_experiment"] = postexp.pyval
        
        return codes
  
    def _get_all_variable_types(self):
        ''' Returns the three sub-classes of variables: collections, parameters, and 'plain' variables '''
        variables = self._obj.find("Variables")
        if variables is None:
            return [], [], []
        collects, params, plainvars = [], [], []
        try:
            for variable in variables.Variable:
                varobj = variable_factory(variable)
                if isinstance(varobj, Collection):
                    collects.append(varobj)
                elif isinstance(varobj, Parameter):
                    params.append(varobj)
                elif isinstance(varobj, Variable):
                    plainvars.append(varobj)
                else:
                    raise TypeError(f"Unknown class for: {varobj}")
        except:
            print(f"Problem in experiment {self.name}")
        return collects, params, plainvars

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
        
        return dict(zip(
            ["Outputs", "Statistics", "DataSets", "HistogramDatas", "Histogram2DDatas"], 
            [outputs, stats, datasets, histos1D, histos2D]
            ))  

    def _get_functions(self):
        ''' Gets a list of all function objects added to the agent '''
        functions = self._obj.find("Functions")
        if functions is None:
            return []
        return [Function(f) for f in functions.Function]

    def get_parameter_value(self, parameter_obj, error_on_missing=None):
        value = None

        name_obj = parameter_obj.find("ParameterName")
        if name_obj is not None: # has a name
            name = parameter_obj.ParameterName.pyval
            value_obj = parameter_obj.find("ParameterValue") # if set to default, will be none
            
            if value_obj is None:
                # get default from TLA
                param = self.toplevel_agent.get_parameter(name, None)
                if param is not None:
                    value = param.default_value
            else:
                value = value_obj.Code.pyval
        else: # no "ParameterName" tag, try based on ID
            # currently only found this format in calibration experiment
            id_obj = parameter_obj.find("Id")
            if id_obj is not None: # has an id
                pid = id_obj.pyval
                # follows Value -> Code format
                value_obj = parameter_obj.find("Value")
                if value_obj is not None:
                    value = value_obj.Code.pyval
                else: # no value provided; assumed to be default
                    param = self.toplevel_agent.get_parameter(pid, None)
                    if param is not None:
                        value = param.default_value
        return value

    def uses_fixed_seed(self):
        return self.rng_type == "fixedSeed"

    def get_fixed_seed(self):
        if not self.uses_fixed_seed():
            return None
        return self.rng_value
    
    def uses_random_seed(self):
        return self.rng_type == "randomSeed"

    def is_experiment_simulation(self):
        return self.type == "Simulation"
    
    def is_experiment_optimization(self):
        return self.type == "Optimization"

    def is_experiment_paramvariation(self):
        return self.type == "ParamVariation"

    def is_experiment_compareruns(self):
        return self.type == "CompareRuns"

    def is_experiment_rl(self):
        return self.type == "ReinforcementLearning"

    def is_experiment_custom(self):
        return self.type == "Custom"


## experiment sub-classes add their own:
#   - parameters
#   - other unique attributes (e.g., constraints, fields, etc.)
class SimExperiment(Experiment):
    def __init__(self, model, obj: ObjectifiedElement):
        super().__init__(model, obj)

        self.parameters = self._get_parameters()

    def _get_parameters(self):
        parameters = []
        params_obj = self._obj.Parameters
        for param_obj in params_obj.findall("Parameter"):
            param = dict()
            param['name'] = param_obj.ParameterName.pyval
            param['value'] = super().get_parameter_value(param_obj)
            parameters.append( param )
        return parameters


class CompareRunsExperiment(Experiment):
    def __init__(self, model, obj: ObjectifiedElement):
        super().__init__(model, obj)

        self.parameters = self._get_parameters()

    def _get_parameters(self):
        parameters = []
        for param_obj in self._obj.Parameters.findall("Parameter"):
            param = dict()
            param['name'] = param_obj.ParameterName.pyval
            param['value'] = super().get_parameter_value(param_obj)
            parameters.append( param )
        return parameters
    

class VariationExperiment(Experiment):
    def __init__(self, model, obj: ObjectifiedElement):
        super().__init__(model, obj)

        self.parameters = self._get_parameters()
        self.replication_properties = self._get_replication_info()

    def _get_parameters(self):
        parameters = []

        if self._obj.UseFreeformParameters.pyval:

            for free_param_obj in self._obj.findall("FreeformParamValue"):
                param = dict()
                
                param["_parameter"] = next(filter(
                    lambda p: p._id == free_param_obj.Id.pyval, self.toplevel_agent.parameters
                    ), None)
                param["name"] = param["_parameter"].name
                expr_obj = free_param_obj.find("Expression")
                if expr_obj is not None:
                    expr = expr_obj.Code.pyval
                else:
                    expr = self.toplevel_agent.get_parameter(param['name'], False).default_value
                param["expression"] = expr
                parameters.append(param)
        else:
            for range_param_obj in self._obj.findall("RangeVariationParamValue"):
                param = dict()
                
                param["_parameter"] = next(filter(
                    lambda p: p._id == range_param_obj.Id.pyval, self.toplevel_agent.parameters
                    ), None) 
                param["name"] = param["_parameter"].name
                ptype = range_param_obj.Type.pyval
                param["type"] = ptype
                if ptype == "FIXED":
                    expr_obj = range_param_obj.find("Expression")
                    if expr_obj is not None:
                        expr = expr_obj.Code.pyval
                    else:
                        expr = self.toplevel_agent.get_parameter(param['name'], False).default_value
                    param["expression"] = expr
                else: # range
                    param["from"] = range_param_obj.From.Code.pyval
                    param["to"] = range_param_obj.To.Code.pyval
                    param["step"] = range_param_obj.Step.Code.pyval
                parameters.append(param)
        return parameters


    def _get_replication_info(self):
        info = dict()

        props = self._obj.ReplicationsProperties
        use = props.UseReplication.pyval
        info["use_replication"] = use
        if not use:
            return info
        
        fixed = props.FixedReplicationsNumber.pyval
        info["fixed_number_of_replications"] = fixed
        if fixed:
            info["replications_per_iteration"] = props.ReplicationPerIteration
        else:
            info["minimum_replications"] = props.MinimumReplication.pyval
            info["maximum_replications"] = props.MaximumReplication.pyval
            info["confidence_level"] = props.ConfidenceLevel.pyval
            info["error_percent"] = props.ErrorPercent.pyval
            info["confidence_expression"] = props.ExpressionForConfidenceComputation.pyval
        return info


class OptimizationExperiment(Experiment):
    def __init__(self, model, obj: ObjectifiedElement):
        super().__init__(model, obj)

        self.objective = obj.Objective.pyval
        self.objective_function = obj.ObjectiveFunctionCode.pyval

        self._append_time_properties() # for early stopping settings

        self.parameters = self._get_parameters()
        self.constraints = self._get_constraints()
        self.requirements = self._get_requirements()

    def _append_time_properties(self):
        ''' Appends early stopping settings to the time properties in the super-experiment's object '''
        props = self._obj.ModelTimeProperties
        if props.StopAfterIterationCount.pyval:
            limit = props.IterationCount.pyval
        else:
            limit = None
        self.time_properties["iteration_limit"] = limit
        self.time_properties["automatic_stop"] = props.AutomaticStop.pyval
        

    def _get_parameters(self):
        parameters = []
        if self._obj.find("Parameter") is None:
            return parameters

        for param_obj in self._obj.Parameter:
            param = dict()
            param["_parameter"] = next(filter(
                lambda p: p._id == param_obj.Id.pyval, self.toplevel_agent.parameters
                ), None)
            param["name"] = param["_parameter"].name
            ptype = param_obj.Type.pyval
            param["type"] = ptype
            if ptype == "FIXED" or ptype == "BOOLEAN":
                param['value'] = super().get_parameter_value(param_obj)
            elif ptype in ["INTEGER", "DISCRETE", "DESIGN", "CONTINUOUS"]:
                param["min"] = param_obj.Min.Code.pyval
                param["max"] = param_obj.Max.Code.pyval
                step_obj = param_obj.find("Step")
                param["step"] = None if step_obj is None else step_obj.Code.pyval
                suggested_obj = param_obj.find("Suggested")
                param["suggested"] = None if suggested_obj is None else suggested_obj.Code.pyval
            else:
                raise ValueError(f"Unknown optimization parameter type: {ptype}")
            parameters.append(param)
        return parameters

    def _get_constraints(self):
        constraints = []
        if self._obj.find("Constraint") is None:
            return constraints
        for con_obj in self._obj.Constraint:
            con = dict()
            con["enabled"] = con_obj.Enabled.pyval
            con["expression"] = con_obj.Expression.pyval
            con["type"] = con_obj.Type.pyval
            con["bound"] = con_obj.Bound.pyval
            constraints.append(con)
        return constraints

    def _get_requirements(self):
        requirements = []
        if self._obj.find("Requirement") is None:
            return requirements
        for req_obj in self._obj.Requirement:
            req = dict()
            req["enabled"] = req_obj.Enabled.pyval
            req["expression"] = req_obj.Expression.pyval
            req["type"] = req_obj.Type.pyval
            req["bound"] = req_obj.Bound.pyval
            requirements.append(req)
        return requirements

    
class ReinforcementLearningExperiment(Experiment):
    def __init__(self, model, obj: ObjectifiedElement):
        super().__init__(model, obj)

        self.stop_condition = obj.StopCondition.pyval
        
        self.observation_fields, self.observation_code = self._get_observations()

        self.action_fields, self.action_code = self._get_actions()
        actionObj = obj.find("ActionCode")
        self.action_code = "" if actionObj is None else actionObj.pyval

        self.config_fields, self.config_code = self._get_configs()

    def _get_observations(self):
        fields = []
        for field_obj in self._obj.findall("ObservationField"):
            field = {"name": field_obj.Name.pyval, "type": field_obj.Type.pyval}
            fields.append(field)
        code_obj = self._obj.find("ObservationCode")
        code = None if code_obj is None else code_obj.pyval
        return fields, code

    def _get_actions(self):
        fields = []
        for field_obj in self._obj.findall("ActionField"):
            field = {"name": field_obj.Name.pyval, "type": field_obj.Type.pyval}
            fields.append(field)
        code_obj = self._obj.find("ActionCode")
        code = None if code_obj is None else code_obj.pyval
        return fields, code

    def _get_configs(self):
        fields = []
        for field_obj in self._obj.findall("ConfigurationField"):
            field = {"name": field_obj.Name.pyval, "type": field_obj.Type.pyval}
            fields.append(field)
        code_obj = self._obj.find("ConfigurationCode")
        code = None if code_obj is None else code_obj.pyval
        return fields, code

class CustomExperiment(Experiment):
    def __init__(self, model, obj: ObjectifiedElement):
        super().__init__(model, obj)

        codeObj = obj.find("Code")
        self.code = "" if codeObj is None else obj.Code.pyval

