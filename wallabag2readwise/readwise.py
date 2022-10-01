import requests
from wallabag2readwise.logging import logger
from typing import Generator
from datetime import datetime
from typing import Optional

from wallabag2readwise.models import Annotation, Entry, ReadwiseBook, ReadwiseHighlight


class ReadwiseConnector:
    def __init__(
        self,
        token: str,
    ):
        self.token = token
        self.url = 'https://readwise.io/api/v2'

    @property
    def _session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                'Accept': 'application/json',
                'Authorization': f'Token {self.token}',
            }
        )
        return session

    def get(self, endpoint: str, params: dict = {}) -> requests.Response:
        url = self.url + endpoint
        logger.debug(f'Getting "{url}" with params: {params}')
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: dict = {}) -> requests.Response:
        url = self.url + endpoint
        logger.debug(f'Posting "{url}" with data: {data}')
        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response

    def get_books(self, category: str) -> Generator[ReadwiseBook, None, None]:
        page = 1
        page_size = 1000
        while True:
            data = self.get(
                '/books',
                {'page': page, 'page_size': page_size, 'category': category},
            ).json()
            for book in data['results']:
                yield ReadwiseBook(
                    id=book['id'], title=book['title'], source=book['source']
                )

            if not data['next']:
                break
            page += 1

    def get_book_highlights(
        self, book_id: str
    ) -> Generator[ReadwiseHighlight, None, None]:
        page = 1
        page_size = 1000
        while True:
            data = self.get(
                '/highlights',
                {'page': page, 'page_size': page_size, 'book_id': book_id},
            ).json()
            for highlight in data['results']:
                yield ReadwiseHighlight(
                    highlight['id'], highlight['text'], highlight['tags']
                )

            if not data['next']:
                break
            page += 1

    def create_highlight(
        self,
        text: str,
        title: str,
        author: Optional[str] = None,
        highlighted_at: Optional[datetime] = None,
        source_url: Optional[str] = None,
        category: str = 'articles',
        note: Optional[str] = None,
    ):
        payload = {'text': text, 'title': title, 'category': category}
        if author:
            payload['author'] = author
        if highlighted_at:
            payload['highlighted_at'] = highlighted_at.isoformat()
        if source_url:
            payload['source_url'] = source_url
        if note:
            payload['note'] = note

        self.post('/highlights/', {'highlights': [payload]})


def new_highlights(
    readwise: ReadwiseConnector, entry: Entry, annotations: list[Annotation]
):
    for item in annotations:
        readwise.create_highlight(
            item.quote,
            entry.title,
            highlighted_at=item.created_at,
            source_url=entry.url,
            note=item.text,
            category='articles',
        )
