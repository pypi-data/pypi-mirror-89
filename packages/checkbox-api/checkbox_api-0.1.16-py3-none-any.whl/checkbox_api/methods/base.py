from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict

from httpx import Response

from checkbox_api.storage.simple import SessionStorage


class HTTPMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()


class AbstractMethod(ABC):
    method: HTTPMethod = HTTPMethod.GET

    @property
    @abstractmethod
    def uri(self) -> str:
        pass

    @property
    @abstractmethod
    def query(self):
        pass

    @property
    @abstractmethod
    def payload(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def parse_response(self, storage: SessionStorage, response: Response):
        pass


class BaseMethod(AbstractMethod, ABC):
    @property
    def query(self):
        return {}

    @property
    def payload(self):
        return {}

    @property
    def headers(self):
        return {}

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.json()


class PaginationMixin:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = limit
        self.offset = offset

    @property
    def query(self):
        query = {}
        if self.limit is not None:
            query["limit"] = self.limit
        if self.offset is not None:
            query["offset"] = self.offset
        return query

    def shift_next_page(self):
        self.offset += self.limit
        return self

    def shift_previous_page(self):
        self.offset -= self.limit
        return self

    def set_page(self, page: int):
        self.offset = self.limit * page

    def resolve_pagination(self, paginated_result: Dict[str, Any]):
        meta = paginated_result["meta"]
        self.offset = meta["offset"]
        self.limit = meta["limit"]
        return self

    @property
    def page(self):
        return self.offset // self.limit
