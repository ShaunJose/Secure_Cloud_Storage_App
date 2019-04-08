# Name of the admin's folder
ADMIN_FOLDER = "admin_files"

# File name where the symmetric key is saved
SHARED_KEY_FILE = "Shared Key"

# Make encrypted file and descrypted extensions
ENCR_EXTENSION = ".encrypt"

# Google drive folder name where all encrypted files will be saved online
DRIVE_FOLDER = "Secure Cloud Storage"

# Id of the root folder on drive
DRIVE_ROOT_ID = "root"

# Name of file where User names and passwords are saved
USERS_FILE = "Users.txt"

# Name of file where new users are saved
N_USERS_FILE = "newUsers.txt"

# Delimiter between users in files
USER_DELIM = "\n\n"

# Delimiter between user and user's password in files
USER_PASS_DELIM = "\n"

# Delimiter between private and public keys
KEY_DELIM = "\n\n\n\n"

# Private key file name for each user
PRIV_KEY_FILE = "Private Key"

# Test message for signature verification
TEST_MSG = b"Just a test message, not like the usual one but not unique either."

# Instructions for user input (upload, download, add user, remove user)
INSTR_UP = "To upload a file to the drive, type upload filename (with extension). Make sure the file is in your user folder"
INSTR_DOWN = "To download a file from the drive, type download filename (with extension)"
INSTR_ADD = "To add a user, type add username"
INSTR_REM = "To remove a user, type remove username"
INSTR_EXIT = "Enter e to exit, or continue file sharing\n"
