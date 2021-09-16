# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.http.response import HttpResponse
from django.db.models import QuerySet
from datetime import datetime, date as datetime_date
from decimal import Decimal
import string
import random
import json
import requests
from django.conf import settings


# 转换时间格式到字符串
def human_datetime(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')


# 转换时间格式到字符串(天)
def human_date(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d')


def human_time(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%H:%M:%S')


# 解析时间类型的数据
def parse_time(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        if len(value) == 10:
            return datetime.strptime(value, '%Y-%m-%d')
        elif len(value) == 19:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    raise TypeError('Expect a datetime.datetime value')


# 传两个时间得到一个时间差
def human_diff_time(time1, time2):
    time1 = parse_time(time1)
    time2 = parse_time(time2)
    delta = time1 - time2 if time1 > time2 else time2 - time1
    if delta.seconds < 60:
        text = '%d秒' % delta.seconds
    elif delta.seconds < 3600:
        text = '%d分' % (delta.seconds / 60)
    else:
        text = '%d小时' % (delta.seconds / 3600)
    return '%d天%s' % (delta.days, text) if delta.days else text


def json_response(data='', error=''):
    content = AttrDict(data=data, error=error)
    if error:
        content.data = ''
    elif hasattr(data, 'to_dict'):
        content.data = data.to_dict()
    elif isinstance(data, (list, QuerySet)) and all([hasattr(item, 'to_dict') for item in data]):
        content.data = [item.to_dict() for item in data]
    return HttpResponse(json.dumps(content, cls=DateTimeEncoder), content_type='application/json')


# 继承自dict，实现可以通过.来操作元素
class AttrDict(dict):
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __delattr__(self, item):
        self.__delitem__(item)


# 日期json序列化
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime_date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, Decimal):
            return float(o)

        return json.JSONEncoder.default(self, o)


# 生成指定长度的随机数
def generate_random_str(length: int = 4, is_digits: bool = True) -> str:
    words = string.digits if is_digits else string.ascii_letters + string.digits
    return ''.join(random.sample(words, length))


def get_request_real_ip(headers: dict):
    x_real_ip = headers.get('x-forwarded-for')
    if not x_real_ip:
        x_real_ip = headers.get('x-real-ip', '')
    return x_real_ip.split(',')[0]


class RequestApiAgent:
    host = None
    timeout = 30
    verify = False
    headers = None
    data = None
    request_map = {
        "create": {
            "method": requests.post,
            "url": "",
            "form_data_keys": [],
            "param_keys": [],
        },
        "delete": {
            "method": requests.delete,
            "url": "",
            "form_data_keys": [],
            "param_keys": [],
        },
        "list": {
            "method": requests.get,
            "url": "",
            "form_data_keys": [],
            "param_keys": [],
        },
        "retrieve": {
            "method": requests.get,
            "url": "",
            "form_data_keys": [],
            "param_keys": [],
        },
        "put": {
            "method": requests.put,
            "url": "",
            "form_data_keys": [],
            "param_keys": [],
        },
        "update": {
            "method": requests.put,
            "url": "",
            "form_data_keys": [],
            "param_keys": [],
        }
    }

    def send_request(self, crud_key, kwargs):
        if crud_key not in self.request_map.keys():
            raise KeyError("Unsupported CRUD_KEY: `{this_key}` ""not in {support_keys}".format(
                this_key=crud_key,
                support_keys=list(self.request_map.keys()))
            )
        request = self.request_map[crud_key]
        return request["method"](
            url=kwargs["url"],
            data=self.data if not kwargs.get("data",None) else kwargs["data"],
            # json=kwargs,
            # params=kwargs,
            # timeout=self.timeout if not kwargs.get("timeout", None) else kwargs["timeout"],
            verify=self.verify if not kwargs.get("verify", None) else kwargs["verify"],
            timeout=self.timeout,
            headers=self.headers if not kwargs.get("headers", None) else kwargs["headers"],
        )

    def create(self, *args, **kwargs):
        # return self.send_request("create", kwargs).json()
        return self.send_request("create", kwargs).text

    def close(self, *args, **kwargs):
        # return self.send_request("close", kwargs).json()
        return self.send_request("close", kwargs).text

    def put(self, *args, **kwargs):
        return self.send_request("put", kwargs).content
        # return self.send_request("put", kwargs).text

    def list(self, *args, **kwargs):
        return self.send_request("list", kwargs)
        # return self.send_request("list", kwargs).text


