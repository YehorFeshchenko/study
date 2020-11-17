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

    def generate(self, number):  # TODO
        request = 'INSERT INTO "author"(name , date_of_first_publication , year_of_birth , year_of_death) ' \
                  'SELECT MD5(random()::text), trunc(random()*%s)::int , timestamp \'1-1-1\' ' \
                  '+ random()*(timestamp \'2020-10-10\' - timestamp \'1-1-1\') FROM generate_series(1 , %s)'
        data = (number, number, number)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def __get_generate_datas(self, request, data):  # TODO
        try:
            self.cursor.execute(request, data)
            datas = self.cursor.fetchall()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return datas
