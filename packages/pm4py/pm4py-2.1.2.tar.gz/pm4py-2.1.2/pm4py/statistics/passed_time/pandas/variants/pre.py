from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TIMESTAMP_KEY
from pm4py.util.constants import CASE_CONCEPT_NAME
from pm4py.objects.dfg.retrieval import pandas
from pm4py.statistics.parameters import Parameters
from pm4py.util import exec_utils


def apply(df, activity, parameters=None):
    """
    Gets the time passed from each preceding activity

    Parameters
    -------------
    df
        Dataframe
    activity
        Activity that we are considering
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    dictio
        Dictionary containing a 'pre' key with the
        list of aggregates times from each preceding activity to the given activity
    """
    if parameters is None:
        parameters = {}

    case_id_glue = exec_utils.get_param_value(Parameters.CASE_ID_KEY, parameters, CASE_CONCEPT_NAME)
    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, DEFAULT_NAME_KEY)
    timestamp_key = exec_utils.get_param_value(Parameters.TIMESTAMP_KEY, parameters, DEFAULT_TIMESTAMP_KEY)
    start_timestamp_key = exec_utils.get_param_value(Parameters.START_TIMESTAMP_KEY, parameters, None)

    [dfg_frequency, dfg_performance] = pandas.get_dfg_graph(df, measure="both", activity_key=activity_key,
                                           case_id_glue=case_id_glue, timestamp_key=timestamp_key,
                                                            start_timestamp_key=start_timestamp_key)

    pre = []
    sum_perf_pre = 0.0
    sum_acti_pre = 0.0

    for entry in dfg_performance.keys():
        if entry[1] == activity:
            pre.append([entry[0], float(dfg_performance[entry]), int(dfg_frequency[entry])])
            sum_perf_pre = sum_perf_pre + float(dfg_performance[entry]) * float(dfg_frequency[entry])
            sum_acti_pre = sum_acti_pre + float(dfg_frequency[entry])

    perf_acti_pre = 0.0
    if sum_acti_pre > 0:
        perf_acti_pre = sum_perf_pre / sum_acti_pre

    return {"pre": pre, "pre_avg_perf": perf_acti_pre}
