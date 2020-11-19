from View.view import View


def menu(userModel, profileModel, postModel, groupModel):
    in_menu = True
    while in_menu:
        info = View.main_menu()
        if info == 'error':
            print("Incorrect input")
            continue
        if info == '1':
            while True:
                sub_info = View.sub_menu()
                if sub_info == -1:
                    continue
                else:
                    break
            if sub_info == '1':
                user = View.add_user()
                userModel.add_entity(user)
                continue
            elif sub_info == '2':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                temp_user = userModel.get_entity(input_id)
                if temp_user is None:
                    print("No user on this id!")
                else:
                    userModel.update_entity(View.update_user(temp_user))
            elif sub_info == '3':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                userModel.delete_entity(input_id)
            elif sub_info == '4':
                while True:
                    generate_number = View.generate_entity()
                    if generate_number == -1:
                        continue
                    else:
                        break
                userModel.generate(generate_number)
            elif sub_info == '5':
                while True:
                    option = View.find_users()
                    if option == -1:
                        continue
                    else:
                        break
                if option == '1':
                    min_ = View.input_sort_id()
                    max_ = View.input_sort_id()
                    users_filter = userModel.filter_from_id(min_, max_)
                    for user_temp in users_filter:
                        View.show_user(user_temp)
                elif option == '2':
                    while True:
                        limit_usr = View.get_limit()
                        if limit_usr == -1:
                            continue
                        else:
                            break
                    users_fil = userModel.filter_from_desc(limit_usr)
                    for item_ in users_fil:
                        View.show_user(item_)
                elif option == '3':
                    min_ = View.input_sort_age()
                    max_ = View.input_sort_age()
                    users_filter = userModel.filter_from_age(min_, max_)
                    for user_temp in users_filter:
                        View.show_user(user_temp)
                else:
                    print("Exit done")
                    continue
            elif sub_info == '6':
                while True:
                    id_find = View.id_find()
                    if id_find == -1:
                        continue
                    else:
                        break
                user = userModel.get_entity(id_find)
                if user is None:
                    print("No user on this id")
                else:
                    View.show_user(user)
            elif sub_info == '7':
                View.set_link_print()
                while True:
                    first_id_ = View.id_find()
                    if first_id_ == -1:
                        continue
                    else:
                        break
                while True:
                    second_id_ = View.id_find()
                    if second_id_ == -1:
                        continue
                    else:
                        break
                userModel.set_links(first_id_, second_id_)
            elif sub_info == '8':
                View.delete_link_print()
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                userModel.delete_links(input_id)
            else:
                continue
        elif info == '2':
            while True:
                sub_info = View.sub_menu()
                if sub_info == -1:
                    continue
                else:
                    break
            if sub_info == '1':
                profile = View.add_profile()
                profileModel.add_entity(profile)
                continue
            elif sub_info == '2':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                profile = profileModel.get_entity(input_id)
                if profile is None:
                    print("No profile on this id!")
                else:
                    profileModel.update_entity(View.update_profile(profile))
            elif sub_info == '3':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                profileModel.delete_entity(input_id)
            elif sub_info == '4':
                while True:
                    generate_number = View.generate_entity()
                    if generate_number == -1:
                        continue
                    else:
                        break
                profileModel.generate(generate_number)
            elif sub_info == '5':
                View.find_profiles()
            elif sub_info == '6':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                profile = profileModel.get_entity(input_id)
                if profile is None:
                    print("No profile on this id")
                else:
                    View.show_profile(profile)
            elif sub_info == '7':
                print("One to many so not implemented!")
            elif sub_info == '8':
                print("One to many so not implemented!")
            else:
                continue
        elif info == '3':
            while True:
                sub_info = View.sub_menu()
                if sub_info == -1:
                    continue
                else:
                    break
            if sub_info == '1':
                post = View.add_post()
                postModel.add_entity(post)
                continue
            elif sub_info == '2':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                post = postModel.get_entity(input_id)
                if post is None:
                    print("No post on this id!")
                else:
                    postModel.update_entity(View.update_post(post))
            elif sub_info == '3':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                postModel.delete_entity(input_id)
            elif sub_info == '4':
                while True:
                    generate_number = View.generate_entity()
                    if generate_number == -1:
                        continue
                    else:
                        break
                postModel.generate(generate_number)
            elif sub_info == '5':
                posts = postModel.find_post_profile()
                for item in posts:
                    View.formatted_post(item)
            elif sub_info == '6':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                post = postModel.get_entity(input_id)
                if post is None:
                    print("No post on this id")
                else:
                    View.show_post(post)
            elif sub_info == '7':
                print("One to many so not implemented!")
            elif sub_info == '8':
                print("One to many so not implemented!")
            else:
                continue
        elif info == '4':
            while True:
                sub_info = View.sub_menu()
                if sub_info == -1:
                    continue
                else:
                    break
            if sub_info == '1':
                group = View.add_group()
                groupModel.add_entity(group)
                continue
            elif sub_info == '2':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                group = groupModel.get_entity(input_id)
                if group is None:
                    print("No group on this id!")
                else:
                    groupModel.update_entity(View.update_group(group))
            elif sub_info == '3':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                groupModel.delete_entity(input_id)
            elif sub_info == '4':
                while True:
                    generate_number = View.generate_entity()
                    if generate_number == -1:
                        continue
                    else:
                        break
                groupModel.generate(generate_number)
            elif sub_info == '5':
                while True:
                    choice = View.find_groups()
                    if choice == -1:
                        continue
                    else:
                        break
                if choice == '1':
                    groups = groupModel.find_not_empty_groups_filter_users()
                    for item in groups:
                        View.show_group(item)
                elif choice == '2':
                    min_ = View.input_sort_age()
                    max_ = View.input_sort_age()
                    groups = groupModel.find_not_empty_group_filter_user_age(min_, max_)
                    for item in groups:
                        View.formatted_group(item)
                else:
                    print("Exit done")
                    continue
            elif sub_info == '6':
                while True:
                    input_id = View.id_find()
                    if input_id == -1:
                        continue
                    else:
                        break
                group = groupModel.get_entity(input_id)
                if group is None:
                    print("No group on this id")
                else:
                    View.show_group(group)
            elif sub_info == '7':
                View.set_link_print()
                while True:
                    first_id = View.id_find()
                    if first_id == -1:
                        continue
                    else:
                        break
                while True:
                    second_id = View.id_find()
                    if second_id == -1:
                        continue
                    else:
                        break
                groupModel.set_links(first_id, second_id)
            elif sub_info == '8':
                View.delete_link_print()
                while True:
                    del_id = View.id_find()
                    if del_id == -1:
                        continue
                    else:
                        break
                groupModel.delete_links(del_id)
            else:
                continue
        else:
            in_menu = False
            continue
