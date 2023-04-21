import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path

lgr = logging.getLogger(__name__)


class EmailSender(object):
	"""
	Class for sending notification via email
	"""

	@staticmethod
	def send_email(
			recipient_email, subject, message, reply_to, cc=None, bcc=None, from_address='stanoemali87@gmail.com',
			attachment=None, sender='stanoemali87@gmail.com', password='qisiebnrbeudsopr'):
		"""
		Send the Email
		:param recipient_email: the of the recipient
		:param subject: email subject
		:param message: message send
		:param reply_to: corporate email to be replied to
		:param cc: list of any carbon copy recipient
		:param bcc: list of blind copy recipient
		:param from_address: where the email will be coming from
		:param sender: origin of the email
		:param password: email password
		:return: dict with message status
		"""
		try:
			msg = MIMEMultipart()
			msg['From'] = from_address
			msg['Reply-To'] = reply_to
			msg['To'] = recipient_email
			if cc:
				if cc is not list:
					cc = cc.split(",")
				msg['Cc'] = ",".join(cc)
			if bcc:
				if bcc is not list:
					bcc = bcc.split(",")
				msg['Bcc'] = ','.join(bcc)
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = subject
			msg.attach(MIMEText(message, 'html'))
			if recipient_email is not list:
				recipient_email = recipient_email.split(",")
			toaddrs = recipient_email
			if cc:
				toaddrs = toaddrs + cc
			if bcc:
				toaddrs = toaddrs + bcc
			if attachment:
				for f in attachment or []:
					part = MIMEBase('application', "octet-stream")
					with open(f, 'rb') as fil:
						part.set_payload(fil.read())
					encoders.encode_base64(part)
					part.add_header('Content-Disposition', 'attachment; filename={}'.format(Path(f).name))
					msg.attach(part)
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.set_debuglevel(0)
			server.login(sender, password)
			server.sendmail(from_address, toaddrs, msg.as_string())
			server.close()
			return {'status': "success", 'message': 'Email sent successfully'}
		except Exception as e:
			lgr.exception(f"Error during email send of message")
			return {'status': 'failed', 'message': 'Error sending the email: %s' % e}
