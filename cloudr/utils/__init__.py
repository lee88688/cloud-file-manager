

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


def change_path_prefix(path, path_prefix, new_path_prefix):
    '''
    this function changes the path's prefix. like
    ('/123/345', '/123', '/') => '/345'
    ('/123/345', '/123', '/222') => '/222/345'
    '''
    if path_prefix not in path or path.index(path_prefix) != 0:
        raise ValueError('path_prefix must in path, or path_prefix must at start of the path.')
    if new_path_prefix == path_prefix:
        return path

    if new_path_prefix == '/':
        return path[len(path_prefix):]
    elif path_prefix == '/':
        return new_path_prefix + path
    else:
        return new_path_prefix + path[len(path_prefix):]
