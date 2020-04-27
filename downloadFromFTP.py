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
			ftp.cwd('Desired_directory')
			print('connected')
			return ftp
		except:
			print('connection failed')
			return ftp

	def downloadFiles(self, ftp):
		file_dict = {}
		os.chdir('directory_to_download')
		for f in ftp.nlst():
			with open(f, 'wb') as fp:
				ftp.retrbinary('RETR ' + f, fp.write)
			print('file ' + f + ' downloaded')
			ftp.delete(f)

	def getEmailRecipients(self,file_path):
		with open(file_path) as myFile:
			for line in myFile:
				if("EMAIL_RECIPIENTS=" in line and not line.startswith('#')):
					pos = line.find('=')
					li = line[pos+1:len(line)-2].split('-t ')
		li.pop(0)
		return li




server = 'server_name'
user = 'username'
password = 'password'
downloadTo = 'path_to_destination_folder'
backup_folder = 'path_to_backup_folder'
file_with_emails = 'path_to_file_with_emails'
file_dict = {}

sender = 'sender@domain'
receiver = 'receiver@domain'

msg = MIMEMultipart()
msg['Subject'] = 'Subject'
msg['From'] = sender
msg['To'] = receiver

text = '''\
<html>
<head>
	<title></title>
</head>
<body aria-readonly='false'>Dear All,<br><br>
Please find attached the files.<br>
'''

for f in Path(downloadTo).iterdir():
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(f, 'rb').read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename=' + f.name)
	msg.attach(part)
	text += 'Attached you can find the downloaded file: ' + f.name + ' <br>'

msg.attach(MIMEText(text,'html'))
smtpObj = smtplib.SMTP('172.22.50.25',25)
smtpObj.sendmail(sender, receiver, msg.as_string())
print("Email sent!\n")


