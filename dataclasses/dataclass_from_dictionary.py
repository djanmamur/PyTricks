from typing import Any, ClassVar, Dict, List, NoReturn
from dataclasses import dataclass, fields


def dataclass_from_dict(data_class: ClassVar, object_dict: Dict = None) -> ClassVar:
    if object_dict is None:
        object_dict = dict()

    try:
        new_dataclass_fields: Dict = {
            field.name: field.type for field in fields(data_class)
        }
        new_dataclass: ClassVar = data_class(
            **{
                f: dataclass_from_dict(new_dataclass_fields[f], object_dict[f])
                for f in object_dict
            }
        )

        return new_dataclass
    except Exception:
        pass
    return object_dict


def print_list(lst: List[Any], end: str = "\n") -> NoReturn:
    for item in lst:
        print(item, end=end)


@dataclass
class ASCIIMap:
    char: str
    ascii_val: int

    def __repr__(self):
        return f"{self.char} -- {self.ascii_val}"


lst_channels: List[ASCIIMap] = [
    dataclass_from_dict(ASCIIMap, {"char": chr(index) * 3, "ascii_val": index})
    for index in range(65, 91)
]

print_list(lst_channels)
