# author: ShaunJose
# File description: Handles the group (including accepting user login, user additon and deletion etc)


# Imports
from FileFunctionalities import readFile
from constants import USERS_FILE, N_USERS_FILE, USER_DELIM, USER_PASS_DELIM

# Accepts a user log in
def acceptUser():

    users_pass = _getCurrUsersPass_()
    print(users_pass)

    new_users = _getNewUsers_()
    print(new_users)


# Reads current user's and passwords file and return a dict with users and pass
def _getCurrUsersPass_():
    """
    Gets the current users and passwords and returns a dictionary with the users and passwords

    return: dict with users array (accesed by 'users' key) and passwords array (accessed by 'passwords' key)
    """

    # get users file contents
    curr_users_contents = readFile(USERS_FILE)
    users_passwords = curr_users_contents.split(USER_DELIM)
    ret = {'users': [], 'passwords': []} # init users and pass dict

    # seperate users from passwords
    for userPass in users_passwords:
        if not userPass: # if string is empty we're done
            break
        tmpArr = userPass.split(USER_PASS_DELIM)
        ret['users'].append(tmpArr[0])
        ret['passwords'].append(tmpArr[1])

    return ret


# Reads the new user file and returns array with new usernames
def _getNewUsers_():
    """
    Reads contents of the new user files and gives back an array with new usernames

    return: Array with new usernames
    """

    # get new user's usernames
    new_users_contents = readFile(N_USERS_FILE)
    new_users = new_users_contents.split(USER_DELIM)

    return new_users[:-1] # ignore last empty element
