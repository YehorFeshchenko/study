from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import exc
import psycopg2


class BaseModel(ABC):
    def __init__(self, dbname_, user_, password_, host_):
        self._dbname = dbname_
        self._user = user_
        self._password = password_
        self._host = host_
        try:
            self.conn = psycopg2.connect(dbname=self._dbname, user=self._user,
                                         password=self._password, host=self._host)
            self.engine = create_engine("postgres+psycopg2://{}:{}@{}/{}"
                                        .format(self._user, self._password, self._host, self._dbname))
            self.session = Session(bind=self.engine)
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError, exc.DatabaseError, exc.InvalidRequestError) as error:
            self.session.execute("ROLLBACK")
            self.cursor.execute('ROLLBACK')
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
            self.session.close()
        except (Exception, psycopg2.DatabaseError, exc.InvalidRequestError) as error:
            self.session.execute("ROLLBACK")
            self.cursor.execute('ROLLBACK')
            print(error)

    def add_entity(self, new_entity):
        try:
            self.session.add(new_entity)
            self.session.commit()
        except (Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            self.session.execute('ROLLBACK')
            print(error)

    @abstractmethod
    def get_entity(self, entity_id):
        pass

    @abstractmethod
    def get_entities(self):
        pass

    def update_entity(self, update_entity):
        try:
            self.session.add(update_entity)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    @abstractmethod
    def delete_entity(self, entity_id):
        pass

    @abstractmethod
    def set_links(self, first_entity_id, second_entity_id):
        pass

    @abstractmethod
    def delete_links(self, entity_id):
        pass

    @abstractmethod
    def generate(self, number):
        pass
