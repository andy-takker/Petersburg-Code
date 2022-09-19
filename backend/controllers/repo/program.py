from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import Program
from database.engine import get_async_session


class ProgramRepo:

    def __init__(self, sesssion: AsyncSession = Depends(get_async_session)):
        self.session = sesssion

    async def get_program(self, program_id: int, with_options=False):
        options = None
        if with_options:
            options = (
                selectinload(Program.study_areas),
                selectinload(Program.organization),
                selectinload(Program.directivity),
                selectinload(Program.education_profiles),
            )
        return await self.session.get(Program, ident=program_id, options=options)
