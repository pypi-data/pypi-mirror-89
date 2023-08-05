from lxml.objectify import ObjectifiedElement
from alp_objectifier.util import add_class_var_if_tag_exists

# tags in **ALL** Presentation objects:
# (including nested Presentation objects)
# ['Attractor', 'BarChart', 'Control', 'Conveyor', 'ConveyorNetwork', 'ConveyorSimpleStation', 
#   'Curve', 'DensityMap', 'EmbeddedObjectPresentation', 'Figure3D', 'FlowStatistics', 
#   'GISMap', 'GISNetwork', 'GISPoint', 'GISRoute', 'Group', 'Histogram', 'Histogram2D', 
#   'Level', 'Line', 'Oval', 'OvalWall', 'Plot', 'Polyline', 'RailStopline', 'RailTrack', 
#   'Railyard', 'Rectangle', 'RectangleNode', 'Road', 'RoadNetwork', 'RoundedRectangle', 
#   'TargetLine', 'Text']

# in ActiveObject's first tier of Presentation, founds tags:
# ['Level', 'GISMap']
# all others are nested.
class Presentation:
    def __init__(self, obj: ObjectifiedElement):
        self._obj = obj

        self.levels = [Level(o) for o in obj.findall("Level")]

        add_class_var_if_tag_exists(self, "gis_obj", obj, "GISMap")


class Level:
    def __init__(self, obj: ObjectifiedElement):
        self._obj = obj
        self.name = obj.Name.pyval
        self.visibility_mode = obj.LevelVisability.pyval
        pres_obj = obj.find("Presentation")
        if pres_obj is not None:
            self.presentation = Presentation(pres_obj)

class GISMap:
    def __init__(self, obj: ObjectifiedElement):
        self._obj = obj
        pres_obj = obj.find("Presentation")
        if pres_obj is not None:
            self.presentation = Presentation(pres_obj)





