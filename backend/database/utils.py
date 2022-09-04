import json

from celery_sqlalchemy_scheduler import PeriodicTask, IntervalSchedule
from loguru import logger

from database import Source, Directivity
from database.engine import get_session


def create_parse_task():
    """Создает задачу на парсинг данных из источника"""
    with get_session() as session:
        periodic_task = session.query(PeriodicTask).filter_by(
            task='parse_events').first()
        if periodic_task is None:
            if session.get(Source, 1) is None:
                logger.info('Source not found. Create source...')
                source = Source()
                source.name = 'Все конкурсы'
                source.url = 'https://vsekonkursy.ru/'
                source.enable = True
                session.add(source)
                logger.info('Source created!')
            logger.info('Task not found. Create task...')
            periodic_task = PeriodicTask()
            periodic_task.task = 'parse_events'
            periodic_task.name = 'Сохранение событий'
            periodic_task.total_run_count = 0
            periodic_task.interval = IntervalSchedule(every=5, period='minutes')
        periodic_task.enabled = True
        periodic_task.kwargs = json.dumps({'source_id': 1})
        session.add(periodic_task)
        session.commit()
        logger.info('Task created!')


def create_directivities():
    with get_session() as session:
        if session.query(Directivity).count() > 0:
            logger.info('Directivities already in database!')
            return
        session.add_all([
            Directivity(id=1, name='Естественнонаучная'),
            Directivity(id=2, name='Физкультурно-спортивная'),
            Directivity(id=3, name='Техническая'),
            Directivity(id=4, name='Художественная'),
            Directivity(id=5, name='Туристско-краеведческая'),
            Directivity(id=7, name='Физкультурно-спортивная'),
        ])
        session.commit()
        logger.info('Directivities created!')
