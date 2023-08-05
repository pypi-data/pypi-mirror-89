import random, string, hashlib, json, datetime
from typing import Any


def random_str(length: int) -> str:
    seed = string.digits + string.ascii_letters
    return ''.join(random.choices(seed, k=length))


def md5(_str: str):
    return hashlib.md5(_str.encode()).hexdigest()


def json_encoder(obj: Any):
    """ JSON 序列化, 修复时间 """
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')

    return super().default(obj)


def json_decoder(obj: Any):
    """ JSON 反序列化，加载时间 """
    ret = obj
    if isinstance(obj, list):
        obj = enumerate(obj)
    elif isinstance(obj, dict):
        obj = obj.items()
    else:
        return obj

    for key, item in obj:
        if isinstance(item, (list, dict)):
            ret[key] = json_decoder(item)
        elif isinstance(item, str):
            try:
                ret[key] = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                ret[key] = item
        else:
            ret[key] = item
    return ret


def json_friendly_loads(obj: Any):
    return json.loads(obj, object_hook=json_decoder)


def json_friendly_dumps(obj: Any, **kwargs):
    return json.dumps(obj, ensure_ascii=False, default=json_encoder, **kwargs)


class SuperDict:
    def __init__(self, _dict: dict = None, _sep='.'):
        self._sep = _sep
        self._dict = _dict or {}

    def __getitem__(self, item):
        tmp_data = None
        if self._sep in item:
            tmp_dict = self._dict
            for key in item.split(self._sep):
                tmp_data = tmp_dict.get(key)
                if tmp_data is not None:
                    if tmp_data and isinstance(tmp_data, dict):
                        tmp_dict = tmp_data
        else:
            tmp_data = self._dict.get(item)
        return SuperDict(tmp_data) if isinstance(tmp_data, dict) else tmp_data

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
        """ 当调用的函数不存在时，去self._dict里面找 """
        try:
            return super(SuperDict, self).__getattribute__(item)
        except AttributeError:
            return self._dict.__getattribute__(item)

    def __str__(self):
        return json_friendly_dumps(self._dict)

    def clear(self):
        self._dict = {}

    def get(self, item, default=None):
        ret_data = self.__getitem__(item)
        return ret_data if ret_data is not None else default
