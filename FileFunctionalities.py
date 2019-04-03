

# Returns the contents of a file
def readFile(filename):
    """
    Reads and returns contents of a file named with the passed filename

    param filename: Name of the file to be read

    return: Contents of file if exists, else None
    """

    # Read file contents
    fileIn = open(filename, "r")
    contents = fileIn.read()
    fileIn.close()

    # return file contents
    return contents


# Creates and saves a file with contents
def saveFile(filename, contents):
    """
    Saves a file with the name in filename, and adds the passed contents to it

    param filename: Name of the file to be created/overwritten
    param contents: Contents that have to be saved to the file

    return: None
    """

    # Create/overwrite file with contents in it
    fileOut = open(filename, "w")
    fileOut.write(contents)
    fileOut.close()
