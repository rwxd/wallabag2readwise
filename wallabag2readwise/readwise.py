import requests
from wallabag2readwise.logging import logger
from typing import Generator
from datetime import datetime
from typing import Optional
from ratelimit import limits, RateLimitException, sleep_and_retry
from backoff import on_exception, expo
from time import sleep

from wallabag2readwise.models import (
    WallabagAnnotation,
    WallabagEntry,
    ReadwiseTag,
    ReadwiseBook,
    ReadwiseHighlight,
)
from wallabag2readwise.output import console


class ReadwiseRateLimitException(Exception):
    pass


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

    @on_exception(expo, RateLimitException, max_tries=8)
    @sleep_and_retry
    @limits(calls=240, period=60)
    def _request(
        self, method: str, endpoint: str, params: dict = {}, data: dict = {}
    ) -> requests.Response:
        url = self.url + endpoint
        logger.debug(f'Calling "{method}" on "{url}" with params: {params}')
        response = self._session.request(method, url, params=params, json=data)
        while response.status_code == 429:
            seconds = int(response.headers['Retry-After'])
            logger.warning(f'Rate limited by Readwise, retrying in {seconds} seconds')
            sleep(seconds)
            response = self._session.request(method, url, params=params, data=data)
        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: dict = {}) -> requests.Response:
        logger.debug(f'Getting "{endpoint}" with params: {params}')
        return self._request('GET', endpoint, params=params)

    @on_exception(expo, RateLimitException, max_tries=8)
    @sleep_and_retry
    @limits(calls=20, period=60)
    def get_with_limit_20(self, endpoint: str, params: dict = {}) -> requests.Response:
        return self.get(endpoint, params)

    def post(self, endpoint: str, data: dict = {}) -> requests.Response:
        url = self.url + endpoint
        logger.debug(f'Posting "{url}" with data: {data}')
        response = self._request('POST', endpoint, data=data)
        response.raise_for_status()
        return response

    def delete(self, endpoint: str) -> requests.Response:
        logger.debug(f'Deleting "{endpoint}"')
        return self._request('DELETE', endpoint)

    def get_books(self, category: str) -> Generator[ReadwiseBook, None, None]:
        page = 1
        page_size = 1000
        while True:
            data = self.get_with_limit_20(
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
            data = self.get_with_limit_20(
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

    def get_book_tags(self, book_id: str) -> Generator[ReadwiseTag, None, None]:
        page = 1
        page_size = 1000
        data = self.get(
            f'/books/{book_id}/tags',
            {'page': page, 'page_size': page_size, 'book_id': book_id},
        ).json()

        for tag in data:
            yield ReadwiseTag(tag['id'], tag['name'])

    def add_tag(self, book_id: str, tag: str):
        logger.debug(f'Adding tag "{tag}" to book "{book_id}"')
        payload = {'name': tag}
        self.post(f'/books/{book_id}/tags/', payload)

    def delete_tag(self, book_id: str, tag_id: str):
        logger.debug(f'Deleting tag "{tag_id}"')
        self.delete(f'/books/{book_id}/tags/{tag_id}')


def new_highlights(
    readwise: ReadwiseConnector,
    entry: WallabagEntry,
    annotations: list[WallabagAnnotation],
):
    for item in annotations:
        console.print(f'==> Adding highlight to Readwise')
        readwise.create_highlight(
            item.quote,
            entry.title,
            highlighted_at=item.created_at,
            source_url=entry.url,
            note=item.text,
            category='articles',
        )
