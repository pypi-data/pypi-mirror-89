from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement
from datetime import datetime
from typing import Dict, Any
from alp_objectifier.util import extract_pyval

class Event:
    def __init__(self, obj: ObjectifiedElement): 
        assertTag(obj.tag, "Event")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        props = obj.Properties
        self.trigger_type = props.get("TriggerType") # timeout, rate, condition

        # conditional tags (all exist, only set those that apply)
        self.mode = None # occuresOnce, cyclic, userControls

        self.timeout_from_db = False
        self.timeout_time = None # may be a string if pulling from a db
        self.timeout_unit = None

        self.rate_from_db = False
        self.rate_time = None # may be a string if pulling from a db
        self.rate_unit = None

        self.occurrence_from_db = False
        self.occurrence_date = None
        self.occurrence_time = None # may be a string if pulling from a db
        self.occurrence_unit = None

        self.recurrence_from_db = False
        self.recurrence_rate = None # may be a string if pulling from a db
        self.recurrence_unit = None

        self.condition = None

        self.action = None

        self._fill_fields()
        self._delete_irrelevant_fields()

    def __str__(self):
        return f"Event[{self.name}]"

    def __repr__(self):
        return str(self)

    def _fill_fields(self):
        props = self._obj.Properties
        if self.trigger_type == "timeout":
            self.mode = props.get("Mode")
            if self.mode == "userControls": # timeout is only used for "user controlled"
                try:
                    self.timeout_time = props.Timeout.Code.pyval
                except: # database reference
                    self.timeout_from_db = True
                    col = props.Timeout.Value.ColumnReference
                    self.timeout_time = f"{col.ClassName.pyval}.{col.ItemName.pyval}"
                self.timeout_unit = props.Timeout.Unit.pyval
            else: # occurrence vars for once/cyclic
                at_time = props.OccurrenceAtTime.pyval
                if at_time: # assign first occurrence at time
                    try:
                        self.occurrence_time = props.OccurrenceTime.Code.pyval
                    except: # database reference
                        self.occurrence_from_db = True
                        col = props.OccurrenceTime.Value.ColumnReference
                        self.occurrence_time = f"{col.ClassName.pyval}.{col.ItemName.pyval}"
                    self.occurrence_unit = props.OccurrenceTime.Unit.pyval
                else: # assign first occurrence at date
                    self.occurrence_date = datetime.fromtimestamp(props.OccurrenceDate.pyval/1000.0)

                if self.mode == "cyclic": # set cyclic recurrence information
                    try:
                        self.recurrence_rate = props.RecurrenceCode.Code.pyval
                    except: # database reference
                        self.recurrence_from_db = True
                        col = props.RecurrenceCode.Value.ColumnReference
                        self.recurrence_rate = f"{col.ClassName.pyval}.{col.ItemName.pyval}"
                    self.recurrence_unit = props.RecurrenceCode.Unit.pyval

        elif self.trigger_type == "rate":
            try :
                self.rate_time = props.Rate.Code.pyval
            except: # database reference
                self.rate_from_db = True
                col = props.Rate.Value.ColumnReference
                self.rate_time = f"{col.ClassName.pyval}.{col.ItemName.pyval}"
            self.rate_unit = props.Rate.Unit.pyval
        else: # condition
            self.condition = props.Condition.pyval
        
        actObj = self._obj.find("Action")
        if actObj is not None:
            self.action = actObj.pyval


    def _delete_irrelevant_fields(self):
        if self.mode is None or self.mode != "cyclic":
            # only cyclic mode has recurrence
            del self.recurrence_from_db
            del self.recurrence_rate
            del self.recurrence_unit
        if self.mode is None or self.mode == "userControls":
            # both occurs once and cyclic modes have occurrence
            del self.occurrence_from_db
            del self.occurrence_date
            del self.occurrence_time
            del self.occurrence_unit
        if self.mode is None or self.mode != "userControls":
            # only user controls mode has timeout
            del self.timeout_from_db
            del self.timeout_time
            del self.timeout_unit
        if self.mode is not None or self.trigger_type != "condition":
            # only conditional trigger type has condition
            del self.condition
        if self.mode is not None or self.trigger_type != "rate":
            # only rate trigger type has rate
            del self.rate_from_db
            del self.rate_time
            del self.rate_unit

        # rate/condition types do not have a 'mode'
        if self.trigger_type != "timeout":
            del self.mode
        
        # cyclic or occurs once modes can have date OR time
        try:
            if self.occurrence_date is None:
                del self.occurrence_date
            else:
                del self.occurrence_time
                del self.occurrence_unit
        except:
            pass

    def is_timeout_trigger(self):
        return self.trigger_type == "timeout"

    def is_rate_trigger(self):
        return self.trigger_type == "rate"
    
    def is_conditional_trigger(self):
        return self.trigger_type == "condition"

    def is_cyclic(self):
        return self.is_timeout_trigger() and self.mode == "cyclic"

    def is_user_controlled(self):
        return self.is_timeout_trigger() and self.mode == "userControls"

    def is_occurs_once(self):
        return self.is_timeout_trigger() and self.mode == "occuresOnce"

    def pulls_from_db(self):
        ''' Checks whether any of the values in this object pull from the database '''
        classvars = vars(self)
        for n, v in classvars.items():
            if "_from_db" in n:
                return v
        return False

    def get_values(self):
        ''' A type-agnostic way to get the trigger values. 
        Returns the non-None values for the following list, in the specified order:
            occurrence date, occurrence time, occurrence unit,
            recurrence date, recurrence time, recurrence unit,
            timeout time, timeout unit
            rate time, rate unit,
            condition
        '''
        priority = [
            'occurrence_date', 'occurrence_time', 'occurrence_unit',
            'recurrence_date', 'recurrence_rate', 'recurrence_unit',
            'timeout_time', 'timeout_unit',
            'rate_time', 'rate_unit',
            'condition'
        ]
        classvars = vars(self)
        values = []
        for n in priority:
            v = classvars.get(n, None)
            if v is not None:
                values.append(v)
        return values

        

class DynamicEvent:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "DynamicEventClass")
        self._obj = obj
        self.name = obj.Name.pyval
        self.description = extract_pyval(obj, "Description", "")
        
        # technically optional fields; fill out in function
        self.action = None
        self.arguments = []

        self._fill_fields()

    def __str__(self):
        return f"DynamicEvent[{self.name}]"

    def __repr__(self):
        return str(self)

    def _fill_fields(self):
        obj = self._obj

        actObj = obj.find("Action")
        if actObj is not None:
            self.action = actObj.pyval
        
        if obj.find("Parameter") is not None:
            for arg in obj.Parameter:
                self.arguments.append( (arg.Name.pyval, arg.Type.pyval) )

    def has_arguments(self):
        return len(self.arguments) > 0

