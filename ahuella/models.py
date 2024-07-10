import dataclasses
from typing import Any, Dict, List

@dataclasses.dataclass
class StickersObject:
    count: int
    names: list
    price_vote: int

@dataclasses.dataclass
class StickersGroups:
    animation: StickersObject
    free: StickersObject
    stickers: StickersObject
    styles: StickersObject
    unique: StickersObject

@dataclasses.dataclass
class Stickers:
    all_price: int
    all_price_vote: int
    count: int
    items: StickersGroups

@dataclasses.dataclass
class Sticker:
    author: str
    author_id: int
    count: int
    description: str
    is_anim: bool
    is_new: bool
    items: dict
    price: int
    style_orig: bool
    title: str
    unique: bool


@dataclasses.dataclass
class Captcha:
    object: str

@dataclasses.dataclass
class GroupItems:
    group_id: int
    names: List[str]
    gdesc: str | None = None

@dataclasses.dataclass
class Groups:
    items: List[GroupItems]
    count: int

def from_dict(data_class, data: Dict[str, Any]):
    fieldtypes = {f.name: f.type for f in dataclasses.fields(data_class)}
    return data_class(**{f: from_dict(fieldtypes[f], data[f]) if dataclasses.is_dataclass(fieldtypes[f]) else data[f] for f in data})