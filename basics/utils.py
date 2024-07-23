from .models import Organization

def get_email_server_config():
    organization = Organization.objects.first()  # retrieve the first organization (assuming there's only one)
    if organization:
        return {
            'DEFAULT_FROM_EMAIL': organization.email, 
            'EMAIL_HOST_PASSWORD': organization.password, 
        }
    else:
        return {}  # return an empty dictionary if no organization is found