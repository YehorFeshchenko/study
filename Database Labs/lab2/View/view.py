import datetime
from Entities.user import User
from Entities.profile import Profile
from Entities.post import Post
from Entities.group import Group


class View:

    @staticmethod
    def set_link_print():
        print("Input Main Entity, then second")

    @staticmethod
    def delete_link_print():
        print("Input Main Entity id")

    @staticmethod
    def id_find():
        input_id = input("Input id:\n")
        if input_id.isdigit() is False:
            print("Not a number")
            return -1
        else:
            return int(input_id)

    @staticmethod
    def update_profile(update_profile):
        while True:
            info = input("Choose what field do you want to change:\n1)nickname\n2)date_of_registration\n"
                         "3)country\n4)user_id\n5)Exit\n")

            if info == '1':
                update_profile.nickname = input("Input nickname\n")
            elif info == '2':
                try:
                    date = datetime.datetime.strptime(input("Input date of registration(yyyy-mm-dd):\n"),
                                                      '%Y-%m-%d')
                except:
                    print("Incorrect data format")
                    continue
                update_profile.date_of_registration = date
            elif info == '3':
                update_profile.country = input("Input country\n")
            elif info == '4':
                user_id = input("Input user_id\n")
                if user_id.isdigit() is False:
                    print("Not a number")
                    continue
                else:
                    update_profile.user_id = user_id
            elif info == '5':
                print("Exit done")
                return update_profile
            else:
                print("Try again!")
                continue

    @staticmethod
    def update_user(update_user):
        while True:
            info = input(
                "Choose what field do you want to change:\n1)first_name\n2)last_name\n3)age\n4)Exit\n")
            if info == '1':
                update_user.first_name = input("Input first_name\n")
                continue
            elif info == '2':
                update_user.last_name = input("Input last_name\n")
                continue
            elif info == '3':
                age = input("Input age\n")
                if age.isdigit() is False:
                    print("Not a number")
                    continue
                else:
                    update_user.age = age
            elif info == '4':
                print("Exit done")
                return update_user
            else:
                print("Try again!")
                continue

    @staticmethod
    def update_group(update_group):
        while True:
            info = input(
                "Choose what field do you want to change:\n1)name\n2)number_of_members\n3)date_of_creation\n4)Exit")
            if info == '1':
                update_group.name = input("Input name\n")
            elif info == '2':
                num = input("Input number_of_members\n")
                if num.isdigit() is False:
                    print("Not a number")
                    continue
                update_group.number_of_members = num
            elif info == '3':
                try:
                    date = datetime.datetime.strptime(input("Input date of creation(yyyy-mm-dd):\n"),
                                                      '%Y-%m-%d')
                except:
                    print("Incorrect data format")
                    continue
                update_group.date_of_creation = date
            elif info == '4':
                print("Exit done")
                return update_group
            else:
                print("Try again!")
                continue

    @staticmethod
    def update_post(update_post):
        while True:
            info = input(
                "Choose what field do you want to change:\n1)topic\n2)date_of_publishing\n3)owner\n4)profile_id\n"
                "5)Exit\n")
            if info == '1':
                update_post.topic = input("Input topic\n")
                continue
            elif info == '2':
                try:
                    date = datetime.datetime.strptime(input("Input date of publishing(yyyy-mm-dd):\n"),
                                                      '%Y-%m-%d')
                except:
                    print("Incorrect data format")
                    continue
                update_post.date_of_publishing = date
            elif info == '3':
                update_post.owner = input("Input owner\n")
            elif info == '4':
                profile_id = input("Input profile_id\n")
                if profile_id.isdigit() is False:
                    print("Not a number")
                    continue
                else:
                    update_post.profile_id = profile_id
            elif info == '5':
                print("Exit done")
                return update_post

    @staticmethod
    def generate_entity():
        number = input("Input generate number\n")
        if number.isdigit() is False:
            print("Not a number")
            return -1
        else:
            return int(number)

    @staticmethod
    def sub_menu():
        print(
            "Choose action:\n1)Add\n2)Update\n3)Delete\n4)Generate\n5)Find/Filter\n6)Get\n"
            "7)Set links\n8)Delete links\nExit")
        info = input("Input number\n")
        if (info == '1' or info == '2' or info == '3' or info == '4' or info == '5' or info == '6' or info == '7'
                or info == '8'):
            return info
        elif info == 'Exit':
            print("Exit done")
            return
        else:
            print("Incorrect input")
            return -1

    @staticmethod
    def add_post():
        topic = input("Input topic:\n")
        while True:
            try:
                date = datetime.datetime.strptime(input("Input date of publishing(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect date format")
                continue
        owner = input("Input owner:\n")
        while True:
            profile_id = input("Input profile_id\n")
            if profile_id.isdigit() is False:
                print("Not a number")
                continue
            else:
                break
        new_post = Post(0, topic, date, owner, profile_id)
        return new_post

    @staticmethod
    def formatted_post(item):
        print("topic-> {} ".format(item[0]))
        print("nickname-> {} ".format(item[1]))
        print('\n')

    @staticmethod
    def formatted_group(item):
        print('{} id-> {}'.format('Group', item[0]))
        print('{} name-> {}'.format('Group', item[1]))
        print('{} date of creation -> {}'.format('Group', item[2]))
        print('{} number of members-> {}'.format('Group', item[3]))
        print('{} last name -> {}'.format('User', item[4]))
        print('\n')

    @staticmethod
    def show_user(item):
        print('User id-> {}'.format(item.id))
        print('User first name-> {}'.format(item.first_name))
        print('User last name-> {}'.format(item.last_name))
        print('User age-> {}'.format(item.age))
        print('\n')

    @staticmethod
    def show_post(item):
        print('Post id-> {}'.format(item.id))
        print('Post topic-> {}'.format(item.topic))
        print('Post date of publishing-> {}'.format(item.date_of_publishing))
        print('Post profile id-> {}'.format(item.profile_id))
        print('\n')

    @staticmethod
    def show_group(item):
        print('Group id-> {}'.format(item.id))
        print('Group name-> {}'.format(item.name))
        print('Group date_of_creation-> {}'.format(item.date_of_creation))
        print('Group number_of_members-> {}'.format(item.number_of_members))
        print('\n')

    @staticmethod
    def show_profile(item):
        print('{} id-> {}'.format('Profile', item.id))
        print('{} nickname-> {}'.format('Profile', item.nickname))
        print('{} date_of_registration-> {}'.format('Profile', item.date_of_registration))
        print('{} country-> {}'.format('Profile', item.country))
        print('{} user_id-> {}'.format('Profile', item.user_id))
        print('\n')

    @staticmethod
    def main_menu():
        print("Choose number of option:\n1)User\n2)Profile\n3)Post\n4)Group\nExit")
        info = input("Input number\n")
        if info == '1' or info == '2' or info == '3' or info == '4' or info == 'Exit':
            return info
        else:
            return 'error'

    @staticmethod
    def add_user():
        first_name = input("Input first_name:\n")
        last_name = input("Input last_name:\n")
        while True:
            age = input("Input age:\n")
            if age.isdigit() is False:
                print("Not a number!")
                continue
            else:
                break
        new_user = User(0, first_name, last_name, age)
        return new_user

    @staticmethod
    def add_group():
        name = input("Input name:\n")
        while True:
            number = input("Input number_of_members:\n")
            if number.isdigit() is False:
                print("Not a number!")
                continue
            else:
                break
        while True:
            try:
                date = datetime.datetime.strptime(input("Input date_of_creation(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect date format")
                continue
        new_group = Group(0, name, number, date)
        return new_group

    @staticmethod
    def add_profile():
        nickname = input("Input nickname:\n")
        while True:
            try:
                date = datetime.datetime.strptime(input("Input date of registration(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect date format")
                continue
        country = input("Input country:\n")
        while True:
            user_id = input("Input user_id:\n")
            if user_id.isdigit() is False:
                print("Not a number!")
                continue
            else:
                break
        new_profile = Profile(0, nickname, date, country, user_id)
        return new_profile

    @staticmethod
    def input_sort_date():  # For Profile
        global min_d, max_d
        while True:
            try:
                min_d = datetime.datetime.strptime(input("Input min date_of_registration(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect data format")
                continue
        while True:
            try:
                max_d = datetime.datetime.strptime(input("Input max date_of_registration(yyyy-mm-dd):\n"), '%Y-%m-%d')
                break
            except:
                print("Incorrect data format")
                continue
        return min_d, max_d

    @staticmethod
    def find_users():
        print("1)Find users sorted by amount profiles from id\n2)Find users sorted by amount profiles desc\n"
              "3)Find users sorted by amount profiles from age\n4)Exit")
        info = input("Choose option:\n")
        if info == '1' or info == '2' or info == '3' or info == '4':
            return info
        else:
            print("Incorrect option")
            return -1

    @staticmethod
    def find_profiles():
        print("Not implemented!")

    @staticmethod
    def input_sort_id():
        while True:
            sort_id = input("Input id:\n")
            if sort_id.isdigit() is True:
                min_id = sort_id
                break
            else:
                print("Incorrect input")
                continue
        return int(min_id)

    @staticmethod
    def input_sort_age():
        while True:
            sort_age = input("Input age:\n")
            if sort_age.isdigit() is True:
                age = sort_age
                break
            else:
                print("Incorrect input")
                continue
        return int(age)

    @staticmethod
    def find_groups():
        print(
            "1) Find not empty groups sorted by amount of users\n2) Find not empty groups sorted by user's age\n"
            "3) Exit")
        info = input("Choose option:\n")
        if info == '1' or info == '2' or info == '3':
            return info
        else:
            print("Incorrect option")
            return -1

    @staticmethod
    def get_limit():
        limit = input("Input limit:\n")
        if limit.isdigit() is True:
            return int(limit)
        else:
            return -1
