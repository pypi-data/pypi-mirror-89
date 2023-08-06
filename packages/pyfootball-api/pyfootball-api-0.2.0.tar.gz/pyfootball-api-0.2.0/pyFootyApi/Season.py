from datetime import timedelta, datetime

import pytz as pytz

from pyFootyApi.helper.Cache import Cache
from pyFootyApi.helper.IObject import IObject


class Season(IObject):
    def __init__(self,api_key,**kwargs):
        super().__init__(api_key)
        self._year = kwargs['year']
        Cache.instance().add(self)

    @property
    def year(self):
        return self._year

    @property
    def id(self):
        return self._year

    @staticmethod
    def endpoint() -> str:
        return "seasons"

    @staticmethod
    def type_name() -> str:
        return 'season'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return self._year