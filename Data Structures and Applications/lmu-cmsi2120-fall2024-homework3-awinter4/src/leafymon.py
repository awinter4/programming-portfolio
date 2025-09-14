from damage_type import DamageType
from saalmon import Saalmon
from dataclasses import *
from typing import Any

@dataclass
class Leafymon(Saalmon):
    '''
    Plant-like Saalmon that takes reduced damage from DAMPY damage
    but bonus damage from BURNY damage
    '''
    starting_health = 20
    damage_type = DamageType.LEAFY
    damage_modifier = 3

    def __init__(self, level: int, health: int=starting_health) -> None:
        '''
        Constructs a new Leafymon with the given starting level and health
        values. If no health is given, starts with 20 HP by default.

        :param level: this Leafymon's starting level
        :param health: this Leafymon's starting health (20 by default)
        '''
        super().__init__(level, health, Leafymon.damage_type)

    def take_damage(self, dmg: int, type: DamageType) -> int:
        '''
        Leafymon take bonus BURNY damage, but
        reduced DAMPY damage
        '''
        if type == DamageType.DAMPY:
            dmg -= Leafymon.damage_modifier
        elif type == DamageType.BURNY:
            dmg += Leafymon.damage_modifier

        return super().take_damage(dmg, type)
    
    def clone(self) -> 'Leafymon':
        return Leafymon(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)