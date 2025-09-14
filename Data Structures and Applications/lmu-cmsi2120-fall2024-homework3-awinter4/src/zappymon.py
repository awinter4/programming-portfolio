from damage_type import DamageType
from saalmon import Saalmon
from dataclasses import *
from typing import Any

@dataclass
class Zappymon(Saalmon):
    '''
    Electrical Saalmon that takes bonus damage from DAMPY but
    reduced damage from LEAFY sources
    '''
    starting_health = 20
    damage_type = DamageType.ZAPPY
    damage_modifier = 3

    def __init__(self, level: int, health: int=starting_health) -> None:
        '''
        Constructs a new Zappymon with the given starting level and health
        values. If no health is given, starts with 20 HP by default.

        :param level: this Zappymon's starting level
        :param health: this Zappymon's starting health (20 by default)
        '''
        super().__init__(level, health, Zappymon.damage_type)

    def take_damage(self, dmg: int, type: DamageType) -> int:
        '''
        Zappymon take bonus DAMPY damage, but
        reduced LEAFY damage
        '''
        if type == DamageType.LEAFY:
            dmg -= Zappymon.damage_modifier
        elif type == DamageType.DAMPY:
            dmg += Zappymon.damage_modifier

        return super().take_damage(dmg, type)
    
    def clone(self) -> 'Zappymon':
        return Zappymon(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)