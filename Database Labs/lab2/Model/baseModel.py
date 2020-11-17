from abc import ABC, abstractmethod
import psycopg2


class BaseModel(ABC):
    def __init__(self, dbname, user, password, host):
        self.dbname_ = dbname
        self.user_ = user
        self.password_ = password
        self.host_ = host
        try:
            self.conn = psycopg2.connect(dbname=self.dbname_, user=self.user_, password=self.password_, host=self.host_)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        try:
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @abstractmethod
    def add_entity(self, new_entity):
        pass

    @abstractmethod
    def get_entity(self, entity_id):
        pass

    @abstractmethod
    def get_entities(self):
        pass

    @abstractmethod
    def update_entity(self, update_entity):
        pass

    @abstractmethod
    def delete_entity(self, entity_id):
        pass

    @abstractmethod
    def set_links(self , first_entity_id , second_entity_id):
        pass

    @abstractmethod
    def delete_links(self, entity_id):
        pass

    @abstractmethod
    def generate(self, number):
        pass

