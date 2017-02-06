
import logging
import smtplib
from email.mime.text import MIMEText

always_report = False
email_smtp = ''
email_sender = ''
email_passwd = ''
email_subject = ''
email_recipient = ''
email_signature = ''

class Report(object):
	def __init__(self, name, text = None):
		self.name = name
		self.text = text
	
	def addText(self, text):
		if self.text is None:
			self.text = text
		else:
			self.text += text

def sendemail(text):
	logging.info('Sending email.')
	
	full_text = text + '\n' + email_signature
	
	message = MIMEText(full_text, 'plain', 'utf-8')
	message['Subject'] = email_subject
	message['From'] = email_sender
	message['To'] = email_recipient
	
	try:
		server = smtplib.SMTP_SSL(email_smtp)
		server.login(email_sender, email_passwd)
		server.send_message(message)
		server.quit()
	except Exception as ex:
		logging.error('Exception sending email: ' + str(ex))
	
def collate(results):
	logging.info('Collating results.')
	reports = 0
	text = ''
	for r in results:
		text += '\nReport from ' + r.name + ':\n'
		if r.text is None:
			text += 'All quiet.\n'
		else:
			text += r.text
			reports += 1
		
	if reports > 0 or always_report:
		sendemail(text)
	else:
		logging.info('No results to send.')

