from Model.baseModel import BaseModel
from Storage.tables import Profile
import psycopg2
import time
from sqlalchemy import exc


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class ProfileModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(ProfileModel, self).__init__(dbname, user, password, host)

    def get_entities(self):
        try:
            profiles = self.session.query(Profile)
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return profiles

    def get_entity(self, entity_id):
        try:
            profile = self.session.query(Profile).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return profile

    def delete_entity(self, entity_id):
        try:
            self.session.query(Profile).filter_by(profile_id=entity_id).delete()
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")

    def set_links(self, first_entity_id, second_entity_id):
        pass

    def delete_links(self, entity_id):
        pass

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
        request = 'INSERT INTO profiles(nickname, "date_of_registration", country, user_id) ' \
                  'SELECT MD5(random()::text), timestamp \'1-1-1\' + random()*(timestamp \'2020-10-10\' - ' \
                  'timestamp \'1-1-1\'), MD5(random()::text), ' \
                  'trunc(random()*((SELECT MAX(user_id) FROM "users")-1)+1)::int '\
                  'FROM generate_series(1 , %s)'
        data = (number,)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
