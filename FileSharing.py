# author: ShaunJose (@Github)
# File description: Contains methods for file sharing purposes

# Imports
import os
from constants import ENCR_EXTENSION


# Uploads a file after encrypting it
def upload_file(filename, fernet):
    """
    Saves and uploads an encrypted version of the file named filename, if the file exists

    param filename: Name of the file to be uploaded
    fernet: The fernet object created in KeyManagementSystem class

    return: Filename of encrypted file, if file uploaded successfully, else None
    """

    # return None if file doesn't exist
    if not os.path.exists(filename):
        return None

    # Read file
    fileIn = open(filename, "r")
    plain_text = fileIn.read()
    fileIn.close()

    # Get encrypted file data
    cipher_text = _encrypt(plain_text, fernet)

    # Save file locally
    EncryptedFilename = filename + ENCR_EXTENSION
    fileOut = open(EncryptedFilename, "w")
    fileOut.write(cipher_text)
    fileOut.close()

    # TODO: upload file to google drive

    # TODO: maybe delete local version of encrypted file here

    return EncryptedFilename


# Encrypts file
def _encrypt(plain_text, fernet):
    """
    Encrypts the plain_text passed to it

    param plain_text: Data to be encrypted
    fernet: The fernet object created in KeyManagementSystem class

    return: The encrypted plain_text
    """

    cipher_text = fernet.encrypt(plain_text)
    return cipher_text


# Downloads a file and saves the decrypted version of it
def download_file(filename, fernet):
    """
    Downloads a file named filename from the drive and saves the decrypted version, if the file exists

    param filename: Name of the file to be downloaded
    fernet: The fernet object created in KeyManagementSystem class

    return: Filename of decrypted file, if file downloaded successfully, else None
    """

    # add encrypt extension if it's not in filename
    if ENCR_EXTENSION not in filename:
        filename = filename + ENCR_EXTENSION

    # TODO: return None if file doesnt exist on drive

    # TODO: download file from google drive

    # Read file
    fileIn = open(filename, "r")
    cipher_text = fileIn.read()
    fileIn.close()

    # TODO: maybe delete downloaded encrypted version of the file here.

    # Get decrypted file data
    plain_text = _decrypt(cipher_text, fernet)

    # Save decrypted data here
    DecryptedFileName = filename[ : -len(ENCR_EXTENSION)]
    fileOut = open(DecryptedFileName, "w")
    fileOut.write(plain_text)
    fileOut.close()

    # TODO: maybe open file over here or from caller method
    # NOTE: Filename wont have encrpyt extension

    return DecryptedFileName

    return None


# Decrypts a file
def _decrypt(cipher_text, fernet):
    """
    Decrypts the cipher_text passed to it

    param cipher_text: Data to be decrypted
    fernet: The fernet object created in KeyManagementSystem class

    return: The decrypted cipher_text
    """

    plain_text = fernet.decrypt(cipher_text)
    return plain_text
