from Model.baseModel import BaseModel
from Entities.profile import Profile
import psycopg2
import time


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class ProfileModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(ProfileModel, self).__init__(dbname, user, password, host)
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
        request = 'SELECT * FROM profiles'
        profiles = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if records is not None:
                for record in records:
                    profiles.append(Profile(record[0], record[1], record[2], record[3], record[4]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        finally:
            return profiles

    def get_entity(self, entity_id):
        request = 'SELECT * FROM profile WHERE profile_id = %s'
        data = (entity_id,)
        profile = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchone()
            profile = Profile(record[0], record[1], record[2], record[3], record[4])
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return profile

    def add_entity(self, new_entity):
        request = 'INSERT INTO profiles("nickname", "date of registration", "country", "user_id") ' \
                  'VALUES (%s , %s , %s, %s)'
        data = (new_entity.first_name, new_entity.last_name, new_entity.age)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def update_entity(self, update_entity):
        request = 'UPDATE profiles SET "nickname"=%s, "date of registration"=%s, "country"=%s , "user_id"=%s ' \
                  'WHERE user_id=%s'
        data = (update_entity.nickname, update_entity.date_of_registration, update_entity.country,
                update_entity.user_id, update_entity.id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_entity(self, entity_id):
        if not does_contain(entity_id, self.get_entities()):
            print("No profile on this id")
            return
        request = 'DELETE FROM profiles WHERE profile_id = %s'
        try:
            self.delete_links(entity_id)
            self.cursor.execute(request, (entity_id,))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def set_links(self, first_entity_id, second_entity_id):
        pass

    def delete_links(self, entity_id):
        pass

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
