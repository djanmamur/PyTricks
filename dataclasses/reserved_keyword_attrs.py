import keyword
from dataclasses import dataclass


@dataclass
class Reserved:
    _from: int = 0
    _and: str = ""
    _return: bool = False
    _non_reserved: str = ""

    @staticmethod
    def _verify_keyword(reserved_key: str, identifier: str = "") -> str:
        if reserved_key.startswith(identifier):
            *_, _key = reserved_key.split(identifier)
            if _key in keyword.kwlist:
                return _key
        return reserved_key

    def __iter__(self):
        for key, value in self.__dict__.items():
            _key = self._verify_keyword(key, "_")
            yield (_key, value)


p = Reserved()
dict(p)
