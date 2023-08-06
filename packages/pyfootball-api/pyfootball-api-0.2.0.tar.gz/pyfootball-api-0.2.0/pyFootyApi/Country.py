from datetime import timedelta, datetime
from typing import TYPE_CHECKING

import pytz as pytz


if TYPE_CHECKING:
    from pyFootyApi.League import League
    from pyFootyApi.TeamPlayer import Team
from pyFootyApi.helper.Cache import Cache
from pyFootyApi.helper.IObject import IObject


class Country(IObject):
    def __init__(self,api_key,**kwargs):
        super().__init__(api_key)
        self._name = kwargs['name']
        self._code = kwargs['code']
        self._flag = kwargs['flag']
        self._leagues = {}
        self._teams = {}
        Cache.instance().add(self)

    def add_league(self,league : 'League'):
        self._leagues[league.name] = league

    def add_team(self,team : 'Team'):
        self._teams[team.name] = team

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def flag(self):
        return self._flag

    @property
    def id(self):
        return self._name

    @staticmethod
    def endpoint() -> str:
        return "countries"

    @staticmethod
    def type_name() -> str:
        return 'country'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return self._name