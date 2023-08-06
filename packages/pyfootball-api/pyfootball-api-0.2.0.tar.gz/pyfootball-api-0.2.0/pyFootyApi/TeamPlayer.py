import re
from copy import deepcopy
from datetime import timedelta, datetime
from typing import TYPE_CHECKING, Union, List, Optional, Dict

import pytz

from pyFootyApi.Country import Country
from pyFootyApi.helper.Cache import Cache
from pyFootyApi.helper.IObject import IObject, query


class LeagueSeason:
    def __init__(self, **kwargs):
        self._year = kwargs['year']
        if kwargs['start'] is not None:
            self._start = datetime.strptime(kwargs['start'], "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        else:
            self._start = None

        if kwargs['end']:
            self._end = datetime.strptime(kwargs['end'], "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        else:
            self._end = None

        self._current = kwargs['current']

        coverage_dict = kwargs['coverage']
        fixture_dict = coverage_dict['fixtures']
        self._events = fixture_dict['events']
        self._lineups = fixture_dict['lineups']
        self._statistics_fixtures = fixture_dict['statistics_fixtures']
        self._statistics_players = fixture_dict['statistics_players']

        self._standings = coverage_dict['standings']
        self._players = coverage_dict['players']
        self._top_scorers = coverage_dict['top_scorers']
        self._predictions = coverage_dict['predictions']
        self._odds = coverage_dict['odds']
        self._league = kwargs['league']

    @property
    def year(self) -> int:
        return self._year

    @property
    def start(self) -> datetime:
        return self._start

    @property
    def end(self) -> datetime:
        return self._end

    @property
    def current(self) -> bool:
        return self._current

    @property
    def events(self) -> bool:
        return self._events

    @property
    def lineups(self) -> bool:
        return self._lineups

    @property
    def statistics_fixtures(self) -> bool:
        return self._statistics_fixtures

    @property
    def statistics_players(self) -> bool:
        return self._statistics_players

    @property
    def standings(self) -> bool:
        return self._standings

    @property
    def players(self) -> bool:
        return self._players

    @property
    def top_scorers(self) -> bool:
        return self._top_scorers

    @property
    def predictions(self) -> bool:
        return self._predictions

    @property
    def odds(self) -> bool:
        return self._odds

    @property
    def league(self) -> 'League':
        return self._league

    def __repr__(self):
        return f"{self.league.name}({self._year}"


class League(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)
        self._id = kwargs['league']['id']
        self._name = kwargs['league']['name']
        self._type = kwargs['league']['type']
        self._logo = kwargs['league']['logo']

        self._country = Cache.instance().get(Country, kwargs['country']['name'])
        if self._country is None:
            self._country = Country(api_key, **query(Country, {'name': kwargs['country']['name']}, self.headers)[0])

        self._country.add_league(self)

        self._season_dict = {}
        self._team_dict = {}
        self._fixtures = {}
        self._current_season = None
        for season in kwargs['seasons']:
            self._season_dict[season['year']] = LeagueSeason(**season, league=self)
            if self._season_dict[season['year']].current:
                self._current_season = self._season_dict[season['year']]

        Cache.instance().add(self)

    def get_teams(self, season: Union[LeagueSeason, int] = None) -> List['Team']:
        if season is None:
            season = self._current_season
        else:
            year = season.year if isinstance(season, LeagueSeason) else season
            try:
                season = self._season_dict[year]
            except KeyError:
                season = None

        if season is None:
            return None

        if season in self._team_dict.keys():
            return self._team_dict[season]

        teams = query(Team, {'league': self.id, 'season': season._year}, self.headers)
        teams = [Team(self._api_key, **i) for i in teams]
        for team in teams:
            team.update_statistics(season)

        self._team_dict[season] = teams
        return self._team_dict[season]

    def get_season(self, year=None) -> LeagueSeason:
        if year is None:
            season = self._current_season
        else:
            try:
                season = self._season_dict[year]
            except KeyError:
                season = None

        return season

    def get_fixtures(self, season=None) -> List['Fixture']:
        if season is None:
            season = self._current_season
        else:
            year = season.year if isinstance(season, LeagueSeason) else season
            try:
                season = self._season_dict[year]
            except KeyError:
                season = None

        if season is None:
            return None

        if season.year in self._fixtures.keys():
            return self._fixtures[season.year]

        self.get_teams(
            season)  # Downloading all teams in said league for a given season, to reduce number of query hits

        fixtures = query(Fixture, {'league': self._id, 'season': season.year}, self.headers)
        if season.year not in self._fixtures.keys():
            self._fixtures[season.year] = []

        for i in fixtures:
            self._fixtures[season.year].append(Fixture(self._api_key,season=season, **i))

        return self._fixtures[season.year]

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def logo(self) -> str:
        return self._logo

    @property
    def country(self) -> Country:
        return self._country

    @property
    def current_season(self):
        return self._current_season

    @staticmethod
    def endpoint() -> str:
        return "leagues"

    @staticmethod
    def type_name() -> str:
        return 'league'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return f"{self._name} in {self._country.name}"


class Venue(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)
        self._id = kwargs['id']
        self._name = kwargs['name']
        self._address = kwargs['address']
        self._city = kwargs['city']
        if 'country' in kwargs.keys():
            self._country = kwargs['country']
        else:
            self._country = None
        self._capacity = kwargs['capacity']
        self._surface = kwargs['surface']
        self._image = kwargs['image']
        Cache.instance().add(self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        if self._country is None:
            venue = query(Venue, {'id': self._id}, self.headers)
            self._country = venue['country']
        return self._country

    @property
    def capacity(self):
        return self._capacity

    @property
    def surface(self):
        return self._surface

    @property
    def image(self):
        return self._image

    @staticmethod
    def endpoint() -> str:
        return "venues"

    @staticmethod
    def type_name() -> str:
        return 'venue'

    @staticmethod
    def expiration_time() -> timedelta:
        return None

    def __repr__(self):
        return f"{self.name}"


class Matches:
    def __init__(self, **kwargs):
        self._home = kwargs['home']
        self._away = kwargs['away']
        self._total = kwargs['total']

    @property
    def home(self):
        return self._home

    @property
    def away(self):
        return self._away

    @property
    def total(self):
        return self._total


class TeamStatistics(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)

        self._team = kwargs['teamObj']

        self._league: 'League' = kwargs['leagueSeason'].league

        self._leagueSeason = kwargs['leagueSeason']

        self._id = f"{self._team.id}_{self._league.id}_{self._leagueSeason.year}"

        self._played = Matches(**kwargs['fixtures']['played'])
        self._wins = Matches(**kwargs['fixtures']['wins'])
        self._draws = Matches(**kwargs['fixtures']['draws'])
        self._losses = Matches(**kwargs['fixtures']['loses'])
        self._goals_total_for = Matches(**kwargs['goals']['for']['total'])
        self._goals_average_for = Matches(**kwargs['goals']['for']['average'])
        self._goals_total_against = Matches(**kwargs['goals']['against']['total'])
        self._goals_average_against = Matches(**kwargs['goals']['against']['average'])

    @property
    def id(self):
        return self._id

    @staticmethod
    def endpoint() -> str:
        return "teams/statistics"

    @staticmethod
    def type_name() -> str:
        return 'teamstats'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)


class Team(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)
        self._id = kwargs['team']['id']
        self._name = kwargs['team']['name']
        if kwargs['team']['country'] == "United States":
            kwargs['team']['country'] = "USA"
        elif kwargs['team']['country'] == "Equatorial Guinea":
            kwargs['team']['country'] = "Guinea"
        elif kwargs['team']['country'] == 'Côte d\'Ivoire':
            kwargs['team']['country'] = "Ivory Coast"
        elif kwargs['team']['country'] == 'Korea Republic':
            kwargs['team']['country'] = 'South Korea'
        elif kwargs['team']['country'] == 'Bosnia and Herzegovina':
            kwargs['team']['country'] = 'Bosnia'
        self._country = Cache.instance().get(Country, kwargs['team']['country'])
        if self._country is None:
            try:
                self._country = Country(api_key, **query(Country, {'name': kwargs['team']['country']}, self.headers)[0])
            except:
                self._country = kwargs['team']['country']

        if isinstance(self._country, Country):
            self._country.add_team(self)

        self._founded = kwargs['team']['founded']
        self._national = kwargs['team']['national']
        self._logo = kwargs['team']['logo']
        self._statistics = {}
        self._players = {}
        self._competitions = {}

        self._venue = Cache.instance().get(Venue, kwargs['venue']['id'])
        if self._venue is None:
            self._venue = Venue(api_key, **kwargs['venue'])
        Cache.instance().add(self)

    def update_statistics(self, season: 'LeagueSeason'):
        statistics = query(TeamStatistics, {'league': season.league._id, 'season': f"{season.year}", 'team': self._id},
                           self.headers)
        if season.league._name not in self._statistics.keys():
            self._statistics[season.league._name] = {}

        self._statistics[season.league._name][season.year] = TeamStatistics(self._api_key, **statistics,
                                                                            leagueSeason=season, teamObj=self)

    def get_statistics(self, season: 'LeagueSeason'):
        try:
            return self._statistics[season.league._name][season.year]
        except KeyError:
            self.update_statistics(season)
            return self._statistics[season.league._name][season.year]

    def get_players(self, season: Union['LeagueSeason', int]):
        try:
            year = season.year
        except AttributeError:
            year = season

        if year in self._players.keys():
            return self._players[year]

        players = query(Player, {'team': self._id, 'season': year}, self.headers)

        objs = []
        for player in players:
            obj: Union[None, Player] = Cache.instance().get(Player, player['player']['id'])
            if obj is None:
                objs.append(Player(self._api_key, **player))
            else:
                obj._append_stats_data(player['statistics'], player['player']['injured'])
                objs.append(obj)

        self._players[year] = objs

        return objs

    def find_league(self, season: Union['LeagueSeason', int]) -> Union[League, None]:
        try:
            year = season.year
        except AttributeError:
            year = season

        if year in self._competitions.keys() and len([i for i in self._competitions[year] if i.type == "League"]) > 0:
            return [i for i in self._competitions[year] if i.type == "League"][0]

        leagues = query(League, {'team': self._id, 'season': year}, self.headers)
        for league in leagues:
            if Cache.instance().get(League, league['league']['id']) is None:
                league = League(self._api_key, **league)
            else:
                league = Cache.instance().get(League, league['league']['id'])

            if year in self._competitions:
                self._competitions[year].append(league)
            else:
                self._competitions[year] = [league]

        if year in self._competitions.keys() and len([i for i in self._competitions[year] if i.type == "League"]) > 0:
            return [i for i in self._competitions[year] if i.type == "League"][0]
        else:
            return None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def country(self) -> 'Country':
        return self._country

    @property
    def founded(self) -> int:
        return self._founded

    @property
    def national(self) -> bool:
        return self._national

    @property
    def logo(self) -> str:
        return self._logo

    @property
    def statistics(self):
        return self._statistics

    @staticmethod
    def endpoint() -> str:
        return "teams"

    @staticmethod
    def type_name() -> str:
        return 'team'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return self._name


class Substitutes:
    def __init__(self, **sub_dict):
        self._in: int = sub_dict['in']
        self._out: int = sub_dict['out']
        self._bench: int = sub_dict['bench']

    @property
    def subin(self):
        return self._in

    @property
    def subout(self):
        return self._out

    @property
    def bench(self):
        return self._bench


class Shots:
    def __init__(self, **shot_dict):
        self._total = shot_dict['total']
        self._on = shot_dict['on']

    @property
    def total(self):
        return self._total

    @property
    def on(self):
        return self._on


class Goals:
    def __init__(self, **goal_dict):
        self._total: int = goal_dict['total']
        self._conceded: Union[int, None] = goal_dict['conceded']
        self._assists: int = goal_dict['assists']
        self._saves: int = goal_dict['saves']

    @property
    def total(self):
        return self._total

    @property
    def conceded(self):
        return self._conceded

    @property
    def assists(self):
        return self._assists

    @property
    def saves(self):
        return self._saves


class Passes:
    def __init__(self, **pass_dict):
        self._total = pass_dict['total']
        self._key = pass_dict['key']
        self._accuracy = pass_dict['accuracy']

    @property
    def total(self):
        return self._total

    @property
    def key(self):
        return self._key

    @property
    def accuracy(self):
        return self._accuracy


class Tackles:
    def __init__(self, **tackle_dict):
        self._total = tackle_dict['total']
        self._blocks = tackle_dict['blocks']
        self._interceptions = tackle_dict['interceptions']

    @property
    def total(self):
        return self._total

    @property
    def blocks(self):
        return self._blocks

    @property
    def interceptions(self):
        return self._interceptions


class Duels:
    def __init__(self, **duel_dict):
        self._total = duel_dict['total']
        self._won = duel_dict['won']

    @property
    def total(self):
        return self._total

    @property
    def won(self):
        return self._won


class Dribbles:
    def __init__(self, **dribble_dict):
        self._attempts = dribble_dict['attempts']
        self._success = dribble_dict['success']
        self._past = dribble_dict['past']

    @property
    def attempts(self):
        return self._attempts

    @property
    def success(self):
        return self._success

    @property
    def past(self):
        return self._past


class Fouls:
    def __init__(self, **foul_dict):
        self._drawn = foul_dict['drawn']
        self._committed = foul_dict['committed']

    @property
    def drawn(self):
        return self._drawn

    @property
    def committed(self):
        return self._committed


class Cards:
    def __init__(self, **card_dict):
        self._yellow = card_dict['yellow']
        self._yellowred = card_dict['yellowred']
        self._red = card_dict['red']

    @property
    def yellow(self):
        return self._yellow

    @property
    def yellowred(self):
        return self._yellowred

    @property
    def red(self):
        return self._red


class Penalty:
    def __init__(self, **penalty_dict):
        self._won = penalty_dict['won']
        self._commited = penalty_dict['commited']
        self._scored = penalty_dict['scored']
        self._missed = penalty_dict['missed']
        self._saved = penalty_dict['saved']


class Games:
    def __init__(self, **game_dict):
        self._appearences = game_dict['appearences']
        self._lineups = game_dict['lineups']
        self._minutes = game_dict['minutes']
        self._number = game_dict['number']
        self._position = game_dict['position']
        self._rating = game_dict['rating']
        self._captain = game_dict['captain']

    @property
    def appearances(self) -> int:
        return self._appearences

    @property
    def lineups(self) -> int:
        return self._lineups

    @property
    def minutes(self) -> int:
        return self._minutes if self._minutes is not None else 0

    @property
    def number(self) -> int:
        return self._number

    @property
    def position(self) -> str:
        return self._position

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def captain(self) -> bool:
        return self._captain


class PlayerStats:
    def __init__(self, league_season: LeagueSeason, team: Team, player: 'Player', injured: bool, **statistics_dict):
        self._league_season = league_season
        try:
            self._league = league_season.league
        except AttributeError:
            self._league = None
        self._team = team
        self._player = player
        self._injured = injured
        self._games = Games(**statistics_dict['games'])
        self._substitutes = Substitutes(**statistics_dict['substitutes'])
        self._shots = Shots(**statistics_dict['shots'])
        self._goals = Goals(**statistics_dict['goals'])
        self._passes = Passes(**statistics_dict['passes'])
        self._tackles = Tackles(**statistics_dict['tackles'])
        self._duels = Duels(**statistics_dict['duels'])
        self._dribbles = Dribbles(**statistics_dict['dribbles'])
        self._fouls = Fouls(**statistics_dict['fouls'])
        self._cards = Cards(**statistics_dict['cards'])
        self._penalty = Penalty(**statistics_dict['penalty'])

    @property
    def team(self):
        return self._team

    @property
    def player(self):
        return self._player

    @property
    def injured(self):
        return self._injured

    @property
    def substitutes(self):
        return self._substitutes

    @property
    def shots(self):
        return self._shots

    @property
    def goals(self):
        return self._goals

    @property
    def passes(self):
        return self._passes

    @property
    def tackles(self):
        return self._tackles

    @property
    def duels(self):
        return self._duels

    @property
    def dribbles(self):
        return self._dribbles

    @property
    def fouls(self):
        return self._fouls

    @property
    def cards(self):
        return self._cards

    @property
    def penalty(self):
        return self._penalty

    @property
    def games(self):
        return self._games


class PlayerHistory(IObject):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key)
        self._kwargs = kwargs

    @staticmethod
    def endpoint():
        return "/players/seasons"


class Player(IObject):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key)
        player_dict = kwargs['player']

        self._id: int = player_dict['id']
        self._name: str = player_dict['name']
        self._firstname: str = player_dict['firstname']
        self._lastname: str = player_dict['lastname']
        self._age: int = player_dict['age']
        try:
            self._birthdate: datetime = datetime.strptime(player_dict['birth']['date'], '%Y-%m-%d') if \
            player_dict['birth'][
                'date'] is not None else None
        except (ValueError, AttributeError):
            self._birthdate = None
        self._birthplace: str = player_dict['birth']['place']
        self._country: Country = Cache.instance().get(Country, player_dict['birth']['country'])
        self._nationality: Country = Cache.instance().get(Country, player_dict['nationality'])
        self._height: str = player_dict['height']
        self._weight: str = player_dict['weight']
        self._photo: str = player_dict['photo']

        statistics_dict = kwargs['statistics']
        self._playerstats = {}
        self._teamhistory = {}
        self._append_stats_data(statistics_dict, player_dict['injured'])
        Cache.instance().add(self)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def firstname(self):
        return self._firstname

    @property
    def lastname(self):
        return self._lastname

    @property
    def age(self):
        return self._age

    @property
    def birthdate(self):
        return self._birthdate

    @property
    def birthplace(self):
        return self._birthplace

    @property
    def country(self):
        return self._country

    @property
    def nationality(self):
        return self._nationality

    @property
    def height(self):
        return self._height

    @property
    def weight(self):
        return self._weight

    @property
    def photo(self):
        return self._photo

    def get_stats(self, season: Union[LeagueSeason, int], team: Optional[Team] = None):
        try:
            year = season.year
        except AttributeError:
            year = season

        if year in self._playerstats.keys():
            return self._playerstats[year]

        if team is not None:
            players = query(Player, {'id': self._id, 'team': team.id, 'season': year}, self.headers)
        else:
            players = query(Player, {'id': self._id, 'season': year}, self.headers)

        self._append_stats_data(players[0]['statistics'], players[0]['player']['injured'])
        return self._playerstats[year]

    def _append_stats_data(self, statistics_dict: Dict, injured: bool):
        for stats in statistics_dict:
            team = Cache.instance().get(Team, stats['team']['id'])
            if team is None:
                team = query(Team, {'id': stats['team']['id']}, self.headers)
                try:
                    team = Team(self._api_key, **team[0])
                except:
                    if len(team) == 0:
                        continue
                    team = Team(self._api_key, **team[0])
                    return

            if isinstance(stats['league']['season'], str) and "-" in stats['league']['season']:
                stats['league']['season'] = int(stats['league']['season'].split("-")[0])
            else:
                try:
                    stats['league']['season'] = int(stats['league']['season'])
                except ValueError:
                    stats['league']['season'] = int(re.findall(r"(\d{4})", stats['league']['season'])[0])

            league = Cache.instance().get(League, stats['league']['id'])
            if league is None:
                if stats['league']['id'] is None:
                    league = None
                else:
                    league = query(League, {'id': stats['league']['id']}, self.headers)
                    league = League(self._api_key, **league[0])

            if league is not None:
                league_season = league.get_season(stats['league']['season']).year
            else:
                league_season = int(stats['league']['season'])

            if league_season not in self._playerstats.keys():
                self._playerstats[league_season] = {}

            if team not in self._playerstats[league_season].keys():
                self._playerstats[league_season] = {team: {}}

            stats.pop('team')
            self._playerstats[league_season][team][league] = PlayerStats(league_season,
                                                                         team, self,
                                                                         injured,
                                                                         **stats)
        pass

    def get_team_history(self, start_year: Optional[int] = None, end_year: Optional[int] = None):
        years = query(PlayerHistory, {}, self.headers)
        start_year = start_year if start_year is not None and start_year >= min(years) else min(years)
        end_year = end_year if end_year is not None and end_year <= max(years) else max(years)

        chosen_years = [i for i in years if i >= start_year and i <= end_year]

        res_dict = {}

        for year in chosen_years:
            if year in self._teamhistory.keys():
                res_dict = self._teamhistory[year]
                continue

            player_stats = query(Player, {'id': self.id, 'season': year}, self.headers)
            if len(player_stats) == 0:
                continue

            team_objs = []
            og_player_dict = deepcopy(player_stats)
            self._append_stats_data(player_stats[0]['statistics'], player_stats[0]['player']['injured'])
            for stats in og_player_dict[0]['statistics']:
                if 'team' not in stats.keys():
                    continue

                team = Cache.instance().get(Team, stats['team']['id'])
                if team not in team_objs:
                    team_objs.append(team)

            res_dict[year] = team_objs
            self._teamhistory[year] = team_objs

        return res_dict[0] if isinstance(res_dict, list) else res_dict

    @property
    def id(self):
        return self._id

    @staticmethod
    def endpoint() -> str:
        return "players"

    @staticmethod
    def type_name() -> str:
        return 'player'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return self._name


class Rounds(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)

    @property
    def id(self):
        return self._id

    @staticmethod
    def endpoint() -> str:
        return "rounds"

    @staticmethod
    def type_name() -> str:
        return 'round'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return self._name


class Event(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)
        self._fixture : 'Fixture' = kwargs['fixture']
        self._elapsed = kwargs['time']['elapsed']
        self._extra = kwargs['time']['extra']
        if kwargs['team']['id'] is not None:
            self._team = Cache.instance().get(Team, kwargs['team']['id'])
            if self._team is None:
                team = query(Team, {'id': kwargs['team']['id']}, self.headers)
                self._team = Team(api_key, **team[0])
        else:
            self._team = None

        if kwargs['player']['id'] is not None:
            self._player = Cache.instance().get(Player, kwargs['player']['id'])
            if self._player is None:
                player = query(Player, {'id': kwargs['player']['id'],'season':self.fixture._season.year}, self.headers)
                self._player = Player(api_key, **player[0])
        else:
            self._player = None

        if kwargs['assist']['id'] is not None:
            self._assist_player = Cache.instance().get(Player, kwargs['assist']['id'])
            if self._assist_player is None:
                assist_player = query(Player, {'id': kwargs['assist']['id'],'season':self.fixture._season.year}, self.headers)
                self._assist_player = Player(api_key, **assist_player[0])
        else:
            self._assist_player = None

        self._type = kwargs['type']
        self._detail = kwargs['detail']
        self._comments = kwargs['comments']

    @property
    def fixture(self):
        return self._fixture

    @property
    def elapsed(self):
        return self._elapsed

    @property
    def extra(self):
        return self._extra if self._extra is not None else 0

    @property
    def team(self):
        return self._team

    @property
    def player(self):
        return self._player

    @property
    def assist_player(self):
        return self._assist_player

    @property
    def type(self):
        return self._type

    @property
    def detail(self):
        return self._detail

    @property
    def comments(self):
        return self._comments

    @staticmethod
    def endpoint() -> str:
        return "fixtures/events"

    @staticmethod
    def type_name() -> str:
        return 'events'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(minutes=1)

    def __repr__(self):
        return f"{self.fixture}: ({self.elapsed + self.extra}): {self.detail}"


class Fixture(IObject):
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key)
        self._fill_data(**kwargs)

        self._season : LeagueSeason = kwargs['season']
        self._last_fixture_update = datetime.utcnow()
        self._last_event_call = None
        self._events = None
        Cache.instance().add(self)

    def _fill_data(self,**kwargs):
        fixture_dict = kwargs['fixture']
        league_dict = kwargs['league']
        teams_dict = kwargs['teams']
        goals_dict = kwargs['goals']
        score_dict = kwargs['score']

        self._id = fixture_dict['id']
        self._referee = fixture_dict['referee']
        self._date = datetime.strptime(fixture_dict['date'].split("+")[0], "%Y-%m-%dT%H:%M:%S")
        self._timestamp = fixture_dict['timestamp']
        self._period_first = fixture_dict['periods']['first']
        self._period_second = fixture_dict['periods']['second']
        self._venue = Cache.instance().get(Venue, fixture_dict['venue']['id'])
        if self._venue is None:
            venue = query(Venue, {'id': fixture_dict['venue']['id']}, self.headers)
            try:
                self._venue = Venue(self._api_key, **venue[0])
            except IndexError:
                self._venue = None

        self._status_long = fixture_dict['status']['long']
        self._status_short = fixture_dict['status']['short']
        self._elapsed = fixture_dict['status']['elapsed']
        self._league = Cache.instance().get(League, league_dict['id'])
        if self._league is None:
            league = query(League, {'id': league_dict['id']}, self.headers)
            self._league = League(self._api_key, **league[0])

        self._home_team = Cache.instance().get(Team, teams_dict['home']['id'])
        if self._home_team is None:
            home_team = query(Team, {'id': teams_dict['home']['id']}, self.headers)
            self._home_team = Team(self._api_key, **home_team[0])

        self._away_team = Cache.instance().get(Team, teams_dict['away']['id'])
        if self._away_team is None:
            away_team = query(Team, {'id': teams_dict['away']['id']}, self.headers)
            self._away_team = Team(self._api_key, **away_team[0])

        if teams_dict['home']['winner']:
            self._winner = self._home_team
        elif teams_dict['away']['winner']:
            self._winner = self._away_team
        else:
            self._winner = None

        self._home_goals = goals_dict['home']
        self._away_goals = goals_dict['away']

        self._score = {}

        for i in ['halftime', 'fulltime', 'extratime', 'penalty']:
            self._score[i] = {}
            for j in ['home', 'away']:
                self._score[i][j] = score_dict[i][j]

    def update_fixture(self):
        expiration_time = timedelta(minutes=1) if self._status_short not in ['1H', '2H', 'ET', 'P',
                                                                             'HT'] else timedelta(hours=12)

        if datetime.utcnow() - self._last_fixture_update < expiration_time:
            return

        fixture = query(Fixture,{'id':self._id},self.headers)
        self._fill_data(**fixture[0])

    def get_events(self):
        self.update_fixture()
        if self._last_event_call is None or self._events is None:
            must_update = True
        elif self._status_short not in ['1H', '2H', 'ET', 'P']:
            must_update = False
        else:
            time_passed = datetime.utcnow() - self._last_event_call
            if time_passed > Event.expiration_time():
                must_update = True
            else:
                must_update = False

        if not must_update:
            return self._events

        events = query(Event, {'fixture': self._id}, self.headers)

        self._events = [Event(self._api_key,fixture=self, **i) for i in events]
        return self._events

    def _update_events(self):



        pass

    @property
    def id(self):
        return self._id

    @property
    def referee(self):
        return self._referee

    @property
    def date(self):
        return self._date

    @property
    def venue(self):
        return self._venue

    @property
    def status_long(self):
        return self._status_long

    @property
    def status_short(self):
        return self._status_short

    @property
    def elapsed(self):
        return self._elapsed

    @property
    def league(self):
        return self._league

    @property
    def home_team(self):
        return self._home_team

    @property
    def away_team(self):
        return self._away_team

    @property
    def winner(self):
        return self._winner

    @property
    def home_goals(self):
        return self._home_goals

    @property
    def away_goals(self):
        return self._away_goals

    @property
    def score(self):
        return self._score

    @property
    def id(self):
        return self._id

    @staticmethod
    def endpoint() -> str:
        return "fixtures"

    @staticmethod
    def type_name() -> str:
        return 'fixture'

    @staticmethod
    def expiration_time() -> timedelta:
        return timedelta(days=1)

    def __repr__(self):
        return f"{self.date.strftime('%d.%m.%Y %H:%M')}: {self._home_team.name} vs {self._away_team.name}"
