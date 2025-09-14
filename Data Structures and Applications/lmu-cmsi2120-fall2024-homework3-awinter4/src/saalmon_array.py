from saalmon import Saalmon
from typing import Iterator, overload

class SaalmonArray:
    elements: list[Saalmon | None]
    length: int

    def __init__(self, initializer: list[Saalmon | None] | int) -> None:
        if isinstance(initializer, list):
            self.elements = []
            for element in initializer:
                if isinstance(element, Saalmon) or element is None:
                    self.elements.append(element)
                else:
                    raise ValueError(
                        f'SaalmonArray can only contain Saalmon; received {type(element)} instead'
                    )
        elif isinstance(initializer, int):
            self.elements = [None] * initializer
        else:
            raise ValueError(
                f'Initializer must be a list of Saalmon or a number; received {type(initializer)} instead'
            )
        
        self.length = len(self.elements)
        
    def __str__(self) -> str:
        return str(self.elements)
    
    # [!] These methods are here specifically for mypy's static type-checking requirements;
    # do not touch any methods marked @overload!
    @overload
    def __getitem__(self, key: int) -> Saalmon | None:
        ...

    @overload
    def __getitem__(self, key: slice) -> 'SaalmonArray':
        ...
    
    def __getitem__(self, key: int | slice) -> 'Saalmon | None | SaalmonArray':
        if isinstance(key, int):
            if key < 0 or key >= self.length:
                raise IndexError(
                    f'Index {key} out of bounds for array of length {self.length}'
                )
            return self.elements[key]
        else:
            start, stop, step = key.start or 0, key.stop or self.length, key.step or 1
            if stop > self.length:
                raise IndexError(
                    f'Index {stop} out of bounds for array of length {self.length}'
                )
            
            return SaalmonArray(self.elements[start:stop:step])
        
    def __setitem__(self, key: int, new_value: Saalmon | None) -> None:
        if key < 0 or key > self.length:
            raise IndexError(
                f'Index {key} out of bounds for array of length {self.length}'
            )
        
        if not isinstance(new_value, Saalmon) and new_value is not None:
            raise ValueError(
                f'SaalmonArray can only contain Saalmon; received {type(new_value)} instead'
            )
        
        self.elements[key] = new_value

    def __len__(self) -> int:
        return self.length
    
    def __iter__(self) -> Iterator[Saalmon | None]:
        return iter(self.elements)