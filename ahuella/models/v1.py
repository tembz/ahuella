import dataclasses

@dataclasses.dataclass
class StickersStickers:
    count: int
    items: list[str]

@dataclasses.dataclass
class Stickers:
    price: int
    price_vote: int
    stickers: StickersStickers
    styles: StickersStickers


@dataclasses.dataclass
class Sticker:
    author: str
    author_id: int
    count: int
    desciption: str
    is_anim: bool
    is_new: bool
    items: dict[list[str]]
    price: int
    style_orig: bool
    title: str
    unique: bool


@dataclasses.dataclass
class GroupItems:
    group_id: int
    names: list[str]
    gdesc: str | None = None

@dataclasses.dataclass
class Groups:
    count: int
    items: list[GroupItems]


@dataclasses.dataclass
class Captcha:
    object: str