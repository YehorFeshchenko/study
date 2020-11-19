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
        request = 'SELECT * FROM "users" WHERE user_id = %s'
        user = None
        try:
            self.cursor.execute(request, (entity_id,))
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
        request = 'INSERT INTO users("first name", "last name", age) SELECT MD5(random()::text), MD5(random()::text),' \
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
                  'WHERE "profiles".user_id = "users".user_id), users."first name" DESC LIMIT %s'
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
