from typing import Any, Callable, Dict, Optional

import attr

from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Parameter:
    """ A parameter to an operation. """

    name: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        name = self.name

        dct = {
            "name": name,
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Parameter":
        name = d["name"]

        return Parameter(
            name=name,
        )
