# author: ShaunJose (@Github)
# File description: Run this to run project.

# Imports
from KeyManagementSystem import KMS
from FileSharing import GoogleDriveAccess
from GroupHandler import acceptUser


# Main method
if __name__ == "__main__":

    kms = KMS() # to initialise shared key incase it hasnt been initialised

    acceptUser() # Call method to accept user input here

    print("Goodbye!")
