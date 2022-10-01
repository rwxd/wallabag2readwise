import requests
from wallabag2readwise.logging import logger
from typing import Generator
from datetime import datetime

from wallabag2readwise.models import Annotation, Entry


class WallabagConnector:
    def __init__(
        self, url: str, user: str, password: str, client_id: str, client_secret: str
    ):
        self.url = url
        self.user = user
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token: str = self._get_oauth_token()

    @property
    def _session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.access_token}',
            }
        )
        return session

    def _get_oauth_token(self):
        logger.info('Getting wallabag oauth token')
        response = requests.post(
            self.url + '/oauth/v2/token',
            {
                'grant_type': 'password',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.user,
                'password': self.password,
            },
        )
        data = response.json()
        return data['access_token']

    def get(self, endpoint: str, params: dict = {}) -> requests.Response:
        url = self.url + endpoint
        logger.debug(f'Getting "{url}" with params: {params}')
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: dict = {}) -> requests.Response:
        url = self.url + endpoint
        logger.debug(f'Posting "{url}" with data: {data}')
        response = self._session.post(url, data=data)
        response.raise_for_status()
        return response

    def get_entries(self) -> Generator[Entry, None, None]:
        page = 1
        perPage = 100
        while True:
            data = self.get(
                '/api/entries.json', {'page': page, 'perPage': perPage}
            ).json()
            for entry in data['_embedded']['items']:
                yield Entry(
                    id=entry['id'],
                    title=entry['title'],
                    url=entry['url'],
                    hashed_url=entry['hashed_url'],
                    content=entry['content'],
                    annotations=entry['annotations'],
                )

            if page == data['pages']:
                break
            page += 1

    def get_annotations(self, entry_id: str) -> Generator[Annotation, None, None]:
        data = self.get(f'/api/annotations/{entry_id}.json').json()
        for item in data['rows']:
            yield Annotation(
                id=item['id'],
                text=item['text'],
                quote=item['quote'],
                created_at=datetime.strptime(item['created_at'], '%y-%m-%dT%H:%M+%S'),
                ranges=item['ranges'],
            )
