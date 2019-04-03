# author: ShaunJose (github username)

# Imports
import os
import constants
from cryptography.fernet import Fernet


# key management system class
class KMS:

    # Constructor
    def __init__(self):
        self.__generate_new_key__()


    # Generate and save a key
    def __generate_new_key__(self):
        """
            Generates a new key and saves it to the file

            return: None
        """

        # generate a key
        self.key = Fernet.generate_key()

        # save generated key to file in proper directory
        if not os.path.isdir(constants.FOLDER_NAME):
            os.mkdir(constants.FOLDER_NAME)

        
