from Model.baseModel import BaseModel
from Entities.group import Group
import psycopg2
import time


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class GroupModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(GroupModel, self).__init__(dbname, user, password, host)
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

    def add_entity(self, new_entity):
        request = 'INSERT INTO groups("name", "number of members", "date of creation")' \
                  'VALUES (%s, %s, %s)'
        data = (new_entity.name, new_entity.number_of_members, new_entity.date_of_creation)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entities(self):
        request = 'SELECT * FROM groups'
        groups = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if records is not None:
                for record in records:
                    groups.append(Group(record[0], record[1], record[2], record[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        finally:
            return groups

    def update_entity(self, update_entity):
        request = 'UPDATE groups SET name=%s, "number of members"=%s, "date of creation"=%s WHERE group_id = %s'
        data = (update_entity.name, update_entity.number_of_members, update_entity.date_of_creation, update_entity.id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_entity(self, entity_id):
        if not does_contain(entity_id, self.get_entities()):
            print("No group on this id")
            return
        request = 'DELETE FROM groups WHERE group_id = %s'
        try:
            self.delete_links(entity_id)
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def get_entity(self, entity_id):
        request = 'SELECT * FROM groups WHERE group_id = %s'
        group = None
        try:
            self.cursor.execute(request, (entity_id,))
            record = self.cursor.fetchone()
            group = Group(record[0], record[1], record[2], record[3])
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return group

    def set_links(self, first_entity_id, second_entity_id):
        request = 'SELECT * FROM users WHERE user_id = %s'
        try:
            self.cursor.execute(request, (second_entity_id,))
            user = None
            user = self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
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
        request = 'DELETE FROM user_groups WHERE group_id = %s'
        try:
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def generate(self, number):
        request = 'INSERT INTO groups(name, "number of members", "date of creation") ' \
                  'SELECT MD5(random()::text), trunc(random()*%s)::int, timestamp \'1-1-1\' ' \
                  '+ random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') FROM generate_series(1 , %s)'
        data = (number, number)
        try:
            self.cursor.execute(request, data)
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

    def find_not_empty_groups_filter_users(self):
        request = 'SELECT * FROM "groups" WHERE "number of members" > 0 ORDER BY(SELECT COUNT(*) ' \
                  '' \
                  '' \
                  'FROM "user_groups" WHERE "user_groups".group_id = "groups".group_id) ASC'
        data = ()
        groups = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            temp = self.cursor.fetchall()
            finish = time.time()
            print("\nExecution time: " + str(finish - start))
            for item in temp:
                groups.append(Group(item[0], item[1], item[2], item[3], item[4]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return groups

    def find_not_empty_group_filter_user_age(self, min_, max_):
        request = 'SELECT "groups".group_id, "groups".name, "groups"."date of creation", ' \
                  '"groups"."number of members", "users"."last name" ' \
                  'FROM "groups" JOIN "user_groups" ON "user_groups".group_id = "groups".group_id ' \
                  'JOIN "users" ON "user_groups".user_id = "users".user_id ' \
                  'WHERE "users".age >= %s AND "users".age <= %s ORDER BY id ASC'
        data = (min_, max_)
        groups = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            records = self.cursor.fetchall()
            finish = time.time()
            print("\nExecution time: " + str(finish - start))
            for item in records:
                groups.append((item[0], item[1], item[2], item[3], item[4]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return groups
