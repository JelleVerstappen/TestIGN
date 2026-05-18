import ftplib
from StringIO import StringIO


def establishFtpConnection(ftpHost, ftpPort, ftpUname, ftpPass, passive):
    """
    Establishes an FTP connection.

    Args:
        ftpHost (str): FTP server hostname.
        ftpPort (int): FTP server port.
        ftpUname (str): FTP username.
        ftpPass (str): FTP password.
        passive (bool): Whether to use passive mode.

    Returns:
        ftplib.FTP: FTP connection object.
    """
    ftp = ftplib.FTP()
    ftp.connect(ftpHost, ftpPort)
    ftp.login(ftpUname, ftpPass)
    ftp.set_pasv(passive)
    return ftp


def uploadToFtp(ftp, sourceFile, newFileName):
    """
    Uploads a file to an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
        sourceFile (str): Local file to upload.
        newFileName (str): Remote file name on the server.
    """
    if not isinstance(ftp, ftplib.FTP):
        raise ValueError("Invalid FTP connection object")

    with open(sourceFile, 'rb') as binaryFile:
        ftp.storbinary(newFileName, binaryFile)


def uploadDatasetAsCsvToFtp(ftp, dataset, fileName):
    """
    Uploads a dataset as a CSV file to an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
        dataset: The input dataset.
        fileName (str): The name to use for the uploaded CSV file.
    """
    spreadsheet = system.dataset.toCSV(dataset)
    tempFile = system.file.getTempFile("csv")
    system.file.writeFile(tempFile, spreadsheet)
    remoteFileName = fileName + '.csv'
    uploadToFtp(ftp, tempFile, remoteFileName)


def uploadDatasetAsXlsToFtp(ftp, dataset, fileName):
    """
    Uploads a dataset as an Excel file to an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
        dataset: The input dataset.
        fileName (str): The name to use for the uploaded Excel file.
    """
    spreadsheet = system.dataset.dataSetToExcel(1, [dataset], 1)
    tempFile = system.file.getTempFile("xls")
    system.file.writeFile(tempFile, spreadsheet)
    remoteFileName = fileName + '.xls'
    uploadToFtp(ftp, tempFile, remoteFileName)


def downloadBinaryFromFtp(ftp, filename, remotePath):
    """
    Downloads a binary file from an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
        filename (str): Name of the file to download.
        remotePath (str): Path on the server where the file is located.

    Returns:
        str: The binary data of the downloaded file.
    """
    if not isinstance(ftp, ftplib.FTP):
        raise ValueError("Invalid FTP connection object")

    binaryData = StringIO()
    ftp.cwd(remotePath)
    ftp.retrbinary('RETR ' + filename, binaryData.write)
    return binaryData.getvalue()


def deleteFileOnFtp(ftp, filename, remotePath):
    """
    Deletes a file on an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
        filename (str): Name of the file to delete.
        remotePath (str): Path on the server where the file is located.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    if not isinstance(ftp, ftplib.FTP):
        raise ValueError("Invalid FTP connection object")

    ftp.cwd(remotePath)
    deleted = ftp.delete(filename)
    ftp.quit()
    return deleted


def getFilesInDirectoryOnFtp(ftp, remotePath):
    """
    Gets a list of files in a directory on an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
        remotePath (str): Path on the server where the directory is located.

    Returns:
        list: A list of filenames in the specified directory.
    """
    if not isinstance(ftp, ftplib.FTP):
        raise ValueError("Invalid FTP connection object")

    fileList = StringIO()
    ftp.cwd(remotePath)
    ftp.retrlines('NLST', fileList.write)
    return fileList.getvalue()


def disconnectFtp(ftp):
    """
    Disconnects from an FTP server.

    Args:
        ftp (ftplib.FTP): FTP connection object.
    """
    try:
        ftp.quit()
    except ftplib.Error, e:
    	### TODO: implementeer fatsoenlijke error afhandeling
        if isinstance(e, ftplib.error_perm):
            print("Error during quit: %s" % e)
            # Handle specific FTP permission error
        elif isinstance(e, ftplib.error_reply):
            print("Error during quit: %s" % e)
            # Handle specific FTP reply error
        elif isinstance(e, ftplib.error_temp):
            print("Error during quit: %s" % e)
            # Handle specific FTP temporary error
        elif isinstance(e, ftplib.error_proto):
            print("Error during quit: %s" % e)
            # Handle specific FTP protocol error
        else:
            print("Other error during quit: %s" % e)
            # Handle other exceptions
    
    # Close the connection regardless
    ftp.close()

