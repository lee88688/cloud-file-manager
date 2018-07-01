import requests
from functools import partial


class Aria2(object):

    URL_FORMAT = 'http://{host}:{port}/jsonrpc'
    ID_PREFIX = 'pyaria2'

    def __init__(self, host, port, token=None):
        self._host = host
        self._port = port
        self._token = token

    def _rpc(self, method, *option):
        if type(method) is not str:
            raise TypeError('method must be str type')

        payload = {
            'jsonrpc': '2.0',
            'id': self.ID_PREFIX,
            'method': 'aria2.' + method,
            'params': []
        }

        if len(option) == 0 and self._token is None:
            payload.pop('params')  # remove params
        else:
            if self._token is not None:
                payload['params'].append('token:' + self._token)
            payload['params'].extend(option)

        r = requests.post(self.URL_FORMAT.format(host=self._host, port=self._port), json=payload)
        return r

    def __getattr__(self, attr):
        func = partial(self._rpc, attr)

        def wrap(*args, **kargs):
            r = func(*args, **kargs)
            if 'error' not in r.json():
                self.__dict__[attr] = func
            return r.json()

        return wrap
