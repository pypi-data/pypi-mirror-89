from enum import Enum

from pm4py.objects.dfg.retrieval.pandas import get_partial_order_dataframe
from pm4py.util import exec_utils, constants, xes_constants


class Parameters(Enum):
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    START_TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY
    KEEP_FIRST_FOLLOWING = "keep_first_following"


def apply(dataframe, parameters=None):
    if parameters is None:
        parameters = {}

    if parameters is None:
        parameters = {}

    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes_constants.DEFAULT_NAME_KEY)
    case_id_glue = exec_utils.get_param_value(Parameters.CASE_ID_KEY, parameters, constants.CASE_CONCEPT_NAME)
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters,
                                               xes_constants.DEFAULT_TIMESTAMP_KEY)
    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, None)
    keep_first_following = exec_utils.get_param_value(Parameters.KEEP_FIRST_FOLLOWING, parameters, False)

    partial_order_dataframe = get_partial_order_dataframe(dataframe, start_timestamp_key=start_timestamp_key,
                                                          timestamp_key=timestamp_key, case_id_glue=case_id_glue,
                                                          activity_key=activity_key,
                                                          keep_first_following=keep_first_following)

    ret_dict = partial_order_dataframe.groupby([activity_key, activity_key + '_2']).size().to_dict()

    # assure to avoid problems with np.float64, by using the Python float type
    for el in ret_dict:
        ret_dict[el] = int(ret_dict[el])

    return ret_dict
