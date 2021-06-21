
import hashlib
import logging
import smtplib
import traceback
from email.mime.text import MIMEText

always_report = False
print_report = False

email_smtp = ''
email_sender = ''
email_passwd = ''
email_subject = ''
email_recipient = ''
email_signature = ''

class Report(object):
    '''
    A class to collect reporting text from agents.
    '''
    
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
    
    digest = hashlib.sha1()
    digest.update(text.encode('utf-8'))
    hexdigest = 'auxo SHA1 ' + digest.hexdigest()
            
    full_text = text + '\n' + email_signature + '\n\n' + hexdigest
    
    message = MIMEText(full_text, 'plain', 'utf-8')
    message['Subject'] = email_subject
    message['From'] = email_sender
    message['To'] = email_recipient
    
    try:
        server = smtplib.SMTP_SSL(email_smtp)
        server.login(email_sender, email_passwd)
        server.send_message(message)
        server.quit()
    except Exception:
        logging.error('Exception sending email: ' + traceback.format_exc())
    
def plain_text(results):
    reports = 0
    text = ''
    for r in results:
        text += '\nReport from ' + r.name + ':\n'
        if r.text is None:
            text += 'All quiet.\n'
        else:
            text += r.text
            reports += 1
        
    return (reports, text)

def write_html(filename, html):
    with open(filename, 'w') as file:
        file.write(html)
        logging.info('HTML results file written.')

def html_formatted(results):
    text = '<html><head><title>Auxo Status</title></head><body>\n'
    for r in results:
        text += '<h2>Report from ' + r.name + '</h2>\n'
        if r.text is None:
            text += '<pre>All quiet.</pre>\n'
        else:
            text += '<pre>' + r.text + '</pre>\n'

    text += '</body></html>\n'

    return text

def collate(results):
    '''
    Function to collect the text from a list of reports. If there is at least one
    non-empty report then an email is sent to the configured recipient.
    '''
    logging.info('Collating results.')

    if len(html_report) > 0:
        write_html(html_report, html_formatted(results))
    else:
        (reports, text) = plain_text(results)

        if reports > 0 or always_report:
            if print_report:
                print(text)
            else:
                sendemail(text)
        else:
            logging.info('No results to send.')

