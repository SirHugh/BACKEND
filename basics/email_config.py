from django.conf import settings
from basics.models import Organization
from django.shortcuts import HttpResponse
import smtplib
from email.mime.text import MIMEText

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
