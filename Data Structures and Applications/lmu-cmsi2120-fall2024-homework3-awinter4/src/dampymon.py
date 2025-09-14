from damage_type import DamageType
from saalmon import Saalmon
from dataclasses import *
from typing import Any

@dataclass
class Dampymon(Saalmon):
    '''
    Water-pale Saalmon that takes bonus BURNY damage.
    '''
    starting_health = 25
    damage_type = DamageType.DAMPY
    damage_modifier = 5

    def __init__(self, level: int, health: int=starting_health) -> None:
        '''
        Constructs a new Dampymon with the given starting level and health
        values. If no health is given, starts with 25 HP by default.

        :param level: this Dampymon's starting level
        :param health: this Dampymon's starting health (25 by default)
        '''
        super().__init__(level, health, Dampymon.damage_type)

    def take_damage(self, dmg: int, type: DamageType) -> int:
        '''Dampymon take bonus BURNY damage.'''
        if type == DamageType.BURNY:
            dmg += Dampymon.damage_modifier

        return super().take_damage(dmg, type)

    def clone(self) -> 'Dampymon':
        return Dampymon(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)