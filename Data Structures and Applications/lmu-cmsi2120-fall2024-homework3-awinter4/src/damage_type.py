'''
Describes the different types of damage that Saalmon
may endure in the arena -- everything from torrents of
flame to trickles of water goes in here!
'''
from enum import Enum

DamageType = Enum('DamageType', ['BASIC', 'BURNY', 'DAMPY', 'ZAPPY', 'LEAFY'])