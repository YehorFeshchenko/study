from Model.baseModel import BaseModel
from Storage.tables import Group
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


class GroupModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(GroupModel, self).__init__(dbname, user, password, host)

    def get_entities(self):
        try:
            groups = self.session.query(Group)
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return groups

    def get_entity(self, entity_id):
        try:
            group = self.session.query(Group).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return group

    def delete_entity(self, entity_id):
        try:
            self.delete_links(entity_id)
            self.session.query(Group).filter_by(group_id=entity_id).delete()
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
            self.session.query(User_groups).filter_by(group_id=entity_id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print(error)
            self.session.execute("ROLLBACK")

    def generate(self, number):
        request = 'INSERT INTO groups(name, "number_of_members", "date_of_creation") ' \
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
        request = 'SELECT * FROM "groups" WHERE "number_of_members" > 0 ORDER BY(SELECT COUNT(*) ' \
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
                groups.append(Group(item[0], item[1], item[2], item[3]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return groups

    def find_not_empty_group_filter_user_age(self, min_, max_):
        request = 'SELECT "groups".group_id, "groups".name, "groups"."date_of_creation", ' \
                  '"groups"."number_of_members", "users"."last name" ' \
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
