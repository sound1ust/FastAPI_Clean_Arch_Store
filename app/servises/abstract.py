from abc import ABC, abstractmethod
from typing import Union, List

from app.config import *
from app.models.products import Product
from app.repositories.exceptions import (
    RepositoryNotSettedException,
    RepositoryNotFoundException, AppNotSettedException, AppNotFoundException,
)


class AbstractService(ABC):
    def __init__(self, **kwargs):
        self.config = kwargs
        self.repo_dict = self.__get_repo_dict()
        self.app_name = None

    @abstractmethod
    def create(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @abstractmethod
    def list(self, *args, **kwargs) -> Union[List[Product], None]:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @staticmethod
    def __get_repo_dict():
        repo_name = DATABASE_SETTINGS.get("REPOSITORY")
        if not repo_name:
            raise RepositoryNotSettedException

        repo_dict = REPOSITORIES.get(repo_name)
        if not repo_dict:
            raise RepositoryNotFoundException(repo_name)

        return repo_dict

    def get_repo(self):
        if not self.app_name:
            raise AppNotSettedException

        repo = self.repo_dict.get(self.app_name)
        if not repo:
            raise AppNotFoundException(self.app_name)

        return repo(self.config)
