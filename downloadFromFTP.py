import os
import io
import ftplib
import shutil
import smtplib
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class FTPServer(object):
	def __init__(self, server, user, password):
		self.server = server
		self.user = user 
		self.password = password

	def connect(self):
		try:
			ftp = ftplib.FTP(self.server)
			ftp.login(self.user, self.password)
			ftp.cwd('SRS_EFT_FILES')
			print('connected')
			return ftp
		except:
			print('connection failed')
			return ftp

	def downloadFiles(self, ftp):
		file_dict = {}
		os.chdir('C:\\Users\\bogdan.hasan\\Desktop\\pyDBTEST\\KSH scripting\\files\\')
		for f in ftp.nlst():
			with open(f, 'wb') as fp:
				ftp.retrbinary('RETR ' + f, fp.write)
			print('file ' + f + ' downloaded')
			ftp.delete(f)

	def getEmailRecipients(self,file_path):
		with open(file_path) as myFile:
			for line in myFile:
				if("SRS_EFT_EMAIL_RECIPIENTS=" in line and not line.startswith('#')):
					pos = line.find('=')
					li = line[pos+1:len(line)-2].split('-t ')
		li.pop(0)
		return li


# First create an FTPServer object
# Create a connection to the FTP server
# Download the files from the FTP server
# Using the connection we just created
# Get the list of the mail recipients
'''
ftps = FTPServer(server, user, password)
connection = ftps.connect()
ftps.downloadFiles(connection)
recipients = ftps.getEmailRecipients(file_with_emails)
'''

server = 'transfer.dufry.com'
user = 'ftp_uk_fi_sap'
password = 'Chained_42m7'
downloadTo = 'D:\\DIPDATA\\EFT File Transfer\\files\\'
backup_folder = 'D:\\DIPDATA\\EFT File Transfer\\bckup\\'
file_with_emails = 'D:\\DIPDATA\\EFT File Transfer\\files\\\\text.txt'
file_dict = {}

sender = 'ops@6k3.dufry.com'
receiver = 'bogdan.hasan@mindit.io'

msg = MIMEMultipart()
msg['Subject'] = 'EFT files'
msg['From'] = sender
msg['To'] = receiver

text = '''\
<html>
<head>
	<title></title>
</head>
<body aria-readonly='false'>Dear All,<br><br>
Please find attached the Consolidated and Summary EFT files.<br>
'''

for f in Path(downloadTo).iterdir():
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(f, 'rb').read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename=' + f.name)
	msg.attach(part)
	text += 'Attached you can find the EFT file ' + f.name + ' <br>'

msg.attach(MIMEText(text,'html'))
smtpObj = smtplib.SMTP('172.22.50.25',25)
smtpObj.sendmail(sender, receiver, msg.as_string())
print("Email with reconciliation files sent!\n")
'''
for path in Path(downloadTo).iterdir():
	try:
		shutil.move(str(path), backup_folder)
		print('file ' + path.name + " moved to backup folder")
	except:
		print('file ' + path.name + " failed to be moved to backup folder")
'''

