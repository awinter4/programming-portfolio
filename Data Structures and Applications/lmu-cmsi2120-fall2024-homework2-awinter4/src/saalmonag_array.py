'''
CMSI 2120 - Homework 2
Author: Andrew Winter

Original Java assignment written by Andrew Forney @forns,
converted to Python by Natalie Lau @nklau.
'''
from saalmon_array import SaalmonArray
from saalmon import Saalmon
from saalmonagerie import Saalmonagerie
from typing import Any, Optional

class SaalmonagArray(Saalmonagerie):
    '''
    Collections of Saalmon ready to fight in the arena!
    '''

    # Constants
    # ----------------------------------------------------------
    # [!] DO NOT change this START_SIZE for your collection, and
    # your collection *must* be initialized to this size
    START_SIZE = 4

    # Fields
    # ----------------------------------------------------------
    collection: SaalmonArray
    _size: int

    # Constructor
    # ----------------------------------------------------------
    def __init__(self) -> None:
        self.collection = SaalmonArray(self.START_SIZE)
        self._size = 0

    # Methods
    # ----------------------------------------------------------
    def empty(self) -> bool:
        """
        Returns true if the SaalmonagArray has no Saalmon inside, false otherwise.
        param:
        - self: Current instance of the SaalmonagArray object.
        """
        return self._size == 0
    
    def size(self) -> int:
        """
        Returns the current size of the SaalmonagArray 
        param:
        - self: Current instance of the SaalmonagArray object.        
        """
        return self._size
    
    def collect(self, to_add: Saalmon) -> bool:
        """
        Collection method adds a reference to the given Saalmon to the SaalmonagArray's collection.
        If Saalmon is the same species as a Saalmon already in the SaalmonagArray, keep the 
        Saalmon with the higher level. If both are the same level, the Saalmon already stored within is kept.
        param:
        - self: Current instance of the SaalmonagArray object.
        - to_add: Saalmon object that the method attempts to add.
        """
        index = self.get_species_index(to_add.get_species())
        if index != -1:
            current = self.collection[index]
            # Type check
            if isinstance(current, Saalmon):
                if current.get_level() >= to_add.get_level():
                    return False
                self.collection[index] = to_add
                return True
        
        # Check and grow
        if self._size >= len(self.collection):
            self._check_and_grow()

        # If Saalmon to add is unique, add to collection and increment collection size
        self.collection[self._size] = to_add
        self._size += 1
        return True

    def get(self, index: int) -> Saalmon:
        """
        Returns the Saalmon at the requested index in the collection, if valid.
        If the given index is invalid, raise IndexError().
        param:
        - self: Current instance of the SaalmonagArray object.
        - index: Position of the Saalmon to retrieve.
        """
        if index < 0 or index >= self._size:
            raise IndexError(f'Index {index} is out of range')
        
        saalmon = self.collection[index]
        if saalmon is None:
            raise ValueError(f'No Saalmon found at index {index}')
        return saalmon
    
    def get_mvp(self) -> Optional[Saalmon]:
        """
        Returns the "best" Saalmon currently in the collection, or None if the collection is empty.
        Here, "best" is defined as:
        - The highest level Saalmon in the collection, with ties broken by:
        - The highest health of those with the max level, with ties broken by:
        - The earlier index of those tied in the collection.
        param:
        - self: Current instance of the SaalmonagArray object.
        """    
        if self._size == 0:
            return None
        
        mvp = self.collection[0]

        for i in range(1, self._size):
            current = self.collection[i]
    
            # Type check 
            if current is not None and mvp is not None:
        
                if current.get_level() > mvp.get_level():
                    mvp = current

                elif current.get_level() == mvp.get_level():
                    if current.get_health() > mvp.get_health():
                        mvp = current

        return mvp
    
    def remove(self, index: int) -> Saalmon:
        """
        Removes and returns the Saalmon at the given index, if valid, and maintains 
        the relative order of remaining Saalmon in the collection. If the given index 
        is invalid, raise an IndexError().
        param:
        - self: Current instance of the SaalmonagArray object.
        - index: Position of the Saalmon to retrieve.
        """
        if index < 0 or index >= self._size:
            raise IndexError(f'Index {index} is out of range')
        
        removed_saalmon = self.collection[index]

        if removed_saalmon is None:
            raise ValueError(f'No Saalmon found at index {index}')

        for i in range(index, self._size - 1):
            self.collection[i] = self.collection[i + 1]

        self.collection[self._size - 1] = None
        self._size -= 1

        return removed_saalmon

    def release_species(self, species: str) -> bool:
        """
        Removes the Saalmon of the given species species from the SaalmonagArray, 
        maintaining the relative order of remaining Saalmon in the collection, and returning true.
        If the given species does not exist in the SaalmonagArray, returns false.
        param:
        - self: Current instance of the SaalmonagArray object.
        - species: Species name of the Saalmon to be removed.
        """
        species_to_find = False
        i = 0

        while i < self._size:
            saalmon = self.collection[i]
            # Check that saalmon is not None before calling get_species()
            if saalmon is not None and saalmon.get_species() == species:
                self.remove(i)
                species_to_find = True
            else:
                i += 1
        return species_to_find
    
    def get_species_index(self, species: str) -> int:
        """
        Returns the index of a Saalmon with the given species in the collection, or -1 if that type is not found within.
        param:
        - self: Current instance of the SaalmonagArray object.
        - species: Species name of the Saalmon to find. 
        """
        for i in range(self._size):
            saalmon = self.collection[i]
            # Check that saalmon is not None before calling get_species()
            if saalmon is not None and saalmon.get_species() == species:
                return i

        return -1
    
    def contains_species(self, species: str) -> bool:
        """
        Returns true if the given species is found within the SaalmonagArray's collection.
        param:
        - self: Current instance of the SaalmonagArray object.
        - species: Species name of the Saalmon to check for in the collection.
        """
        return self.get_species_index(species) != -1
    
    def trade(self, other: Saalmonagerie) -> None:
        """
        Swaps the contents of the calling SaalmonagArray and the other specified. 
        Does nothing if other is not a SaalmonagArray.
        param: 
        - self: Current instance of the SaalmonagArray object.
        - other: Instance of of another Saalmonagerie object to trade with.
        """
        if not isinstance(other, SaalmonagArray):
            return 

        # Swap 
        self.collection, other.collection = other.collection, self.collection
        self._size, other._size = other._size, self._size
            
    def rearrange(self, species: str, index: int) -> None:
        """
        Moves the Saalmon of the given species from its current position in the SaalmonagArray 
        to the one specified by the index, shifting any existing Saalmon around the requested 
        index so that the relative indexing is preserved. If no such Saalmon is found, does nothing.
        param:
        - self: Current instance of the SaalmonagArray object.
        - species: Species name of the Saalmon to move.
        - index: Position of which the Saalmon is to move to. 
        """
        self._validate_index(index)
        species_index = self.get_species_index(species)
        if species_index == -1 or species_index == index:
            return
        
        saalmon_to_move = self.collection[species_index]
        self._shift_left(species_index)
        self._shift_right(index)
        self.collection[index] = saalmon_to_move

    def clone(self) -> 'SaalmonagArray':
        """
        Returns a deep copy of this SaalmonagArray in the same collection order, 
        but with new (cloned) instances of each stored Saalmon and it's own collection.
        param:
        - self: Current instance of the SaalmonagArray object.
        """
        clone = SaalmonagArray()

        for i in range(self._size):
            saalmon_to_clone = self.collection[i]

            # Type check 
            if isinstance(saalmon_to_clone, Saalmon):
                # Clone 
                cloned_saalmon = saalmon_to_clone.clone()
                clone.collect(cloned_saalmon)

        return clone
    
    # Overridden Python methods
    # ----------------------------------------------------------
    
    def __eq__(self, other: Any) -> bool:
        """
        Returns whether or not the given Object other is a property-equivalent SaalmonagArray to this one, 
        which we define as meaning that it contains equal (i.e., property-equivalence) Saalmon in the same 
        order in the collection as this one. Returns false in all other cases.
        param:
        - self: Current instance of the SaalmonagArray object.
        - other: Any object to compare with the current SaalmonagArray.
        """
        if not isinstance(other, SaalmonagArray) or self._size != other.size():
            return False
        for i in range(self._size):
            if self.collection[i] != other.get(i):
                return False 
        return True

    def __str__(self) -> str:
        '''
        Returns a string representing this SaalmonagArray of the format
        [ <Type> [<Level>]: <CurrentHealth> HP, <Type2> [<Level2>]: <CurrentHealth2> HP ]
        '''
        return f'[ {", ".join([saalmon.__str__() for saalmon in self.collection])} ]'
    
    # Private helper methods
    # ----------------------------------------------------------

    def _check_and_grow(self) -> None:
        """
        Doubles the size of the collection array.
        """
        new_collection = SaalmonArray(len(self.collection) * 2)
        for i in range(self._size):
            new_collection[i] = self.collection[i]
        self.collection = new_collection

    def _validate_index(self, index: int) -> None:
        """
        Validates that index is in range.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index is out of range.")
        
    def _shift_left(self, start_index: int) -> None:
        """
        Shifts elements to the left from the specified start index.
        """
        for i in range(start_index, self._size -1):
            self.collection[i] = self.collection[i + 1]
        self.collection[self._size - 1] = None

    def _shift_right(self, end_index: int) -> None:
        """
        Shifts elements to the right to accomodate a new head.
        """
        if self._size >= len(self.collection): 
            self._check_and_grow()

        for i in range(self._size, end_index, -1):
            self.collection[i] = self.collection[i - 1]

# =====================================================
# >>> [SS] Summary
# Coding style was generally good, but there's
# a few areas for improvement, primarily in
# preventing repetive code with helper
# methods and using methods you've
# already written.
# 
# Make sure to write some additional
# tests next time around to confirm the complete
# functionality of your code!
# -----------------------------------------------------
# >>> [SS] Style Checklist
# [ ] Variables and helper methods used well
# [X] Proper and consistent indentation and spacing
# [X] Proper doc comments provided for ALL methods
# [X] Logic is adequatley simplified
# [ ] Code repetition is kept to a minimum 
# -----------------------------------------------------
# Correctness:          76 / 100 (-2 / missed unit test)
# Static Typing:        -0
# Style Penalty:        -3
# Total:                73 / 100
# =====================================================