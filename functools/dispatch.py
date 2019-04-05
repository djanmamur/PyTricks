import json
from datetime import datetime
from functools import singledispatch
from typing import Dict, List, Iterable

from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


@singledispatch
def json_serialize(value: Iterable):
    msg: str = f"Serialize overload for {type(value)} instances is not implemented yet"
    raise NotImplementedError(msg)


@json_serialize.register(dict)
def json_dict_serialize(value: Dict) -> Dict:
    serialize = JSONEncoder().encode(value)
    serialized_dict: Dict = json.dumps(json.loads(serialize))

    return serialized_dict


@json_serialize.register(list)
def json_lst_serialize(value: List[Dict]) -> List[Dict]:
    return [json_dict_serialize(v) for v in value]


test_dict: List[Dict] = [
    {f"{chr(key)}" * 3: ObjectId(), "time": datetime.utcnow()} for key in range(65, 93)
]

json_dict_serialize(test_dict[0])
json_lst_serialize(test_dict)
