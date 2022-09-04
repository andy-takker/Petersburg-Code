from typing import List

import requests
from loguru import logger
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from api.schemas.program import ProgramInput
from config import get_settings
from database import Directivity, Organization, StudyArea, Program
from database.engine import get_session


class DigitalSpbAPI:
    BASE_URL = "https://odo.gate.petersburg.ru/ext_edu"
    PROGRAMS_URL = f"{BASE_URL}/external/edu/programs"
    PROGRAM_URL = f"{BASE_URL}/external/edu/program"

    def __init__(self):
        settings = get_settings()
        self.TOKEN = settings.DIGITAL_SPB_TOKEN
        self.programs: List[ProgramInput] = []
        self.organizations = set()
        self.study_areas = set()

    def _get(self, url: str, params: dict):
        return requests.get(
            url=url,
            params=params,
            headers={'Authorization': f'Bearer {self.TOKEN}'},
        )

    def get_external_edu_programs(
            self,
            directivity_id: int,
            page: int = 1,
            count: int = 100,
    ) -> dict:
        result = self._get(
            url=self.PROGRAMS_URL,
            params={
                'page': page,
                'directivity': directivity_id,
                'count': count,
                'radius': 10,
            },
        )
        return result.json()

    def download_programs(self):
        with get_session() as session:
            directivities: list[Directivity] = session.query(Directivity).all()
            for directivity in directivities:
                logger.info(f'Download {directivity.name}...')
                self.download_directivity(directivity.id)
            for program in self.programs:
                self.organizations.add(program.organization)
                self.study_areas.update(program.study_areas)
            self.save_models(session=session)

    def download_directivity(self, directivity_id: int):
        count = -1
        page = 1
        while True:
            result = self.get_external_edu_programs(
                directivity_id=directivity_id,
                page=page,
            )
            if result['count'] == 0:
                break
            if count == -1:
                count = result['count']
            data = result['data']
            count -= len(data)
            programs: list[ProgramInput] = parse_obj_as(List[ProgramInput],
                                                        data)
            for p in programs:
                p.directivity_id = directivity_id
            self.programs.extend(programs)
            if count <= 0:
                break
            page += 1

    def save_models(self, session: Session):
        logger.info("Saving models!")
        for org in self.organizations:
            create_if_not_exist(session=session, model=Organization,
                                name=org)
        for sa in self.study_areas:
            create_if_not_exist(session=session, model=StudyArea, name=sa)
        session.commit()
        logger.info('Saving programs!')
        for program in self.programs:
            p: Program | None = session.get(Program, program.id)
            if p is None:
                p = Program(**program.dict(exclude={'organization','study_areas'})
                )
                organization = session.query(Organization).filter_by(
                    name=program.organization).first()
                p.organization = organization

                p.study_areas = session.query(StudyArea).filter(
                    StudyArea.name.in_(program.study_areas)).all()
            else:
                p.update_from_dict(
                    **program.dict(exclude={'organization','study_areas'})
                )
            session.add(p)
        session.commit()
        logger.info('Saving is ended!')


def create_if_not_exist(session: Session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return
    instance = model(**kwargs)
    session.add(instance)
