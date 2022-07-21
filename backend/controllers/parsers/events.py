import datetime
import logging
import re
from datetime import datetime, date
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from api.schemas.event import ImportEvent
from celery_worker.celery_conf import celery as celery_app
from controllers.parsers.base import Parser
from database import Source, Event
from database.engine import Session

logger = logging.getLogger(__name__)

MONTHS = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'май': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}


def find_organizer(tag):
    return tag.name == 'p' and 'организатор' in tag.text.lower()


def get_organizer(article):
    organizer_text = article.find(find_organizer)
    if organizer_text:
        organizer = re.findall(r'Организаторы?: ([^\.]*)', organizer_text.text)[
            0]
        return organizer


# ссылка на сайт конкурса
def find_site_url(tag):
    return tag.name == 'p' and 'сайт конкурса:' in tag.text.lower()


def get_url(article):
    url_text = article.find(find_site_url)
    if url_text:
        url_text = url_text.text
        url = url_text[url_text.index('http'):]
        return url


def find_deadline_contest(tag):
    return tag.name == 'p' and 'дедлайн' in tag.text.lower()


def get_deadline(article):
    current_year = date.today().year
    deadline_text = article.find(find_deadline_contest)
    if deadline_text:
        deadline_text = deadline_text.text.lower()
        deadline_text = \
            re.findall(r"дедлайн (?:конкурса)?([^.]+)", deadline_text)[0]
        lbrace = deadline_text.find('(')
        if lbrace > -1:
            deadline_text = deadline_text[:lbrace]
        deadline = deadline_text.strip().split()
        day = int(deadline[0])
        month = MONTHS[deadline[1]]
        year = current_year if len(deadline) < 3 else int(deadline[2])

        deadline_datetime = datetime(day=day, month=month, year=year, hour=0,
                                     minute=0)
        return deadline_datetime


class VseKonkursyParser(Parser):
    events: List[ImportEvent]

    def __init__(self, source_url: str):
        self.urls = []
        self.events = []
        self.source_url = source_url
        self.source_id = 1

    def parse_last_contest_urls(self):
        r = requests.get(self.source_url)
        if r.ok:
            soup = BeautifulSoup(r.text, "html.parser")
            for article in soup.find_all('article'):
                self.urls.append(article.find('a')['href'])

    def parse_data(self):
        self.parse_last_contest_urls()
        for url in self.urls:
            self.events.append(self.parse_contest(contest_url=url))

    def parse_contest(self, contest_url):
        r = requests.get(contest_url)
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.find('article')
        title = article.find('h1', class_='title entry-title').text
        published_date = article.find('time', class_='published')['datetime']
        url = get_url(article)
        deadline = get_deadline(article)
        organizer = get_organizer(article)

        return ImportEvent(
            name=title,
            source_url=contest_url,
            url=url,
            published_date=published_date,
            deadline_date=deadline,
            comment=organizer,
            source_id=self.source_id,
        )

    def save_data(self, session: Session):
        for event in self.events:
            url = event.url
            if not session.query(Event).filter_by(url=url).first():
                session.add(Event(**event.dict()))
        session.commit()


@celery_app.task(bind=True, name='parse_contests', track_started=True)
def make_parse(self, source_id: int):
    session = Session()
    source: Optional[Source] = session.query(Source).filter_by(
        id=source_id,
        enable=True,
    ).first()
    if source is None:
        logger.error('Source not found!')
        return
    parser = VseKonkursyParser(source_url=source.url)
    parser.parse_data()
    parser.save_data(session=session)
    logger.info('Events were updated!')
