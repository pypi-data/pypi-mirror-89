import json
from datetime import timedelta, datetime
from typing import Generic, TypeVar, Dict, Type, Union, List

import requests

from pyFootyApi.helper.Cache import Cache

api_dict = {
    2: "https://v2.api-football.com",
    3: "https://v3.football.api-sports.io"
}

api_version=3

class HTTP404Error(Exception):
    def __init__(self,msg:str):
        self._msg = msg

T = TypeVar('T')

class IObject(Generic[T]):
    def __init__(self,api_key : str):
        self._api_key = api_key
        self._headers = {
            'x-rapidapi-host': "https://v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }
        self._created_at = datetime.utcnow()


    @staticmethod
    def endpoint() -> str:
        raise NotImplementedError("You need to implement the endpoint for this object")

    @staticmethod
    def expiration_time() -> timedelta:
        raise NotImplementedError("You need to implement an expiration time for this object")

    @staticmethod
    def type_name() -> str:
        raise NotImplementedError("You need to provide a type name for this object")

    @property
    def id(self):
        raise NotImplementedError("You need to provide an id for this object")

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def expired(self):
        return datetime.utcnow() > self.created_at + self.expiration_time()

    def query(self,params : Dict[str,str]):
        endpoint = self.endpoint() if self.endpoint().startswith('/') else "/" + self.endpoint()
        resp = requests.get(api_dict[api_version] + endpoint,headers=self._headers,params= params)

        if resp.status_code != 200:
            raise HTTP404Error("Query failed")

        return json.loads(resp.content)

    @property
    def headers(self) -> Dict[str,str]:
        return self._headers

query_list = []

def query(obj_type : Union[Type[IObject],IObject],params : Dict[str,str],headers : Dict[str,str]) -> Dict:
    endpoint = obj_type.endpoint() if obj_type.endpoint().startswith('/') else "/" + obj_type.endpoint()
    resp = requests.get(api_dict[api_version] + endpoint,headers=headers,params= params)

    if resp.status_code != 200:
        raise HTTP404Error("Query failed")

    data = json.loads(resp.content)
    resp_data : Union[List,Dict]= data['response']
    if data['paging']['current'] != data['paging']['total']:
        params['page'] = data['paging']['current'] +1
        rec_data = query(obj_type,params,headers)
        resp_data += rec_data

    query_list.append(datetime.utcnow())
    return  resp_data
