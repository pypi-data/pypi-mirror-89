from ..exceptions import assertTag
from ..util import extract_code
from lxml.objectify import ObjectifiedElement
from datetime import datetime
from alp_objectifier.util import extract_pyval


class Output:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Output")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        self.type, self.unit = obj.Type.pyval, None
        if not self.type: # has units
            self.type = obj.UnitType.pyval
            self.unit = obj.UnitOfValue.pyval
        valObj = obj.find("Value")
        self.value = None if valObj is None else extract_code(obj.Value)

        # possible moments: # ON_SIMULATION_END, AT_MODEL_TIME, MANUALLY, AT_CALENDAR_DATE
        self.computation_moment = obj.ComputationMoment.pyval 
        self.computation_time = None
        self.computation_unit = None
        self.computation_date = None

        self._fill_fields()
        self._delete_irrelevant_fields()

    def __str__(self):
        return f"Output[{self.name}]"

    def __repr__(self):
        return str(self)

    def _fill_fields(self):
        obj = self._obj
        if self.is_computed_at_model_time():
            self.computation_time = extract_code(obj.ComputationTimeCode)
            self.computation_unit = obj.ComputationTimeCode.Unit.pyval
        elif self.is_computed_at_calendar_date():
            self.computation_date = datetime.fromtimestamp(obj.ComputationDate.pyval/1000.0)

    def _delete_irrelevant_fields(self):
        if not self.is_computed_at_model_time():
            del self.computation_time
            del self.computation_unit

        if not self.is_computed_at_calendar_date():
            del self.computation_date

    def is_computed_on_sim_end(self):
        return self.computation_moment == "ON_SIMULATION_END"

    def is_computed_at_model_time(self):
        return self.computation_moment == "AT_MODEL_TIME"
    
    def is_computed_manually(self):
        return self.computation_moment == "MANUALLY"

    def is_computed_at_calendar_date(self):
        return self.computation_moment == "AT_CALENDAR_DATE"


class Statistics: ## TODO
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Statistics")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
    
    def __str__(self):
        return f"Statistics[{self.name}]"

    def __repr__(self):
        return str(self)

class DataSet: ## TODO
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "DataSet")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")

class HistogramData: ## TODO
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "HistogramData")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")

    def __str__(self):
        return f"HistogramData[{self.name}]"

    def __repr__(self):
        return str(self)

class Histogram2DData: ## TODO
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Histogram2DData")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")

    def __str__(self):
        return f"Histogram2DData[{self.name}]"

    def __repr__(self):
        return str(self)