from django.conf import settings
from basics.models import Organization
from django.shortcuts import HttpResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def get_email_server_config():
    organization = Organization.objects.first()  # retrieve the first organization (assuming there's only one)
    if organization:
        return {
            'DEFAULT_FROM_EMAIL': organization.email,
            'EMAIL_HOST_USER': organization.email,
            'EMAIL_HOST_PASSWORD': organization.password,
        }
    else:
        return {}  # return an empty dictionary if no organization is found

def send_email(subject, message, to_email):
    # Use the email server config to send the email
    email_config = get_email_server_config()
    if email_config:
        from_email = email_config['DEFAULT_FROM_EMAIL']
        email_host_user = email_config['EMAIL_HOST_USER']
        email_host_password = email_config['EMAIL_HOST_PASSWORD']
        # Send the email using the email server config
        # Create the email message
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Send the email using SMTP
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(email_host_user, email_host_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    else:
        print("No email server config found")

def send_email_with_attachment(email, pdf_file):
    if email and pdf_file:
        subject = 'PDF File Attachment'
        message = 'Please find the attached PDF file.'

        # Create the email message with attachment
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = 'your_from_email@example.com'
        msg['To'] = email

        # Attach the PDF file
        attachment = MIMEApplication(pdf_file.read())
        attachment['Content-Disposition'] = f'attachment; filename={pdf_file.name}'
        msg.attach(attachment)

        # Add the message body
        msg.attach(MIMEText(message))

        # Send the email using the send_email method
        send_email(subject, msg.as_string(), email)

        return HttpResponse('Email sent successfully!')
    else:
        return HttpResponse('Invalid request. Please provide an email and a PDF file.')
    