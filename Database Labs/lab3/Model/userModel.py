from Model.baseModel import BaseModel
from Storage.tables import User
from Storage.tables import User_groups
import psycopg2
import time
from sqlalchemy import exc


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class UserModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(UserModel, self).__init__(dbname, user, password, host)

    def get_entities(self):
        try:
            users = self.session.query(User)
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return users

    def get_entity(self, entity_id):
        try:
            user = self.session.query(User).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return user

    def delete_entity(self, entity_id):
        try:
            self.delete_links(entity_id)
            self.session.query(User).filter_by(user_id=entity_id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")

    def set_links(self, first_entity_id, second_entity_id):
        try:
            new_entity = User_groups(first_entity_id, second_entity_id)
            self.session.add(new_entity)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")

    def delete_links(self, entity_id):
        try:
            self.session.query(User_groups).filter_by(user_id=entity_id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    def __get_generate_data(self, request, data):
        try:
            self.cursor.execute(request, data)
            records = self.cursor.fetchall()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return records

    def generate(self, number):
        request = 'INSERT INTO users("first_name", "last_name", age) SELECT MD5(random()::text), MD5(random()::text),' \
                  ' trunc(random()*%s)::int FROM generate_series(1 , %s)'
        data = (number, number)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def filter_from_id(self, min_, max_):
        request = 'SELECT * FROM "users" WHERE "users".user_id >= %s AND "users".user_id <= %s ' \
                  'ORDER BY(SELECT COUNT(*) FROM "profiles" WHERE "profiles".user_id = "users".user_id)'
        data = (min_, max_)
        users_list = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            users = self.cursor.fetchall()
            finish = time.time()
            print("\nExecution time: " + str(finish - start))
            for item in users:
                users_list.append(User(item[0], item[1], item[2], item[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return users_list

    def filter_from_age(self, min_, max_):
        request = 'SELECT * FROM "users" WHERE "users".age >= %s AND "users".age <= %s ' \
                  'ORDER BY(SELECT COUNT(*) FROM "profiles" WHERE "profiles".user_id = "users".user_id)'
        data = (min_, max_)
        users_list = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            users = self.cursor.fetchall()
            finish = time.time()
            print("\nExecution time: " + str(finish - start))
            for item in users:
                users_list.append(User(item[0], item[1], item[2], item[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return users_list

    def filter_from_desc(self, limit):
        request = 'SELECT * FROM "users" ORDER BY(SELECT COUNT("profiles".profile_id) FROM "profiles" ' \
                  'WHERE "profiles".user_id = "users".user_id), users."first_name" DESC LIMIT %s'
        data = (limit,)
        users_list = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            users = self.cursor.fetchall()
            finish = time.time()
            print("\nExecution time: " + str(finish - start))
            for item in users:
                users_list.append(User(item[0], item[1], item[2], item[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return users_list
