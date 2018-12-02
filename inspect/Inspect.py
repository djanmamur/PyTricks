from collections import OrderedDict
from inspect import Signature, Parameter
from typing import List, Dict, Tuple

from ..type.TypedValues import Descriptor


def create_signature(lst_names: List[str] = None) -> Signature:
    """
    Create Signature object for the list of arguments.
    :param lst_names: List of arguments to create a signature.
    :return: Signature object.
    """
    if lst_names is None:
        lst_names = list()
    return Signature(
        Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in lst_names
    )


class StructureMetaClass(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(cls, class_name: str, class_bases: Tuple, class_dict: Dict):
        _fields = [
            key for key, value in class_dict.items() if isinstance(value, Descriptor)
        ]
        for name in _fields:
            class_dict[name].name = name

        cls_object = super().__new__(cls, class_name, class_bases, class_dict)
        __signature = create_signature(_fields)
        setattr(cls_object, "__signature__", __signature)
        return cls_object
