'''
Test Saalmon classes that are used for certain Saalmonagerie methods
'''
from saalmon import Saalmon
from damage_type import DamageType
from typing import Any

class Saalmon0(Saalmon):
    starting_health = 15
    damage_type = DamageType.BASIC

    def __init__(self, level: int, health: int=starting_health):
        super().__init__(level, health, Saalmon0.damage_type)

    def clone(self) -> 'Saalmon0':
        return Saalmon0(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)


class Saalmon1(Saalmon):
    starting_health = 15
    damage_type = DamageType.BASIC

    def __init__(self, level: int, health: int=starting_health):
        super().__init__(level, health, Saalmon1.damage_type)

    def clone(self) -> 'Saalmon1':
        return Saalmon1(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)
    

class Saalmon2(Saalmon):
    starting_health = 15
    damage_type = DamageType.BASIC

    def __init__(self, level: int, health: int=starting_health):
        super().__init__(level, health, Saalmon2.damage_type)

    def clone(self) -> 'Saalmon2':
        return Saalmon2(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)
    

class Saalmon3(Saalmon):
    starting_health = 15
    damage_type = DamageType.BASIC

    def __init__(self, level: int, health: int=starting_health):
        super().__init__(level, health, Saalmon3.damage_type)

    def clone(self) -> 'Saalmon3':
        return Saalmon3(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)
    

class Saalmon4(Saalmon):
    starting_health = 15
    damage_type = DamageType.BASIC

    def __init__(self, level: int, health: int=starting_health):
        super().__init__(level, health, Saalmon4.damage_type)

    def clone(self) -> 'Saalmon4':
        return Saalmon4(self._level, self._health)
    
    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)