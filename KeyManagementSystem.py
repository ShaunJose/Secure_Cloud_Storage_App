# author: ShaunJose (@Github)
# File description: Contains the KeyManagementSystem class

# Imports
import os
from constants import ADMIN_FOLDER, SHARED_KEY_FILE, PRIV_KEY_FILE
from FileFunctionalities import readFile, saveFile
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


# key management system class
class KMS:

    # Constructor
    def __init__(self):
        self.__init_key_fernet__() # initialise self.key and self.fernet


    # Initialises a new key if it doesn't exist
    def __init_key_fernet__(self):
        """
        Initialises a new key if it doesn't exist

        return: None
        """

        # read key if key exists else generate a new one
        if os.path.exists(ADMIN_FOLDER + "/" + SHARED_KEY_FILE):
            self.key = readFile(ADMIN_FOLDER + "/" + SHARED_KEY_FILE)
            self.fernet = Fernet(self.key) # create fernet obj
        else:
            self.__generate_new_key__()


    # Generate and save a key
    def __generate_new_key__(self):
        """
        Generates a new key (and fernet obj) and saves it to the file

        return: None
        """

        # generate a key
        self.key = Fernet.generate_key()

        # create admin's directory if it doesn't exist
        if not os.path.isdir(ADMIN_FOLDER):
            os.mkdir(ADMIN_FOLDER)

        # save key to appropriate file in admin's directory
        saveFile(ADMIN_FOLDER + "/" + SHARED_KEY_FILE, self.key)

        # create fernet object
        self.fernet = Fernet(self.key) # create fernet obj

        # TODO: broadcast the new key to everyone (here or in group handler class?)

        # TODO: Donwload, Re encrypt all files with new key, and upload if any files exist on the drive. Also delete all previous files on drive after downloaded (in group handler class)


    # Returns the symmetric key of the group
    @staticmethod
    def getKey(username):
        """
        Returns the symmetric key to the caller

        param username: User's who's folder has to be dealt with and read into

        return: Symmetric key
        """

        sym_key = None
        if username != "admin":
            # Read private key of user
            folder_name = username + "_files/"
            filepath = folder_name + PRIV_KEY_FILE
            priv_key = serialization.load_pem_private_key(readFile(filepath), password = None, backend = default_backend())

            # Read symmetric key
            filepath = folder_name + SHARED_KEY_FILE
            sym_key = priv_key.decrypt(readFile(filepath), padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
        else: # if it's the admin, it's already stored in plaintext
            sym_key = readFile(ADMIN_FOLDER + "/" + SHARED_KEY_FILE)

        return sym_key
