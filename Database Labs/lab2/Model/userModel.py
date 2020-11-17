from Model.baseModel import BaseModel
from Entities.user import User
import psycopg2
import time


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class UserModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(UserModel, self).__init__(dbname, user, password, host)
        try:
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entities(self):
        request = 'SELECT * FROM users'
        users = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if records is not None:
                for record in records:
                    users.append(User(record[0], record[1], record[2], record[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        finally:
            return users

    def get_entity(self, entity_id):
        request = 'SELECT * FROM users WHERE user_id = %s'
        data = (entity_id,)
        user = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchone()
            user = User(record[0], record[1], record[2], record[3])
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return user

    def add_entity(self, new_entity):
        request = 'INSERT INTO "users"("first name", "last name", "age") VALUES (%s , %s , %s)'
        data = (new_entity.first_name, new_entity.last_name, new_entity.age)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def update_entity(self, update_entity):
        request = 'UPDATE users SET "first name"=%s, "last name"=%s, age=%s WHERE user_id=%s'
        data = (update_entity.first_name, update_entity.last_name, update_entity.age, update_entity.id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_entity(self, entity_id):
        if not does_contain(entity_id, self.get_entities()):
            print("No user on this id")
            return
        request = 'DELETE FROM users WHERE user_id = %s'
        try:
            self.delete_links(entity_id)
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def set_links(self, first_entity_id, second_entity_id):
        request = 'SELECT * FROM groups WHERE group_id = %s'
        try:
            self.cursor.execute(request, (second_entity_id,))
            book = self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        if self.get_entity(first_entity_id) is None or book is None:
            print('No entities on this ids')
            return
        request = 'INSERT INTO user_groups(user_id , group_id) VALUES (%s,%s)'
        data = (first_entity_id, second_entity_id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_links(self, entity_id):
        if not does_contain(entity_id, self.get_entities()):
            print("No user on this id")
            return
        request = 'DELETE FROM user_groups WHERE user_id = %s'
        try:
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def __get_generate_datas(self, request, data):
        try:
            self.cursor.execute(request, data)
            datas = self.cursor.fetchall()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return datas

    def generate(self, number):
        request = 'INSERT INTO "user"(name , honor , blacklist) SELECT MD5(random()::text), random(), (random()::int)::boolean FROM generate_series(1 , %s)'
        data = (number,)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
