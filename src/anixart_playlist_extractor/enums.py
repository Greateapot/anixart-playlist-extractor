import enum


class Quality(enum.StrEnum):
    q360 = "360"
    q480 = "480"
    q720 = "720"


__all__ = (Quality,)
