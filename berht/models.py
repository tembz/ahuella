from dataclasses import dataclass
from typing import List, Optional

@dataclass
class StickersObject:
    count: int
    names: list
    price_vote: int

@dataclass
class StickersGroups:
    animation: StickersObject
    free: StickersObject
    stickers: StickersObject
    styles: StickersObject
    unique: StickersObject

@dataclass
class Stickers:
    all_price: int
    all_price_vote: int
    count: int
    items: StickersGroups

@dataclass
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


@dataclass
class Captcha:
    object: str

@dataclass
class GroupItems:
    group_id: int
    names: List[str]
    gdesc: Optional[str] = None

@dataclass
class Groups:
    items: List[GroupItems]
    count: int