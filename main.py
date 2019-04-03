# author: ShaunJose (@Github)
# File description: Run this to run project. Accepts user input

# Imports
from KeyManagementSystem import KMS
import FileSharing


# Main method
if __name__ == "__main__":
    # TODO: call method to accept user input here

    # TODO: move this code to method described above
    tmp = KMS()
    print(tmp.getKey())

    # TODO: get rid of this temp code
    encr = (FileSharing._encrypt("Test text", tmp.fernet))
    print(encr)
    decr = (FileSharing._decrypt(encr, tmp.fernet))
    print(decr)
