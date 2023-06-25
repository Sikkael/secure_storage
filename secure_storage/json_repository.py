from irepository import *


class Entity:
    pass


class JsonRepository(IRepository):

    def get_all(self):
        pass

    def get_by_id(self, _id):
        pass

    def create(self, item):
        pass

    def update(self, item):
        pass

    def delete(self, _id):
        pass

    def add(self, entity) -> None:
        pass
 
    def get(self, order_id: int) -> Entity:
        pass

    def list(self) -> list:
        pass

    def remove(self) -> None:
        pass
