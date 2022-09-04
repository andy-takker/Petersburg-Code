from typing import Optional

import requests

from api.schemas.skill import SkillList
from api.schemas.profession import Proektoria


class ProektoriaAPI:
    url = 'https://lb.proektoria.online/api/suits'

    def get_suits(self) -> Optional[SkillList]:
        result = requests.get(self.url)
        if result.ok:
            return SkillList(skills=result.json()['skills'])

    def post_suits(self, skills: SkillList) -> Optional[Proektoria]:
        data = skills.dict()
        result = requests.post(self.url, json=data)
        if result.ok:
            return Proektoria(professions=result.json()['related'])
