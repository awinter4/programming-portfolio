from abc import *
from typing import Any
from damage_type import DamageType

class Saalmon(ABC):
    '''
    Pseudo-mystical pets locked in combat for the amusement of our
    viewers! Get your Saalmonagerie ready today!
    '''
    _level: int
    _health: int
    _damage_type: DamageType

    @abstractmethod
    def __init__(self, level: int, health: int, type: DamageType) -> None:
        self._level = level
        self._health = health
        self._damage_type = type
    
    # [!] This is here for mypy's static type-checking; you should
    # not need to modify this method!
    @abstractmethod
    def clone(self) -> 'Saalmon':
        ''':returns: a deep copy of this Saalmon'''
        ...

    def take_damage(self, dmg: int, type: DamageType) -> int:
        '''
        Reduces the Saalmon's health by the amount specified,
        with the potential for bonuses / penalties based on the
        damage type

        :param dmg: amount of damage taken
        :param type: damage type of the damage taken
        :returns: this Saalmon's health remaining
        '''
        
        self._health -= dmg
        return self._health
    
    def get_species(self) -> str:
        '''
        Returns a string representation of this Saalmon's type,
        e.g., "Burnymon" or "Dampymon"

        :returns: this Saalmon's species
        '''
        return type(self).__name__
    
    def get_health(self) -> int:
        ''':returns: this Saalmon's remaining health'''
        return self._health
    
    def get_level(self) -> int:
        ''':returns: this Saalmon's current level'''
        return self._level
    
    def get_damage_type(self) -> DamageType:
        ''':returns: the damage type that this Saalmon deals in combat'''
        return self._damage_type

    def __str__(self) -> str:
        '''
        Returns a convenient string representation of the Saalmon
        of the format:
        <Type> [<Level>]: <CurrentHealth> HP

        :returns: a string representing this Saalmon's type, level, and health
        '''
        return f'{self.get_species()} [{self.get_level()}]: {self.get_health()} HP'
    
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        ''':returns: whether two Saalmon are the same type, level, and health'''
        return (
            self.__str__() == other.__str__()
            if isinstance(other, type(self))
            else False
        )
    
    def __hash__(self) -> int:
        return hash((self._level, self._health))