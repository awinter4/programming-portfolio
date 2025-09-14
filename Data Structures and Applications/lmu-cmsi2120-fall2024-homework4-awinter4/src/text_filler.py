from abc import *
from typing import Optional


class TextFiller(ABC):
    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def is_empty(self) -> bool: ...

    @abstractmethod
    def add(self, word: str, priority: int) -> None: ...

    @abstractmethod
    def contains(self, query: str) -> bool: ...

    @abstractmethod
    def text_fill(self, query: str) -> Optional[str]: ...

    @abstractmethod
    def get_sorted_list(self) -> list[str]: ...

    def text_fill_premium(self, query: str) -> Optional[str]:
        return ''
    