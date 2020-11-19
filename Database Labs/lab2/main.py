from Controller.controller import menu
from Model.userModel import UserModel
from Model.groupModel import GroupModel
from Model.postModel import PostModel
from Model.profileModel import ProfileModel


def get_password():
    f = open(r"D:\Job\Apps\password.txt", "r")
    data = f.read()
    f.close()
    return data


password = get_password()

groupModel = GroupModel('Lab1_db', 'postgres', password, 'localhost')
postModel = PostModel('Lab1_db', 'postgres', password, 'localhost')
userModel = UserModel('Lab1_db', 'postgres', password, 'localhost')
profileModel = ProfileModel('Lab1_db', 'postgres', password, 'localhost')

menu(userModel, profileModel, postModel, groupModel)

userModel.__del__()
postModel.__del__()
groupModel.__del__()
profileModel.__del__()
