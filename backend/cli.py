import json

import typer
from celery_sqlalchemy_scheduler import PeriodicTask, IntervalSchedule

from config import get_settings
from database import Source
from database.engine import get_session
from loguru import logger

settings = get_settings()
app = typer.Typer()


@app.command(name='add-task')
def add_task(name: str):
    print(f"Hello {name}!")


@app.command(name='create-parse-task')
def create_parse_task():
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


if __name__ == '__main__':
    app()
