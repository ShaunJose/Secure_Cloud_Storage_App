# author: ShaunJose
# File description: Handles the group (including accepting user login, user additon and deletion etc)


# Imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from constants import USERS_FILE, N_USERS_FILE, USER_DELIM, USER_PASS_DELIM, PRIV_KEY_FILE, SHARED_KEY_FILE
from FileSharing import GoogleDriveAccess
from FileFunctionalities import readFile, saveFile
from KeyManagementSystem import KMS

# Accepts a user log in
def acceptUser():

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


    GoogleDriveAccess.startSharing(username, fernet)
    # kms = KMS()
    # driveAccess = GoogleDriveAccess(username)
    # filename = driveAccess.upload_file("test file 1.jpg", kms.fernet)
    # if filename != None:
    #     print("\n\nEncrypted version in: " + filename + " on the drive")
    # else:
    #     print("\n\nUpload failed.")
    # filename = driveAccess.download_file("test file 1.jpg", kms.fernet)
    # if filename != None:
    #     print("\n\nDecrypted version in: " + filename)
    # else:
    #     print("\n\nDonwload failed.")
    # TODO: Program startoff (File sharing?)

    # TODO: after program has ended, call methods to save users and new users


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

    # Verification #NOTE
    # message = b"A message I want to sign"
    # signature = priv_key.sign(message, padding.PSS( mgf=padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256() )
    # pub_key.verify(signature, message, padding.PSS( mgf=padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256() )

    # Serialization of private key for file storage
    priv_bytes = priv_key.private_bytes(encoding = serialization.Encoding.PEM, format = serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm = serialization.NoEncryption() )

    # Save serialized private key to user's folder in plaintext
    folder_name = username + "_files/"
    filepath = folder_name + PRIV_KEY_FILE
    saveFile(filepath, priv_bytes)

    # getting priv key from the file and verifying it again #NOTE
    # loaded_priv_key = serialization.load_pem_private_key(readFile(filepath), password = None, backend = default_backend())
    # signature = something.sign(message, padding.PSS( mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256() )
    # pub_key.verify(signature, message, padding.PSS( mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256() )

    # encrypt (using user's pubkey) and save symmetric key to user's folder
    kms = KMS()
    encrypted_sym_key = pub_key.encrypt(kms.key, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
    filepath = folder_name + SHARED_KEY_FILE
    saveFile(filepath, encrypted_sym_key)

    # Printing symmetric key and decrypted symmetric key to confirm that the're the exact same #NOTE: delete
    # print(kms.key)
    # print(priv_key.decrypt(readFile(filepath), padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)))

    # Reading the symmetric from the file and decrypting it
    # NOTE: both
    sym_key = KMS.getKey(username)
    print(kms.key)
    print(sym_key)
    fernet = Fernet(sym_key)

    return fernet


# Gets symmetric key, creates a fernet and returns it
def handle_old_user(username):

    sym_key = KMS.getKey(username) # get sym key

    fernet = Fernet(sym_key) # create a fernet obj

    return fernet
