# author: ShaunJose (@Github)
# File description: Run this to run project. Accepts user input

# Imports
from KeyManagementSystem import KMS
import FileSharing


# Main method
if __name__ == "__main__":
    # TODO: call method to accept user input here

    # TODO: move all this code (even below it) to appropriate place
    tmp = KMS()
    print(tmp.getKey())

    # filename = FileSharing.upload_file("test file 1.jpg", tmp.fernet)
    # print("\n\nEncrypted version in: " + filename)
    #
    # filename = FileSharing.upload_file("test file 2.txt", tmp.fernet)
    # print("Encrypted version in: " + filename)

    filename = FileSharing.download_file("test file 1.jpg", tmp.fernet)
    print("\n\nDecrypted version in: " + filename)

    filename = FileSharing.download_file("test file 2.txt.encrypt", tmp.fernet)
    print("Decrypted version in: " + filename)
