import html
import re

from pydantic import BaseModel


CLEANR = re.compile('<.*?>|\r')


class HashableBaseModel(BaseModel):

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


def clear_from_tags(raw_text: str) -> str:
    return html.unescape(re.sub('\n+', '\n', re.sub(CLEANR, '', raw_text)))


def display_name_from_obj(obj: dict) -> str:
    return obj['display_name']
