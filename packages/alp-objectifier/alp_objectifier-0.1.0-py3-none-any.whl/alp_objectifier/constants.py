
import os
import re

from os.path import expanduser, exists, join
from warnings import warn

class ExperimentType:
    SIMULATION = "Simulation"
    OPTIMIZATION = "Optimization"
    PARAMVAR = "ParamVariation"
    COMPARE = "CompareRuns"
    CUSTOM = "Custom"
    REINFORCEMENT_LEARNING = "ReinforcementLearning"

    @staticmethod
    def value_of(exp_type):
        abbv = exp_type[:3].lower()
        if abbv == "sim":
            return ExperimentType.SIMULATION
        elif abbv == "opt":
            return ExperimentType.OPTIMIZATION
        elif abbv == "par":
            return ExperimentType.PARAMVAR
        elif abbv == "com":
            return ExperimentType.COMPARE
        elif abbv == "cus":
            return ExperimentType.CUSTOM
        elif abbv == "rei":
            return ExperimentType.REINFORCEMENT_LEARNING
        else:
            raise ValueError(f"Unrecognized type: {exp_type}")

class AgentRefLocationTypes:
    ''' Types of locations that agents can be referenced from. Used in connections function of util class. '''
    AS_AGENT = "agent"
    AS_VARIABLE = "variable"
    AS_PROPERTY = "property"
    IN_CODE = "code"
    _order = [AS_AGENT, AS_VARIABLE, AS_PROPERTY, IN_CODE]

    @staticmethod
    def to_index(location_type):
        return AgentRefLocationTypes._order.index(location_type)

    


def find_user_model_folder():
    ''' Get default model location from anylogic preferences file (and clean up unneccessary escapes) '''
    pref_file = expanduser(r"~\.AnyLogicProfessional\Workspace8.7\.metadata\.plugins\org.eclipse.core.runtime\.settings\com.anylogic.preferences.prefs".replace("\\", os.sep))
    folder = None
    with open(pref_file) as f:
        match = re.search("AnyLogic.DefaultModelLocation=([^\n]+)", f.read())
        if match is not None:
            # User has defined a custom model location
            folder = match.group(1).replace("\\:", ":").replace("\\\\", "\\").replace("\\", os.sep)
        else:
            # User has kept the default location
            folder = expanduser(r"~\Models".replace("\\", os.sep))

    if folder is None or not exists(folder):
        warn("Could not find location of AnyLogic user models; please manually set `USER_MODEL_FOLDER`")
    return folder

def find_AL_model_folder():
    ''' Get location of AL example models '''
    folder = None
    if os.name == "nt":
        folder = r"C:\ProgramData\AnyLogic 8.7 Professional\eclipse\plugins"
    elif os.name == "posix":
        folder = "/opt/anylogic/plugins"

    if exists(folder):
        # Look for a 8.5 build
        subfolders = os.listdir(folder)
        if subfolders: # Add it to the folder path if found
            folder = os.path.join(folder, subfolders[0])
        else: # Otherwise set to None so user is warned
            folder = None

    if folder is None or not exists(folder):
        warn("Could not find location of AnyLogic example models; please manually set `AL_MODEL_FOLDER`")
    return folder



    
USER_MODEL_FOLDER = find_user_model_folder()
USER_ALPS = [join(root, file) for root, folds, files in os.walk(USER_MODEL_FOLDER, followlinks=True) for file in files if file.endswith(".alp")]
AL_MODEL_FOLDER = find_AL_model_folder()
AL_ALPS = [join(root, file) for root, folds, files in os.walk(AL_MODEL_FOLDER, followlinks=True) for file in files if file.endswith(".alp")]
ALPS = USER_ALPS + AL_ALPS




