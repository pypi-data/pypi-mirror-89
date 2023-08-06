from typing import Type, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pyFootyApi.helper.IObject import IObject


class Cache:
    _instance : 'Cache'= None
    @staticmethod
    def instance() -> 'Cache':
        """ Static access method. """
        if Cache._instance == None:
            Cache()
        return Cache._instance

    def __init__(self):
        """ Virtually private constructor. """
        if Cache._instance != None:
            raise PermissionError("You can't create a Cache instance directly. Use .instance")
        else:
            Cache._instance = self

        self._cache = {}

    def add(self,obj : 'IObject'):
        try:
            type_dict = self._cache[obj.type_name()]
        except KeyError: #Type dict doesn't exist yet!
            type_dict = {}

        try:
            type_dict.pop(obj.id)
        except KeyError: #delete if exists
            pass

        type_dict[obj.id] = obj
        self._cache[obj.type_name()] = type_dict

    def get(self,obj_type : Type['IObject'],id : str) -> Union['IObject',None]:
        try:
            return self._cache[obj_type.type_name()][id]
        except KeyError:
            return None

    def get_type(self,obj_type : Type['IObject']) -> Union[List['IObject'],None]:
        try:
            return list(self._cache[obj_type.type_name()].values())
        except KeyError:
            return None





