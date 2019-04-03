# author: ShaunJose (github username)

# Imports
import os
import constants
from cryptography.fernet import Fernet


# key management system class
class KMS:

    # Constructor
    def __init__(self):
        self.__init_key__()
        print(self.key)


    # Initialises a new key if it doesn't exist
    def __init_key__(self):
        """
        Initialises a new key if it doesn't exist

        return: None
        """

        # read key if key exists else generate a new one
        if os.path.exists(constants.SHARED_KEY_FILE):
            fileRead = open(constants.SHARED_KEY_FILE, "r")
            self.key = fileRead.read()
        else:
            self.__generate_new_key__()


    # Generate and save a key
    def __generate_new_key__(self):
        """
            Generates a new key and saves it to the file

            return: None
        """

        # generate a key
        self.key = Fernet.generate_key()

        # create file-keeping directory if it doesn't exist
        if not os.path.isdir(constants.FOLDER_NAME):
            os.mkdir(constants.FOLDER_NAME)

        # save key to appropraite file in directory
        filepath = open(constants.SHARED_KEY_FILE, "w")
        filepath.write(self.key)
        filepath.close()
