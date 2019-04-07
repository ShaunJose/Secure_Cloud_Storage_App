# author: ShaunJose (@Github)
# File description: Contains class for google drive access and authentication, and methods for file sharing purposes

# Imports
import os
from constants import ENCR_EXTENSION, DRIVE_FOLDER, DRIVE_ROOT_ID, INSTR_UP, INSTR_DOWN, INSTR_ADD, INSTR_REM, INSTR_EXIT
from FileFunctionalities import readFile, saveFile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Google drive access class
class GoogleDriveAccess:

    # Constructor
    def __init__(self, username):
        self.googleAuth = GoogleAuth() # init authentication obj
        self.googleAuth.LocalWebserverAuth() # ask user to complete auth, if not already completed
        self.drive = GoogleDrive(self.googleAuth) # init drive obj
        # Create user-files folder here, where all the user's files would be saved (if it doesn't already exist)
        # TODO: change USER_FILES_FOLDER to self.user_folder = username_files
        self.user_folder = username + "_files"
        if not os.path.isdir(self.user_folder):
            os.mkdir(self.user_folder)


    # Uploads a file after encrypting it
    def upload_file(self, filename, fernet):
        """
        Saves and uploads an encrypted version of the file named filename, if the file exists locally and no duplicate is on the drive

        param filename: Name of the file to be uploaded
        param fernet: The fernet object created in KeyManagementSystem class

        return: Filename of encrypted file, if file uploaded successfully, else None
        """

        # add path to filename if needed
        prevFilename = filename
        filename = self.normaliseFilename(filename)

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
        encryptedFilename = prevFilename + ENCR_EXTENSION
        encryptedFileID = self._get_file_ID_(encryptedFilename, folderID)
        if encryptedFileID != None: # implies there's a file identically named
            print("This file is already up on the drive!")
            return None

        # Save encrypted file locally
        plain_text = readFile(filename) # getting file contents
        cipher_text = GoogleDriveAccess._encrypt_(plain_text, fernet)
        normEncryptedFilename = encryptedFilename
        normEncryptedFilename = self.normaliseFilename(normEncryptedFilename)
        saveFile(normEncryptedFilename, cipher_text) # Saving file locally

        # Upload encrypted file to google drive folder
        fileToUpload = self.drive.CreateFile({"title": encryptedFilename, "parents": [{"id": folderID}]})
        fileToUpload.SetContentFile(normEncryptedFilename) # set file contents
        fileToUpload.Upload()

        # Delete local version of encrypted file here
        os.remove(normEncryptedFilename)

        return encryptedFilename


    # Downloads a file and saves the decrypted version of it
    def download_file(self, filename, fernet):
        """
        Downloads a file named filename from the drive and saves the decrypted version, if the file exists

        param filename: Name of the file to be downloaded
        param fernet: The fernet object created in KeyManagementSystem class

        return: Filename of decrypted file, if file downloaded successfully, else None
        """

        # Add encrypt extension if it's not in filename
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
        filename = self.normaliseFilename(filename)
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

        fileID = None

        # Iterate through files & folders in specified parent, until file/folder needed is found
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % (parents)}).GetList()
        for file in file_list:
            if file['title'] == filename:
                fileID = file['id']
                break

        return fileID


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


    # Adds folder path to filename if it doesn't already exist
    def normaliseFilename(self, filename):
        """
        Adds folder path to filename if filename doesn't already have it

        param filename: Filename to normalise

        return: Normalized file name
        """

        if self.user_folder not in filename:
            filename = self.user_folder + "/" + filename

        return filename


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


    # Simulates file sharing for a user
    @staticmethod
    def startSharing(username, fernet):

        GoogleDriveAccess.printInstructions(False) #print instructions to the user

        # accept user input
        exit = False
        driveAccess = GoogleDriveAccess(username)
        while not exit:
            userIn = raw_input(INSTR_EXIT)
            if userIn == "e":
                exit = True
            elif len(userIn) > 7 and userIn[0:7] == "upload ":
                filename = driveAccess.upload_file(userIn[7:], fernet)
                if filename != None:
                    print("\n\nEncrypted version in: " + filename + " on the drive")
                else:
                    print("\n\nUpload failed.")
            elif len(userIn) > 9 and userIn[0:9] == "download ":
                filename = driveAccess.download_file(userIn[9:], fernet)
                if filename != None:
                    print("\n\nDecrypted version saved in: " + filename)
                else:
                    print("\n\nDonwload failed.")
            else:
                print("Invalid input. Please try again")


    # Prints the instructions for file sharing
    @staticmethod
    def printInstructions(adminInstructions):
        """
        Prints the instructions for filesharing

        param adminInstructions: True to print add and remove user messages, keep False otherwise

        return: None
        """

        if adminInstructions:
            print(INSTR_ADD)
            print(INSTR_REM)

        print(INSTR_UP)
        print(INSTR_DOWN)
