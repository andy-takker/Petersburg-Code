import logging

from controllers.parsers.base import Parser
from database.engine import Session
from celery_worker.celery_conf import celery as celery_app

logger = logging.getLogger(__name__)


class ProgramParser(Parser):
    def __init__(self):
        pass

    def parse_data(self):
        pass

    def save_data(self, session: Session):
        pass


@celery_app.task(bind=True, name='parse_programs', track_started=True)
def make_parse(self):
    session = Session()
    logger.info('Programs were updated')
