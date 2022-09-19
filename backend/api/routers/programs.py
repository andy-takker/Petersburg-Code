from fastapi import APIRouter, Path, Depends, HTTPException

from api.schemas.program import FullProgramSchema
from controllers.digital_spb import DigitalSpbAPI
from controllers.repo.program import ProgramRepo

router = APIRouter(prefix='/programs',
                   tags=['Программы дополнительного образования'])


@router.get(
    path='/{program_id}',
    response_model=FullProgramSchema,
    name='Полная информация о программе',
)
async def get_full_info_program(
        program_id: int = Path(
            title='Program ID',
            description='ID of program from database',
        ),
        program_dao: ProgramRepo = Depends(),
) -> FullProgramSchema:
    if await program_dao.get_program(program_id) is None:
        raise HTTPException(status_code=404, detail='Program no found')
    return DigitalSpbAPI().get_education_program_full_info(program_id)
