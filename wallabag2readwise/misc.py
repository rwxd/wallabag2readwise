from requests import JSONDecodeError
from wallabag2readwise.models import ReadwiseBook, WallabagAnnotation
from wallabag2readwise.readwise import ReadwiseConnector, new_highlights
from wallabag2readwise.wallabag import WallabagConnector
from datetime import datetime
from wallabag2readwise.logging import logger
from wallabag2readwise.output import console
from time import sleep


def get_readwise_articles_with_retries(
    readwise: ReadwiseConnector, retries: int = 15, timeout: int = 5
) -> list[ReadwiseBook]:
    """We try to circumvent readwise JSONDecodeError with retries."""
    maximum = retries
    counter = 0
    while True:
        try:
            readwise_articles = list(readwise.get_books('articles')) + list(
                readwise.get_books('books')
            )
            return readwise_articles
        except JSONDecodeError as e:
            counter = counter + 1
            logger.error(f'Error while getting Readwise articles: \"{e}\"')
            if counter >= maximum:
                raise
            logger.error(
                f'Retrying in {timeout} seconds, {retries - counter} retries left'
            )
            sleep(timeout)


def push_annotations(wallabag: WallabagConnector, readwise: ReadwiseConnector):
    readwise_articles = get_readwise_articles_with_retries(readwise)
    for wallabag_entry in wallabag.get_entries():
        if len(wallabag_entry.annotations) > 0:
            annotations = [
                WallabagAnnotation(
                    id=i['id'],
                    text=i['text'],
                    quote=i['quote'],
                    created_at=datetime.strptime(
                        i['created_at'], '%Y-%m-%dT%H:%M:%S+%f'
                    ),
                    ranges=i['ranges'],
                )
                for i in wallabag_entry.annotations
            ]
            logger.info(f'Found {len(annotations)} for "{wallabag_entry.title}"')
            for readwise_article in readwise_articles:
                if readwise_article.title == wallabag_entry.title:
                    highlights = list(readwise.get_book_highlights(readwise_article.id))
                    console.print(
                        f'=> Found {len(highlights)} wallabag highlights for "{wallabag_entry.title}"'
                    )
                    for annotation in annotations:
                        if annotation.quote not in [i.text for i in highlights]:
                            new_highlights(readwise, wallabag_entry, [annotation])
                        else:
                            logger.debug('Annotation already present')

                    readwise_article_tags = list(
                        readwise.get_book_tags(readwise_article.id)
                    )
                    for tag in wallabag_entry.tags:
                        if tag.label not in [i.name for i in readwise_article_tags]:
                            console.print(
                                f'==> Adding tag "{tag.label}" to Readwise article'
                            )
                            readwise.add_tag(readwise_article.id, tag.label)

                    for tag in readwise_article_tags:
                        if tag.name not in [i.label for i in wallabag_entry.tags]:
                            console.print(
                                f'==> Deleting tag "{tag.name}" from Readwise article'
                            )
                            readwise.delete_tag(readwise_article.id, tag.id)

                    break
            else:
                logger.info(f'Entry "{wallabag_entry.title}" not present in Readwise')
                console.print(
                    f'==> Adding article "{wallabag_entry.title}" to Readwise'
                )
                new_highlights(readwise, wallabag_entry, annotations)
                for new_articles in get_readwise_articles_with_retries(readwise):
                    if new_articles.title == wallabag_entry.title:
                        for tag in wallabag_entry.tags:
                            console.print(
                                f'==> Adding tag "{tag.label}" to Readwise article'
                            )
                            readwise.add_tag(new_articles.id, tag.label)
                        break
