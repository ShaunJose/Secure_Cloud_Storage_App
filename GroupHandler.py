# author: ShaunJose
# File description: Handles the group (including accepting user login, user additon and deletion etc)


# Imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import os
from constants import USERS_FILE, N_USERS_FILE, USER_DELIM, USER_PASS_DELIM, PRIV_KEY_FILE, SHARED_KEY_FILE, ADMIN_PASS
from FileSharing import GoogleDriveAccess
from FileFunctionalities import readFile, saveFile
from KeyManagementSystem import KMS

# Accepts a user log in
def acceptUser():
    """
    Accepts a user login, then calls file sharing method to share files

    return: None
    """

    # get current users (with passwords) and new users
    users_pass = _getCurrUsersPass_()
    new_users = _getNewUsers_()

    # Accept valid and verified username and password
    username = ""
    fernet = None
    while True:
        username = raw_input("Username: ")
        if username in users_pass['users']: # if old usr
            index = users_pass['users'].index(username)
            password = raw_input("Password: ")
            if password == (users_pass['passwords'])[index]:
                print("Login successful!\n")
                fernet = handle_old_user(username)
                break
            else:
                print("Incorrect details. Please try again.\n") # Wrong password
        elif username in new_users: # if new user
            s_password = raw_input("Set password: ")
            c_password = raw_input("Confirm password: ")
            if s_password == c_password:
                users_pass['users'].append(username) # add user details to curr users dict
                users_pass['passwords'].append(s_password)
                new_users.remove(username) # not a new user anymore
                print("Password saved and login successful!\n")
                fernet = handle_new_user(username)
                break
            else:
                print("Passwords don't match. Login failed.\n")
        else: # non-existent user
            print("User specified is not currently in the group.\n")

    # start file sharing
    removed_old = GoogleDriveAccess.startSharing(username, fernet, users_pass, new_users)

    # Save users and new users
    save_old_users(users_pass)
    save_new_users(new_users)

    if removed_old:
        print("Changing keys and re-encrypting all files...")
        GoogleDriveAccess.resetDrive()
        print("Re-encryption successful.")


# Reads current user's and passwords file and return a dict with users and pass
def _getCurrUsersPass_():
    """
    Gets the current users and passwords and returns a dictionary with the users and passwords. If file doesn't exist, it creates it with admin's details

    return: dict with users array (accesed by 'users' key) and passwords array (accessed by 'passwords' key)
    """

    # if file doesn't exist, create file with admin details
    if not os.path.exists(USERS_FILE):
        ret = {'users' :["admin"], 'passwords': [ADMIN_PASS]}
        saveFile(USERS_FILE, "admin" + USER_PASS_DELIM + ADMIN_PASS + USER_DELIM)
        return ret

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
    Reads contents of the new user files and gives back an array with new usernames. Create empty file if file doesn't exist

    return: Array with new usernames
    """

    # Create emtpy file if it doesn't exist
    if not os.path.exists(N_USERS_FILE):
        saveFile(N_USERS_FILE, "")
        return []

    # get new user's usernames
    new_users_contents = readFile(N_USERS_FILE)
    new_users = new_users_contents.split(USER_DELIM)

    return new_users[:-1] # ignore last empty element


# Does the initialisation for the new user
def handle_new_user(username):
    """
    Initialisation of a new user. Creates new folder for user files, generates private and public key and saves serialized private key, and also saves the encrypted symmetric key to user's folder, to be decrypted by the user's private key

    param username: username of the new user to be initialised

    return: the fernet
    """

    driveAccess = GoogleDriveAccess(username) # This creates a folder for the user, and also gives access to the drive

    # key pair generation and verification
    priv_key = rsa.generate_private_key(public_exponent = 65537, key_size = 2048, backend = default_backend())
    pub_key = priv_key.public_key()

    # Serialization of private key for file storage
    priv_bytes = priv_key.private_bytes(encoding = serialization.Encoding.PEM, format = serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm = serialization.NoEncryption() )

    # Save serialized private key to user's folder in plaintext
    folder_name = username + "_files/"
    filepath = folder_name + PRIV_KEY_FILE
    saveFile(filepath, priv_bytes)

    # encrypt (using user's pubkey) and save symmetric key to user's folder
    kms = KMS()
    encrypted_sym_key = pub_key.encrypt(kms.key, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
    filepath = folder_name + SHARED_KEY_FILE
    saveFile(filepath, encrypted_sym_key)

    # do what you do for the old user anywyay, and return the fernet it returns
    return handle_old_user(username)


# Gets symmetric key, creates a fernet and returns it
def handle_old_user(username):
    """
    Gets symmetric key using method in KMS. Initialises fernet based on the symmetric key

    param username: username of the old user being handled

    return: fernet
    """

    sym_key = KMS.getKey(username) # get sym key

    fernet = Fernet(sym_key) # create a fernet obj

    return fernet


# Saves all the old users in USERS_FILE
def save_old_users(users_pass):
    """
    Saves the old users to the relevant file, in proper format

    param users_pass: Dictionary containg arrays of old users and passwords

    return: None
    """

    # make content using dictionary and delimiters
    content = ""
    for i in range(len(users_pass['users'])):
        content += users_pass['users'][i] + USER_PASS_DELIM
        content += users_pass['passwords'][i] + USER_DELIM

    # save the file
    saveFile(USERS_FILE, content)


# Saves all the new users to N_USERS_FILE
def save_new_users(users):
    """
    Saves the new users to the relevant file, in proper format

    param users: Array of new users

    return: None
    """

    # make content using array and delimiters
    content = ""
    for i in range(len(users)):
        content += users[i] + USER_DELIM

    # save the file
    saveFile(N_USERS_FILE, content)


# Changes the private and public key of all (old) users except for admin, and also saves the encrypted version of the NEW or CURRENT symmetric key to the user's files
def change_all_keys():
    """
    Changes the private and public key of all (old) users except for admin, and also saves the encrypted version of the NEW or CURRENT symmetric key to the user's files

    return: None
    """

    # reinitialise pirv_pub key pair for all users and save new sym key
    users_pass = _getCurrUsersPass_()
    users = users_pass['users']
    for user in users:
        if user != "admin":
            handle_new_user(user)
