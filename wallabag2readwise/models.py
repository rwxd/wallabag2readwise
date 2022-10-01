from dataclasses import dataclass
from datetime import datetime


@dataclass
class Entry:
    id: str
    title: str
    content: str
    url: str
    hashed_url: str
    annotations: list


@dataclass
class Annotation:
    id: str
    text: str
    quote: str
    ranges: list
    created_at: datetime


@dataclass
class ReadwiseBook:
    id: str
    title: str
    source: str


@dataclass
class ReadwiseHighlight:
    id: str
    text: str
    tags: list
