from Model.baseModel import BaseModel
from Entities.post import Post
import psycopg2
import time


def does_contain(entity_id, data_list):
    contains = False
    for record in data_list:
        if entity_id == record.id:
            contains = True
    return contains


class PostModel(BaseModel):
    def __init__(self, dbname, user, password, host):
        super(PostModel, self).__init__(dbname, user, password, host)
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
        request = 'SELECT * FROM posts'
        posts = list()
        try:
            self.cursor.execute(request)
            records = self.cursor.fetchall()
            if records is not None:
                for record in records:
                    posts.append(Post(record[0], record[1], record[2], record[3], record[4]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        finally:
            return posts

    def get_entity(self, entity_id):
        request = 'SELECT * FROM posts WHERE posts_id = %s'
        data = (entity_id,)
        post = None
        try:
            self.cursor.execute(request, data)
            record = self.cursor.fetchone()
            post = Post(record[0], record[1], record[2], record[3], record[4])
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)
        return post

    def add_entity(self, new_entity):
        request = 'INSERT INTO posts("topic", "date of publishing", "owner", "profile_id") ' \
                  'VALUES (%s , %s , %s, %s)'
        data = (new_entity.topic, new_entity.date_of_publishing, new_entity.owner, new_entity.id, new_entity.profile_id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def update_entity(self, update_entity):
        request = 'UPDATE posts SET "topic"=%s, "date of publishing"=%s, "owner"=%s , "profile_id"=%s ' \
                  'WHERE user_id=%s'
        data = (update_entity.topic, update_entity.date_of_publishing, update_entity.owner,
                update_entity.profile_id, update_entity.id)
        try:
            self.cursor.execute(request, data)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cursor.execute('ROLLBACK')
            print(error)

    def delete_entity(self, entity_id):
        if not does_contain(entity_id, self.get_entities()):
            print("No post on this id")
            return
        request = 'DELETE FROM posts WHERE posts_id = %s'
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
