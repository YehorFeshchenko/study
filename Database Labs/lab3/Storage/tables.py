from sqlalchemy import Column, Integer, ForeignKey, Text, Float, Boolean, Date, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.indexable import index_property

Base = declarative_base()


class User_groups(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    age = Column(Integer)
    children = relationship("Profile")

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age


class Group(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    date_of_creation = Column(Date, nullable=False)
    number_of_members = Column(Integer, nullable=False)
    users = relationship("User", secondary="user_groups")

    def __init__(self, name, date_of_creation, number_of_members):
        self.name = name
        self.date_of_creation = date_of_creation
        self.number_of_members = number_of_members


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    topic = Column(Text, nullable=False)
    date_of_publishing = Column(Date, nullable=False)
    owner = Column(Text, nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.profile_id'), nullable=False)

    def __init__(self, topic, date_of_publishing, owner, profile_id):
        self.topic = topic
        self.date_of_publishing = date_of_publishing
        self.owner = owner
        self.profile_id = profile_id


class Profile(Base):
    __tablename__ = "profiles"
    profile_id = Column(Integer, primary_key=True)
    nickname = Column(Text, nullable=False)
    date_of_registration = Column(Date, nullable=False)
    country = Column(Text)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    children = relationship("Post")

    def __init__(self, nickname, date_of_registration, country, user_id):
        self.nickname = nickname
        self.date_of_registration = date_of_registration
        self.country = country
        self.user_id = user_id
