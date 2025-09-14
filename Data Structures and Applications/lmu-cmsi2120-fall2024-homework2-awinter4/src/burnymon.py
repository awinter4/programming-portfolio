from damage_type import DamageType
from saalmon import Saalmon
from dataclasses import *
from typing import Any

@dataclass
class Burnymon(Saalmon):
    '''
    Fire-based Saalmon that has little health but can deal bonus
    damage to other Saalmon of certain types
    '''
    starting_health = 15
    damage_type = DamageType.BURNY

    def __init__(self, level: int, health: int=starting_health) -> None:
        '''
        Constructs a new Burnymon with the given starting level and health
        values. If no health is given, starts with 15 HP by default.

        :param level: this Burnymon's starting level
        :param health: this Burnymon's starting health (15 by default)
        '''
        super().__init__(level, health, Burnymon.damage_type)

    def clone(self) -> 'Burnymon':
        return Burnymon(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)