from saalmon import Saalmon
from abc import *
from typing import Any, Optional

class Saalmonagerie(ABC):
    @abstractmethod
    def empty(self) -> bool:
        ...

    @abstractmethod
    def size(self) -> int:
        ...

    @abstractmethod
    def collect(self, to_add: Saalmon) -> bool:
        ...

    @abstractmethod
    def get(self, index: int) -> Saalmon:
        ...

    @abstractmethod
    def get_mvp(self) -> Optional[Saalmon]:
        ...

    @abstractmethod
    def remove(self, index: int) -> Saalmon:
        ...

    @abstractmethod
    def release_species(self, species: str) -> bool:
        ...

    @abstractmethod
    def get_species_index(self, species: str) -> int:
        ...

    @abstractmethod
    def contains_species(self, species: str) -> bool:
        ...

    @abstractmethod
    def trade(self, other: 'Saalmonagerie') -> None:
        ...

    @abstractmethod
    def rearrange(self, species: str, index: int) -> None:
        ...

    @abstractmethod
    def clone(self) -> 'Saalmonagerie':
        ...

    @abstractmethod
    def __eq__(self, value: Any) -> bool:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...