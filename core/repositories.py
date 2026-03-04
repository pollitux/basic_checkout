"""
core/repositories.py

Base repository interface following ISP (Interface Segregation Principle).
Each repository interface defines only the methods its clients need.
"""
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from django.db.models import Model

T = TypeVar("T", bound=Model)


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository.
    Defines the contract for all concrete repositories (DIP).
    """

    @abstractmethod
    def get_by_id(self, pk) -> Optional[T]:
        """
        Get object by id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Get all objects.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save object.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: T) -> None:
        """
        Delete object.
        """
        raise NotImplementedError
