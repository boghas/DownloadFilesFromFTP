# README #

This is a script that connects to an FTP server in order to download files from server to local.

How it works:

1. First create an FTPServer object
2. Create a connection to the FTP server
3. Download the files from the FTP server using the connection we just created
4. Get the list of the mail recipients

Example on how to run the script:

ftps = FTPServer(server, user, password)
connection = ftps.connect()
ftps.downloadFiles(connection)
recipients = ftps.getEmailRecipients(file_with_emails)

The file_with_emails looks like this:

# Email recipients should be supplied as a list of -t <address>
EMAIL_RECIPIENTS="-t account@domain"