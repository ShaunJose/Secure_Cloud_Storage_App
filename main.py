# author: ShaunJose (@Github)
# File description: Run this to run project. Accepts user input

# Imports
from KeyManagementSystem import KMS
from FileSharing import GoogleDriveAccess


# Main method
if __name__ == "__main__":
    # TODO: call method to accept user input here

    # TODO: move all this code (even below it) to appropriate place
    tmp = KMS()
    print(tmp.key)

    driveAccess = GoogleDriveAccess()

    # TODO: initialise group from files or new group if group file doesnt exist

    # filename = driveAccess.upload_file("test file 1.jpg", tmp.fernet)
    # if filename != None:
    #     print("\n\nEncrypted version in: " + filename + " on the drive")
    # else:
    #     print("\n\nUpload failed.")
    #
    # filename = driveAccess.upload_file("test file 2.txt", tmp.fernet)
    # if filename != None:
    #     print("\n\nEncrypted version in: " + filename + " on the drive")
    # else:
    #     print("\n\nUpload failed.")


    filename = driveAccess.download_file("test file 1.jpg", tmp.fernet)
    if filename != None:
        print("\n\nDecrypted version in: " + filename)
    else:
        print("\n\nDonwload failed.")

    filename = driveAccess.download_file("test file 2.txt.encrypt", tmp.fernet)
    if filename != None:
        print("\n\nDecrypted version in: " + filename)
    else:
        print("\n\nDonwload failed.")
