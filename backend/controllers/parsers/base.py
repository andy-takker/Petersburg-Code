import abc

from database.engine import Session


class Parser(abc.ABC):
    @abc.abstractmethod
    def parse_data(self):
        pass

    @abc.abstractmethod
    def save_data(self, session: Session):
        pass
