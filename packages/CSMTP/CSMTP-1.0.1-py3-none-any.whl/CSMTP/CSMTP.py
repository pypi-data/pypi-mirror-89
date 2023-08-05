# Importing essential resources
import smtplib
from email.message import EmailMessage
import os
import imghdr

from validate_email import validate_email


class CMP:

    def __init__(self, sender_mail='', password='', mailhost='localhost', mailport=465):
        # Setting up mail server and port
        self.mailhost = mailhost
        self.mailport = mailport

        # Setting up the sender email and pass
        self.sender_mail = sender_mail if sender_mail else os.environ['CSMTP_MAIL']
        self.password = password if password else os.environ['CSMTP_PASS']

        # Checking if the sender mail info is not left empty
        if self.sender_mail is None or self.password is None:
            raise Exception('Missing information: check "sender_mail" or the "password ')

    def _localhost_server(self, subject='', body=''):
        """
        Sending mails to localhost
        :argument::subject: the subject of the mail
        :argument::body: the body of the mail
        ::argument::port: the port of the DebuggingServer
        """

        # Sending mail to the localhost
        with smtplib.SMTP(self.mailhost, self.mailport) as server:
            message = f"Subject:{subject} \n\n{body}"
            return server.sendmail(self.mailhost, self.mailhost, message)

    def _smtp_server(self, msg):
        """
        sends actual mail via ssl connection
        :argument::msg: EmailMessage object with proper values for send_message method
        """
        # Testing if emails are valid
        emails = [msg['To'], msg['From']]
        for email in emails:
            if validate_email(email):
                continue
            else:
                raise ValueError(f'{email} is an invalid email')

        # Sending mail to receiver
        try:
            # Creating an encryption
            context = smtplib.ssl.create_default_context()

            # Sending the mail
            with smtplib.SMTP_SSL(host=self.mailhost, port=self.mailport, context=context) as smtp:
                # Logging in the account
                smtp.login(self.sender_mail, self.password)

                # Sending msg
                return smtp.send_message(msg)

        except (smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused) as error:
            print(error)

    def send_simple_msg(self, receiver, subject='', body=''):
        """
        sends a simple text message to the receiver
        :argument::receiver: the email of the receiver of the  mail
        :argument::subject: the subject of the mail
        :argument::body: the body of the mail
        """

        # Creating an instance of an EmailMessage class
        msg = EmailMessage()

        # Setting up credential info
        msg['From'] = self.sender_mail
        msg['To'] = receiver if type(receiver) == str else ', '.join(receiver)

        # Setting up the body and subject
        msg['Subject'] = subject
        msg.set_content(body)

        # Assigning message to appropriate method
        if self.mailhost == "localhost":
            return self._localhost_server(subject=subject, body=body)
        else:
            return self._smtp_server(msg)

    def send_html(self, receiver, html_string, subject='', body=''):
        """
        Sends html text to receiver, the text will load like a website on the mail
        :argument::receiver: the email of the receiver of the  mail
        :argument::subject: the subject of the mail
        :argument::body: the body of the mail
        :argument::html_string: the html string you wish to send
        """

        # Creating an instance of an EmailMessage class
        msg = EmailMessage()

        # Setting up credential info
        msg['From'] = self.sender_mail
        msg['To'] = receiver if type(receiver) == str else ', '.join(receiver)

        # Setting up the body and subject
        msg['Subject'] = subject
        msg.set_content(body)

        # Setting up the html file
        msg.add_alternative(html_string, subtype="html")

        # Sending message
        if self.mailhost == 'localhost':
            return self._localhost_server(subject=subject, body=body)

        else:
            return self._smtp_server(msg)

    def send_special(self, receiver, file_dir, maintype='image', subject='', body=''):
        """
        Send email with attachments
        :argument::receiver: the email of the receiver of the  mail
        :argument::subject: the subject of the mail
        :argument::body: the body of the mail
        :argument::file_dir: list of directories to same type of file
        :argument::maintype:  type of file to be sent
        """

        # Creating an instance of an EmailMessage class
        msg = EmailMessage()

        # Setting up credential info
        msg['From'] = self.sender_mail
        msg['To'] = receiver if type(receiver) == str else ', '.join(receiver)

        # Setting up the body and subject
        msg['Subject'] = subject
        msg.set_content(body)

        # setting up essential variables
        maintype = maintype if maintype == "image" else 'application'

        # Ensuring the file_dir argument is a list
        file_dir = file_dir if type(file_dir) == list else file_dir.split(',')

        for file in file_dir:
            # Opening the file
            with open(file, 'rb') as file:
                # Getting the file data
                file_data = file.read()

                # Getting the subtype of file
                subtype = imghdr.what(file.name) if maintype == 'image' else 'octet_stream'

                # Adding attachment
                msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file.name)

        else:
            # Send email
            if self.mailhost == 'localhost':
                return self._localhost_server(subject=subject, body=body)

            else:
                return self._smtp_server(msg)

