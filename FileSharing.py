# author: ShaunJose (@Github)
# File description: Contains methods for file sharing

# Imports
import os
from constants import ENCR_EXTENSION

# Uploads file after encrypting it
def upload_file(filename, fernet):
    """
    Uploads a file named filename to the drive, if the file exists

    param filename: Name of the file to be uploaded
    fernet: The fernet object created in KeyManagementSystem class

    return: Filename of encrypted file, if file uploaded successfully, else None
    """

    # return None if file doesn't exist
    if not os.path.exists(filename):
        return None

    # TODO: Read file

    # TODO: encrypt data from file

    # TODO: save file locally
    # NOTE: Filename should have encrpyt extension

    # TODO: upload file to google drive



# Encrypts file
def _encrypt(plain_text, fernet):
    """
    Encrypts the plain_text passed to it

    param plain_text: Data to be encrypted
    fernet: The fernet object created in KeyManagementSystem class

    return: Encrypted plain_text
    """

    cipher_text = fernet.encrypt(plain_text)
    return cipher_text


# Downloads file and descrypts it
def download_file(filename, fernet):
    """
    Downloads a file named filename from the drive, if the file exists

    param filename: Name of the file to be downloaded
    fernet: The fernet object created in KeyManagementSystem class

    return: Filename of decrypted file, if file downloaded successfully, else None
    """

    # TODO: return None if file doesnt exist on drive

    # TODO: download file from google drive

    # TODO: decrypt file

    # TODO: maybe open file over here or from caller method
    # NOTE: Filename wont have encrpyt extension

    return None


# Decrypts a file
def _decrypt(cipher_text, fernet):
    """
    Decrypts the cipher_text passed to it

    param cipher_text: Data to be decrypted
    fernet: The fernet object created in KeyManagementSystem class

    return: Decrypted cipher_text
    """

    plain_text = fernet.decrypt(cipher_text)
    return plain_text
