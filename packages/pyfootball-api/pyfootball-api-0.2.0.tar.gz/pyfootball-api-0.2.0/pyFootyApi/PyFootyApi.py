from typing import Union, List

from pyFootyApi.Country import Country
from pyFootyApi.Season import Season
from pyFootyApi.TeamPlayer import Team, League
from pyFootyApi.helper.IObject import query, IObject,Cache

main_countries = [
    'Argentina',
    'Australia',
    'Austria',
    'Belgium',
    'Brazil',
    'Czech-Republic',
    'Denmark',
    'England',
    'France',
    'Germany',
    'Greece',
    'Italy',
    'Mexico',
    'Netherlands',
    'Portugal',
    'Russia',
    'Scotland',
    'Slovakia',
    'Slovenia',
    'Spain',
    'Sudan',
    'Sweden',
    'Switzerland',
    'Turkey',
    'USA',
    'World',
]


class PyFootyApi(IObject):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        countries = query(Country,{},self.headers)

        self._countries = [Country(api_key,**i) for i in countries]
        leagues = query(League,{},self.headers)
        self._leagues = [League(api_key, **i) for i in leagues]

    def get_league(self,name : str) -> Union[League,None]:
        try:
            return [i for i in self._leagues if i.name == name][0]
        except IndexError:
            return None

    @property
    def countries(self):
        if any([i.expired for i in self._countries]):
            countries = query(Country, {}, self.headers)
            self._countries = [Country(self._api_key, **i) for i in countries]

        return self._countries

    @staticmethod
    def type_name() -> str:
        return "ApiObj"

    @property
    def id(self):
        return "1"

    @property
    def leagues(self):
        return self._leagues

    @property
    def countries(self):
        return self._countries

    def search_team(self,name):
        teams = query(Team,{'search':name},self.headers)
        if len(teams) ==0:
            return None

        team_list = []
        for team in teams:
            team_obj = Cache.instance().get(Team,team['team']['id'])
            if team_obj is None:
                team_obj = Team(self._api_key,**team)

            team_list.append(team_obj)

        return team_list


    @property
    def top_5_leagues(self) -> List[League]:
        countries = [i for i in self.countries if i.name in ["France", "Germany", "England", "Spain","Italy"]]
        return [i for i in self.leagues if
                i.name in ['Bundesliga 1','Primera Division', 'Serie A','Premier League'] and i.country in countries]
