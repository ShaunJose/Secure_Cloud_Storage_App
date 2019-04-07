# author: ShaunJose (@Github)
# File description: Contains the KeyManagementSystem class

# Imports
import os
from constants import LOCAL_FOLDER, SHARED_KEY_FILE
from FileFunctionalities import readFile, saveFile
from cryptography.fernet import Fernet


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
        if os.path.exists(SHARED_KEY_FILE):
            self.key = readFile(SHARED_KEY_FILE)
            self.fernet = Fernet(self.key) # create fernet obj
        else:
            # TODO: if it's not admin, do I generate key or get key from admin?
            self.__generate_new_key__()


    # Generate and save a key
    def __generate_new_key__(self):
        """
        Generates a new key (and fernet obj) and saves it to the file

        return: None
        """

        # generate a key
        self.key = Fernet.generate_key()

        # create file-keeping directory if it doesn't exist
        if not os.path.isdir(LOCAL_FOLDER):
            os.mkdir(LOCAL_FOLDER)

        # save key to appropriate file in directory
        saveFile(SHARED_KEY_FILE, self.key)

        # create fernet object
        self.fernet = Fernet(self.key) # create fernet obj

        # TODO: broadcast the new key to everyone (here or in group handler class?)

        # TODO: Donwload, Re encrypt all files with new key, and upload if any files exist on the drive. Also delete all previous files on drive after downloaded (in group handler class)

    #
    # # Returns the symmetric key
    # def getKey(self):
    #     """
    #     Returns the symmetric key to the caller
    #
    #     return: Symmetric key
    #     """
    #
    #     return self.key
