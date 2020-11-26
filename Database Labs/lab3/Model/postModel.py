from Model.baseModel import BaseModel
from Storage.tables import Post
import psycopg2
import time
from sqlalchemy import exc


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class PostModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(PostModel, self).__init__(dbname, user, password, host)

    def get_entities(self):
        try:
            posts = self.session.query(Post)
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return posts

    def get_entity(self, entity_id):
        try:
            post = self.session.query(Post).get(entity_id)
            self.session.commit()
        except(Exception, exc.DatabaseError, exc.InvalidRequestError) as error:
            print("Error occurred: " + error)
            self.session.execute("ROLLBACK")
        return post

    def delete_entity(self, entity_id):
        try:
            self.session.query(Post).filter_by(post_id=entity_id).delete()
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
        request = 'INSERT INTO posts(topic, "date_of_publishing", owner, profile_id) ' \
                  'SELECT MD5(random()::text), timestamp \'1-1-1\' + random()*(timestamp \'2020-10-10\' - ' \
                  'timestamp \'1-1-1\'), MD5(random()::text), ' \
                  'trunc(random()*((SELECT MAX(profile_id) FROM "profiles")-1)+1)::int ' \
                  'FROM generate_series(1 , %s)'
        data = (number,)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def find_post_profile(self):
        request = 'SELECT post.topic , "profiles".nickname FROM "posts" post ' \
                  'JOIN "profiles" ON post.profile_id = "profiles".profile_id ORDER BY topic DESC, nickname ASC'
        data = ()
        connections = list()
        try:
            start = time.time()
            self.cursor.execute(request, data)
            temp = self.cursor.fetchall()
            finish = time.time()
            print("\nExecution time: " + str(finish - start))
            for item in temp:
                cons = (item[0], item[1])
                connections.append(cons)
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return connections
