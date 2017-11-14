import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class cfg:
    # TODO: change email to ours
    email_serverhost = 'email-smtp.us-east-1.amazonaws.com'
    email_account = "service@sinyi-tech.com"
    email_password = "Rogu5219"

    email_serverhost = 'derickson99.dotster.com'
    email_account = "support@gotrackster.com"
    email_password = "Paradigm2@"

class Email():
    def __init__(self):
        self.serverhost = cfg.email_serverhost
        self.account = cfg.email_account
        self.psw = cfg.email_password
        self.server = smtplib.SMTP(self.serverhost, 587)
        self.server.starttls()
        self.server.login(self.account, self.psw)
        self.to_email = None

class CloudesignEmail(Email):
    def set(self,sendAccount,subject,html):
        """
        set account
        :param account:
        :return:
        """
        #title
        email_from = formataddr(('Cloudesign Service', self.account))
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = sendAccount
        self.sendAccount=sendAccount

        #content
        p1 = MIMEText(html, 'html')
        msg.attach(p1)
        self.msg = msg.as_string()

    def _send(self):
        try:
            self.server.sendmail(self.account, self.sendAccount, self.msg)
            self.server.quit()
            return True
        except Exception as e:
            print(str(e))
            return False
    def sending(self):

        self._send()

if __name__ == '__main__':

    e=CloudesignEmail()
    e.set("meatball0520@gmail.com","testing123","this is mesg")
    e.sending()