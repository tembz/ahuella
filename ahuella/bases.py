
class Stickers:
    count = int
    names = str | list
    price_vote = int

class StickersItems:
    animation = Stickers
    free = Stickers
    stickers = Stickers
    styles = Stickers
    unique = Stickers

class StickersObject:
    all_price = int
    all_price_vote = int
    count = int
    items = StickersItems

class FinalGetStickers:
    object = StickersObject
    ok = bool

class StickerObject:
    author = str
    author_id = int
    count = int
    description = str
    is_anim = bool
    is_new = bool
    items = dict | str
    price = int
    style_orig = bool
    title = str
    unique = bool

class FinalGetSticker:
    object = StickerObject
    ok = bool

class FinalCaptcha:
    object = str
    ok = bool