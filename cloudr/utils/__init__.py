

SUCCESS_RESULT = "success"
FAILURE_RESULT = "failure"


def api_result(result, reason=None, **kwargs):
    rv = {}
    if result == SUCCESS_RESULT:
        rv["result"] = SUCCESS_RESULT
    else:
        rv["result"] = FAILURE_RESULT

    if reason:
        rv["reason"] = reason

    rv.update(kwargs)

    return rv
