from wallabag2readwise.models import Annotation
from wallabag2readwise.readwise import ReadwiseConnector, new_highlights
from wallabag2readwise.wallabag import WallabagConnector
from datetime import datetime
from wallabag2readwise.logging import logger
from wallabag2readwise.output import console


def push_annotations(wallabag: WallabagConnector, readwise: ReadwiseConnector):
    readwise_articles = list(readwise.get_books('articles')) + list(
        readwise.get_books('books')
    )

    for entry in wallabag.get_entries():
        if len(entry.annotations) > 0:
            annotations = [
                Annotation(
                    id=i['id'],
                    text=i['text'],
                    quote=i['quote'],
                    created_at=datetime.strptime(
                        i['created_at'], '%Y-%m-%dT%H:%M:%S+%f'
                    ),
                    ranges=i['ranges'],
                )
                for i in entry.annotations
            ]
            logger.info(f'Found {len(annotations)} for "{entry.title}"')
            for article in readwise_articles:
                if article.title == entry.title:
                    highlights = list(readwise.get_book_highlights(article.id))
                    console.print(
                        f'=> Found {len(highlights)} wallabag highlights for "{entry.title}"'
                    )
                    for annotation in annotations:
                        if annotation.quote not in [i.text for i in highlights]:
                            new_highlights(readwise, entry, [annotation])
                        else:
                            logger.debug('Annotation already present')

                    break
            else:
                logger.info(f'Entry "{entry.title}" not present in Readwise')
                console.print(f'==> Adding article "{entry.title}" to Readwise')
                new_highlights(readwise, entry, annotations)
