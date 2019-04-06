# author: ShaunJose (@Github)
# File description: Contains class for google drive access and authentication, and methods for file sharing purposes

# Imports
import os
from constants import USER_FILES_FOLDER, ENCR_EXTENSION, DRIVE_FOLDER, DRIVE_ROOT_ID
from FileFunctionalities import readFile, saveFile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Google drive access class
class GoogleDriveAccess:

    # Constructor
    def __init__(self):
        self.googleAuth = GoogleAuth() # init authentication obj
        self.googleAuth.LocalWebserverAuth() # ask user to complete auth, if not already completed
        self.drive = GoogleDrive(self.googleAuth) # init drive obj
        # Create user-files folder here, where all the user's files would be saved (if it doesn't already exist)
        if not os.path.isdir(USER_FILES_FOLDER):
            os.mkdir(USER_FILES_FOLDER)


    # Uploads a file after encrypting it
    def upload_file(self, filename, fernet):
        """
        Saves and uploads an encrypted version of the file named filename, if the file exists locally and no duplicate is on the drive

        param filename: Name of the file to be uploaded
        param fernet: The fernet object created in KeyManagementSystem class

        return: Filename of encrypted file, if file uploaded successfully, else None
        """

        # add path to filename if needed
        filename = GoogleDriveAccess.normaliseFilename(filename)

        # return None if file doesn't exist
        if not os.path.exists(filename):
            print("Error 404: File specified not found")
            return None

        # get the drive's main folder ID
        folderID = self._get_file_ID_(DRIVE_FOLDER, DRIVE_ROOT_ID)

        # Create and share folder on drive if it doesnt exist, and get folderID
        if folderID == None:
            folderID = self.__create_share_folder__()
            print("Created shared folder on drive")

        # Check if file with identical name is already on the drive
        encryptedFilename = filename + ENCR_EXTENSION
        encryptedFileID = self._get_file_ID_(encryptedFilename, folderID)
        if encryptedFileID != None: # implies there's a file identically named
            print("This file is already up on the drive!")
            return None

        # Save encrypted file locally
        plain_text = readFile(filename) # getting file contents
        cipher_text = GoogleDriveAccess._encrypt_(plain_text, fernet)
        saveFile(encryptedFilename, cipher_text) # Saving file locally

        # Upload encrypted file to google drive folder
        fileToUpload = self.drive.CreateFile({"parents": [{"id": folderID}]})
        fileToUpload.SetContentFile(encryptedFilename) # set file contents
        fileToUpload.Upload()

        # TODO: maybe delete local version of encrypted file here
        os.remove("./" + encryptedFilename)

        return encryptedFilename


    # Downloads a file and saves the decrypted version of it
    def download_file(self, filename, fernet):
        """
        Downloads a file named filename from the drive and saves the decrypted version, if the file exists

        param filename: Name of the file to be downloaded
        param fernet: The fernet object created in KeyManagementSystem class

        return: Filename of decrypted file, if file downloaded successfully, else None
        """

        # add encrypt extension if it's not in filename
        if ENCR_EXTENSION not in filename:
            filename = filename + ENCR_EXTENSION

        # If drive's shared folder doesn't exist, return None
        folderID = self._get_file_ID_(DRIVE_FOLDER, DRIVE_ROOT_ID)
        if folderID == None:
            print("Error 404: Shared folder not found on drive")
            return None

        # Return None if file doesnt exist on drive
        fileID = self._get_file_ID_(filename, folderID)
        if fileID == None:
            print("Error 404: File specified does not exist on the drive")
            return None

        # Download encrypted file contents from google drive
        downloadedFile = self.drive.CreateFile({'id': fileID})
        cipher_text = downloadedFile.GetContentString()

        # Get decrypted file data and save decrypted file locally
        plain_text = GoogleDriveAccess._decrypt_(cipher_text.encode('utf-8'), fernet)
        filename = GoogleDriveAccess.normaliseFilename(filename)
        decryptedFilename = filename[ : -len(ENCR_EXTENSION)]
        saveFile(decryptedFilename, plain_text)

        # TODO: maybe open file over here or from caller method
        # NOTE: Filename wont have encrpyt extension

        return decryptedFilename

        return None


    # Gets the file ID of the file specified in the specified parents
    def _get_file_ID_(self, filename, parents):
        """
        Returns the fileID if it exists on the drive in the parents folder

        param filename: name of file to be found
        param parents: Directory in which filename is to be found

        return: id of the file if found in parents, else None
        """

        folderID = None

        # Iterate through files & folders in specified parent, until file/folder needed is found
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % (parents)}).GetList()
        for file in file_list:
            if file['title'] == filename:
                folderID = file['id']
                break

        return folderID


    # creates and shares the shared drive folder
    def __create_share_folder__(self):
        """
        Creates and shares the shared google drive folder to all users in the group

        return: ID of the shared folder on the drive
        """

        folder = self.drive.CreateFile({'title': DRIVE_FOLDER, "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        # TODO: share folder to people (one by one (use another function that adds only one user), so you can use that function to share the folder to a new member added)

        return folder["id"]


    # Encrypts file
    @staticmethod
    def _encrypt_(plain_text, fernet):
        """
        Encrypts the plain_text passed to it

        param plain_text: Data to be encrypted
        param fernet: The fernet object created in KeyManagementSystem class

        return: The encrypted plain_text
        """

        cipher_text = fernet.encrypt(plain_text)
        return cipher_text


    # Decrypts a file
    @staticmethod
    def _decrypt_(cipher_text, fernet):
        """
        Decrypts the cipher_text passed to it

        param cipher_text: Data to be decrypted
        param fernet: The fernet object created in KeyManagementSystem class

        return: The decrypted cipher_text
        """

        plain_text = fernet.decrypt(cipher_text)
        return plain_text


    # Adds folder path to filename if it doesn't already exist
    @staticmethod
    def normaliseFilename(filename):
        """
        Adds folder path to filename if filename doesn't already have it

        param filename: Filename to normalise

        return: Normalized file name
        """

        if USER_FILES_FOLDER not in filename:
            filename = USER_FILES_FOLDER + "/" + filename

        return filename
