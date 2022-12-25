from dataclasses import dataclass
from datetime import datetime


@dataclass
class WallabagTag:
    id: str
    label: str
    slug: str


@dataclass
class WallabagEntry:
    id: str
    title: str
    content: str
    url: str
    hashed_url: str
    annotations: list
    tags: list[WallabagTag]


@dataclass
class WallabagAnnotation:
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
class ReadwiseTag:
    id: str
    name: str


@dataclass
class ReadwiseHighlight:
    id: str
    text: str
    tags: list
