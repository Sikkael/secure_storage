from _base_repository import *


class JsonRepository(AbstractRepository):

    def add(self, model: IModel) -> None:
        pass

    def get(self, order_id: int) -> IModel:
        pass

    def list(self) -> list:
        pass

    def remove(self) -> None:
        pass
