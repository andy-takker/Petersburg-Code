import typer

from controllers.digital_spb import DigitalSpbAPI
from database.utils import create_parse_task, create_directivities

app = typer.Typer()


@app.command(name='create-parse-task')
def create_parse_task_command():
    create_parse_task()


@app.command(name='fill-db')
def fill_database():
    create_parse_task()
    create_directivities()


@app.command(name='download-programs')
def download_programs():
    digital_spb_api = DigitalSpbAPI()
    digital_spb_api.download_programs()


if __name__ == '__main__':
    app()
