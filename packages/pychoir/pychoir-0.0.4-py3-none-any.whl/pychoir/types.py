from typing import Any, Type

from pychoir.core import Matcher


class IsInstance(Matcher):
    def __init__(self, type_: Type[Any]):
        super().__init__()
        self.type = type_

    def _matches(self, other: Any) -> bool:
        return isinstance(other, self.type)

    def _description(self) -> str:
        return self.type.__name__


OfType = IsInstance


class ConvertsTo(Matcher):
    def __init__(self, type_: Type[Any]):
        super().__init__()
        self.type = type_

    def _matches(self, other: Any) -> bool:
        try:
            converted = self.type(other)
        except:  # noqa: E722
            return False
        return isinstance(converted, self.type)

    def _description(self) -> str:
        return self.type.__name__
