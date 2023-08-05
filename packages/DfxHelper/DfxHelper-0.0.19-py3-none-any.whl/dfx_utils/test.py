from dfx_utils.helper import json_friendly_dumps


class SuperDict:
    def __init__(self, _dict: dict = None, _sep='.'):
        self._sep = _sep
        self._dict = _dict or {}

    def __getitem__(self, item):
        if self._sep in item:
            tmp_dict = self._dict
            for key in item.split(self._sep):
                tmp_data = tmp_dict.get(key)
                if tmp_data is not None:
                    if tmp_data and isinstance(tmp_data, dict):
                        tmp_dict = tmp_data
            return tmp_data
        else:
            return self._dict.get(item)

    def __setitem__(self, key, value):
        if self._sep in key:
            tmp_dict = self._dict
            keys = key.split(self._sep)
            for idx, item in enumerate(keys):
                if idx == len(keys) - 1:
                    tmp_dict[item] = value
                else:
                    tmp_dict[item] = tmp_dict.get(item, {})
                    tmp_dict = tmp_dict[item]
        else:
            self._dict[key] = value

    def __getattribute__(self, item):
        try:
            return super(SuperDict, self).__getattribute__(item)
        except AttributeError:
            return self._dict.__getattribute__(item)

    def __str__(self):
        return json_friendly_dumps(self._dict)

    def get(self, item, default=None):
        ret_data = self.__getitem__(item)
        return ret_data if ret_data is not None else default
