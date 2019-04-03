# author: ShaunJose (@Github)
# File description: Contains methods for file sharing

# Uploads file after encrypting it
def upload_file(filename, fernet):
    """
    Uploads a file named filename to the drive, if the file exists

    param filename: Name of the file to be uploaded
    fernet: The fernet object created in KeyManagementSystem class

    return: Filename of encrypted file, if file uploaded successfully, else None
    """

    # TODO: encrypt file

    # TODO: upload file to google drive

    return None


# Encrypts file
def _encrypt(filename, fernet):
    """
    Encrypts the file named with the filename passed to it

    param filename: File to be encrypted
    fernet: The fernet object created in KeyManagementSystem class

    return: None
    """


# Downloads file and descrypts it
def download_file(filename, fernet):
    """
    Downloads a file named filename from the dirve, if the file exists

    param filename: Name of the file to be downloaded
    fernet: The fernet object created in KeyManagementSystem class

    return: Filename of decrypted file, if file downloaded successfully, else None
    """

    # TODO: download file from google drive

    # TODO: decrypt file

    return None


# Decrypts a file
def _decrypt(filename, fernet):
    """
    Decrypts the encrypted file named with the filename passed to it

    param filename: File to be decrypted
    fernet: The fernet object created in KeyManagementSystem class

    return: None
    """
