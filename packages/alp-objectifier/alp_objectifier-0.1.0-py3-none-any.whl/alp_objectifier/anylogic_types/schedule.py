from ..exceptions import assertTag
from lxml.objectify import ObjectifiedElement

class Schedule:
    def __init__(self, obj: ObjectifiedElement):
        assertTag(obj.tag, "Schedule")
        self._obj = obj
        
        # common/known existing fields
        self.name = obj.Name.pyval
        self.type = obj.ValueType.pyval # integer, double_, onOff (real vs Rate defined by precense of units)
        self.defined_by = obj.RepresentationMode.pyval # exactTimes, intervals
        self.duration_type = obj.RepresentationType.pyval # week, calendar, timeUnits
        
        # optional fields (depending on common field settings)
        # set all values to none by default and fix in separate function
        self.rate_units = None # (only for double_ / "Rate")

        self.default_value = None # (only for interval)
        
        self.repeat_time_ms = None # time in ms for repeat unit
        self.repeat_unit = None # milliseconds,seconds,minutes,hours,days,weeks,months,years : only when intervals set to 'days/weeks' or 'custom'

        self.snap_to_ms = None
        self.snap_to_units = None

        self.load_from_db = False
        self.intervals_query = None
        self.intervals = []
        self.exceptions = None

        self._fill_fields()
        self._delete_irrelevant_fields()

    def __str__(self):
        return f"Schedule[{self.name}]"

    def __repr__(self):
        return str(self)

    def _fill_fields(self):
        obj = self._obj

        # has units if double_ and has a unit value
        if obj.UnitType.pyval.lower() != "none":
            self.rate_units = obj.UnitOfValue.pyval
        
        # only intervals has default value and exceptions
        if self.defined_by == "intervals":
            self.default_value = obj.DefaultValue.pyval

            exceptionsObj = obj.Exceptions # will always exist, may not have Exception tag
            self.exceptions = []
            if exceptionsObj.find("Exception") is not None:
                # tuple: annual flag, start time (ms), end time (ms), value (dependent on type)
                for exp in exceptionsObj.Exception:
                    self.exceptions.append(
                        (
                            exp.Annually.pyval,
                            exp.Start.pyval,
                            exp.End.pyval,
                            exp.Value.pyval
                        )
                    )

        # settings for calendar ("days/week") and timeUnits ("custom") duration types
        if self.duration_type != "week":
            # time/repeat interval apply to non-week duration
            if self.duration_type == "calendar": # "days/weeks"
                self.repeat_unit = obj.RepeatTimeInterval.pyval
            else: # == timeUnits # "custom"
                self.repeat_unit = obj.TimeUnitsInterval
            # both have their value tied to the same field
            self.repeat_time_ms = obj.RepeatTime.pyval

            # snap values apply to non-week duration
            if obj.IsSnapTo.pyval:
                self.snap_to_ms = obj.SnapTo.pyval
                # only has a unit for timeUnits duration type ("custom")
                if self.duration_type == "timeUnits":
                    self.snap_to_units = obj.SnapToTimeUnits.pyval

        # database settings
        if obj.LoadFromDatabase.pyval:
            self.load_from_db = True
            table_name, start_col_name, end_col_name, value_col_name = None, None, None, None
            intervalQueryObj = obj.IntervalsQuery
            # wrap each in a try-catch since some may not be filled in
            # (either b/c user error or not needed, e.g., mode is in exact times, not interval)
            try:
                tableRefObj = intervalQueryObj.TableReference
                table_name = tableRefObj.ClassName.pyval
            except:
                pass

            try:
                startColObj = intervalQueryObj.StartColumnReference
                start_col_name = f"{startColObj.ClassName.pyval}.{startColObj.ItemName.pyval}"
            except:
                pass

            try:
                endColObj = intervalQueryObj.EndColumnReference
                end_col_name = f"{endColObj.ClassName.pyval}.{endColObj.ItemName.pyval}"
            except:
                pass

            try:
                valColObj = intervalQueryObj.ValueColumnReference
                val_col_name = f"{valColObj.ClassName.pyval}.{valColObj.ItemName.pyval}"
            except:
                pass
            
            self.intervals_query = (table_name, start_col_name, end_col_name, value_col_name)


        intervalsObj = obj.Intervals
        # will always have an Intervals tag but not necessarily an Interval tag (note the plurality)
        if intervalsObj.find("Interval") is not None:
            self.intervals = []
            # tuple: start time (ms), end time (ms), value (dependent on type)
            for ival in intervalsObj.Interval:
                self.intervals.append(
                        (
                            ival.Start.pyval,
                            ival.End.pyval,
                            ival.Value.pyval
                        )
                    )

    def _delete_irrelevant_fields(self):
        if self.is_defined_by_moments():
            # only intervals have exceptions or a default value
            del self.exceptions
            del self.default_value

        if not self.load_from_db:
            del self.intervals_query

        if self.is_duration_type_week():
            # delete related to: repeat, snap, db-loading
            del self.load_from_db
            del self.rate_units
            del self.repeat_time_ms
            del self.repeat_unit
            del self.snap_to_ms
            del self.snap_to_units
        elif self.is_duration_type_daysweeks():
            # delete snap to if none was set
            if self.snap_to_ms is None:
                del self.snap_to_ms
            # calendar duration never has a unit
            del self.snap_to_units
        elif self.is_duration_type_custom():
            # delete snaps if none was set
            if self.snap_to_ms is None:
                del self.snap_to_ms
                del self.snap_to_units

        try:
            if self.type != "double_":
                assert self.rate_units is None, self.name
                del self.rate_units
        except: # already deleted
            pass

    def is_type_onoff(self):
        return self.type == "onOff"
    
    def is_type_int(self):
        return self.type == "integer"

    def is_type_real(self):
        return self.type == "double_" and self.rate_units is None

    def is_type_rate(self):
        return self.type == "double_" and self.rate_units is not None
        
    def is_defined_by_intervals(self):
        return self.defined_by == "intervals"

    def is_defined_by_moments(self):
        return not self.is_defined_by_intervals()

    def is_duration_type_week(self):
        return self.duration_type == "week"

    def is_duration_type_daysweeks(self):
        return self.duration_type == "calendar"

    def is_duration_type_custom(self):
        return self.duration_type == "timeUnits"


        


    