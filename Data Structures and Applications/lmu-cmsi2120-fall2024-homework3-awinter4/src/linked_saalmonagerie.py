'''
CMSI 2120 - Homework 3
Author: Andrew Winter

Original Java assignment written by Andrew Forney @forns,
converted to Python by Natalie Lau @nklau.
'''
from saalmon import Saalmon
from saalmonagerie import Saalmonagerie
from dataclasses import dataclass
from typing import Any, Iterator, Optional


class LinkedSaalmonagerie(Saalmonagerie):
    '''
    Collections of Saalmon ready to fight in the arena!
    '''

    # Fields
    # -----------------------------------------------------------
    sentinel: 'Node'
    size: int

    # Constructor
    # -----------------------------------------------------------
    def __init__(self) -> None:
        # [!] Leave this constructor as-is, you may not modify!
        self.size = 0
        self.sentinel = Sentinel()

    # Methods
    # -----------------------------------------------------------

    def empty(self) -> bool:
        """
        Returns true if the LinkedSaalmonagerie has no Saalmon inside, false otherwise.
        """
        return self.size == 0
    
    def collect(self, to_add: Saalmon) -> bool:
        """
        Adds a reference to the given Saalmon to the LinkedSaalmonagerie's collection.
        Returns True if to_add was a newly added species to the LinkedSaalmonagerie, False otherwise.

        param:
        - to_add: The Saalmon instance to be added to the collection.
        """
        current_node = self.sentinel.next_node
        while current_node != self.sentinel:

            if current_node.saalmon == to_add:
                return False
            
            elif current_node.saalmon.get_species() == to_add.get_species():

                if current_node.saalmon.get_level() < to_add.get_level():
                    current_node.saalmon = to_add

                return False

            current_node =  current_node.next_node
        # Add new species at the end 
        new_node = Node(to_add)
        new_node.next_node = self.sentinel
        new_node.prev_node = self.sentinel.prev_node
        self.sentinel.prev_node.next_node = new_node
        self.sentinel.prev_node = new_node
        self.size += 1
        return True
    
    def get(self, index: int) -> Saalmon:
        """
        Returns the Saalmon at the requested index in the collection, if valid.
        If the given index is invalid, raises IndexError().

        param: 
        - index: The position in the collection from which to retrieve the Saalmon.
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index is out of range")
        
        current_node = self.sentinel.next_node
        for i in range(index):
            current_node = current_node.next_node

        return current_node.saalmon

    def get_mvp(self) -> Optional[Saalmon]:
        """
        Returns the "best" Saalmon currently in the collection, or None if the collection is empty,
        defined by by highest level, then highest health, then earliest index if there are ties.
        """
        if self.empty():
            return None

        best = self.sentinel.next_node
        current = best.next_node

        while current != self.sentinel:
            if (
                current.saalmon.get_level() > best.saalmon.get_level() or
                (current.saalmon.get_level() == best.saalmon.get_level() and
                current.saalmon.get_health() > best.saalmon.get_health())
            ):
                best = current
            current = current.next_node

        return best.saalmon
    
    def remove(self, index: int) -> Saalmon:
        """
        Removes and returns the Saalmon at the given index, if valid, and maintains 
        the relative order of remaining Saalmon in the collection. If the given index is 
        invalid, raises an IndexError().

        param:
        - index: The position of the Saalmon to remove in the collection.
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index is out of range")
        
        current_node = self.sentinel.next_node
        for i in range(index):
            current_node = current_node.next_node
        
        saalmon_to_remove = current_node.saalmon
        # Adjust links 
        current_node.prev_node.next_node = current_node.next_node
        current_node.next_node.prev_node = current_node.prev_node
        self.size -= 1
        return saalmon_to_remove
    
    def release_species(self, species: str) -> bool:
        """
        Removes the Saalmon of the given species species from the LinkedSaalmonagerie, maintaining the 
        relative order of remaining Saalmon in the collection, and returning True. If the given species 
        does not exist in the LinkedSaalmonagerie, do nothing, and return False.

        param:
        - species: The species of Saalmon to be removed from the collection.
        """
        node_to_remove = self._find_species_node(species)
        if node_to_remove is None:
            return False
        
        # Adjust links
        node_to_remove.prev_node.next_node = node_to_remove.next_node
        node_to_remove.next_node.prev_node = node_to_remove.prev_node
        self.size -= 1
        return True
    
    def get_species_index(self, species: str) -> int:
        """
        Returns the index of a Saalmon with the given species in the collection, 
        or -1 if that type is not found within.

        param:
        - species: The species name of the Saalmon to locate within the collection.
        """
        current_node = self.sentinel.next_node
        index = 0

        while current_node != self.sentinel:
            if current_node.saalmon.get_species() == species:
                return index
            current_node = current_node.next_node
            index += 1

        return -1 
    
    def contains_species(self, species: str) -> bool:
        """
        Returns true if the given species is found within the LinkedSaalmonagerie's collection.

        param: 
        - species: The species name of the Saalmon to check for in the collection.
        """
        return self._find_species_node(species) is not None
    
    def trade(self, other: Saalmonagerie) -> None:
        """
        Swaps the contents of the calling LinkedSaalmonagerie and the other specified. Does nothing 
        if other is not a LinkedSaalmonagerie.

        param:
        - other: The LinkedSaalmonagerie instance to trade contents with.
        """
        if not isinstance(other, LinkedSaalmonagerie):
            return

        self.sentinel, other.sentinel = other.sentinel, self.sentinel
        self.size, other.size = other.size, self.size
    
    def rearrange(self, species: str, index: int) -> None:
        """
        Moves the Saalmon of the given species from its current position in the LinkedSaalmonagerie to the one 
        specified by the index, shifting any existing Saalmon around the requested index so that the relative 
        indexing is preserved. If no such Saalmon is found, does nothing. The given index is defined on the 
        range [0, size-1], inclusive.

        param:
        - species: The species of the Saalmon to rearrange within the collection.
        - index: The new position to move the specified Saalmon species to.
        """
        if index < 0 or index >= self.size:
            raise IndexError("index is out of range")

        node_to_move = self._find_species_node(species)
        if node_to_move is None:
            return

        node_to_move.prev_node.next_node = node_to_move.next_node
        node_to_move.next_node.prev_node = node_to_move.prev_node

        current_node = self.sentinel.next_node
        for i in range(index):
            current_node = current_node.next_node

        node_to_move.next_node = current_node
        node_to_move.prev_node = current_node.prev_node
        current_node.prev_node.next_node = node_to_move
        current_node.prev_node = node_to_move
    
    def clone(self) -> 'LinkedSaalmonagerie':
        """
        Returns a deep copy of this LinkedSaalmonagerie with a new Sentinel node and deep-cloned Saalmon instances.
        """
        clone_list = LinkedSaalmonagerie()
        current_node = self.sentinel.next_node

        while current_node != self.sentinel:
            cloned_saalmon = current_node.saalmon.clone()
            clone_list.collect(cloned_saalmon)
            current_node = current_node.next_node

        return clone_list
    
    # Overridden Python methods
    # ----------------------------------------------------------
    
    def __eq__(self, other: Any) -> bool:
        """
        Returns whether or not the given Object other is a property-equivalent LinkedSaalmonagerie to this one, 
        which we define as meaning that it contains == (i.e., property-equivalence) Saalmon in the same order in 
        the collection as this one. Returns False in all other cases.

        param:
        - other: The object to compare for equivalency with this LinkedSaalmonagerie.
        """
        if not isinstance(other, LinkedSaalmonagerie) or len(self) != len(other):
            return False
        
        self_node = self.sentinel.next_node
        other_node = other.sentinel.next_node
        while self_node != self.sentinel:
            if self_node.saalmon != other_node.saalmon:
                return False
            self_node = self_node.next_node
            other_node = other_node.next_node

        return True
    
    def __len__(self) -> int:
        """
        Returns the current size of the LinkedSaalmonagerie (i.e., the number of Saalmon in the collection)
        """
        return self.size
    
    def __iter__(self) -> '_LinkedSaalmonagerieIterator':
        """
        Returns a new _LinkedSaalmonagerieIterator for this LinkedSaalmonagerie.
        """
        return self._LinkedSaalmonagerieIterator(self)
    
    def __str__(self) -> str:
        '''
        Returns a string representing this LinkedSaalmonagerie of the format
        [ <Type> [<Level>]: <CurrentHealth> HP, <Type2> [<Level2>]: <CurrentHealth2> HP ]
        '''
        saalmon_descriptions: list[str] = []

        node = self.sentinel.next_node
        while node is not self.sentinel:
            saalmon_descriptions += node.saalmon.__str__()
        return f'[ {", ".join(saalmon_descriptions)} ]'
    
    # Private helper methods
    # ----------------------------------------------------------

    def _find_species_node(self, species: str) -> Optional['Node']: # 'Node': forward declaration to resolve NameError
        """
        Returns the node containing a Saalmmon of the specified species, or None if not found

        param:
        - species: The species name of the Saalmon to locate within the collection.
        """
        current_node = self.sentinel.next_node
        while current_node != self.sentinel:
            if current_node.saalmon.get_species() == species:
                return current_node
            current_node = current_node.next_node
        return None

    # Private Iterator class
    # ----------------------------------------------------------

    class _LinkedSaalmonagerieIterator(Iterator):

        def __init__(self, host: 'LinkedSaalmonagerie') -> None:
            self.sentinel = host.sentinel
            self.node = self.sentinel.next_node

        def __iter__(self) -> Iterator[Saalmon]:
            return self
        
        def __next__(self) -> Saalmon:
            """
            Advances to the next Node and returns the Saalmon stored in the current node.
            Raises StopIteration if the sentinel node is reached.
            """
            if self.node == self.sentinel:
                raise StopIteration

            saalmon = self.node.saalmon
            self.node = self.node.next_node
            return saalmon

@dataclass
class Node:
    next_node: 'Node'
    prev_node: 'Node'
    saalmon: Saalmon

    def __init__(self, saalmon: Saalmon) -> None:
        self.next_node = self
        self.prev_node = self
        self.saalmon = saalmon

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.saalmon == other.saalmon
    
    # [!] You may, but need not, add any methods to Node

@dataclass
class Sentinel(Node):
    next_node: 'Node'
    prev_node: 'Node'

    def __init__(self) -> None:
        self.next_node = self
        self.prev_node = self

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self))
    
    # [!] Leave this class as-is, you may not modify!