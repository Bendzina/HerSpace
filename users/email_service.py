# users/email_service.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verification_email(user, token, request):
    verification_url = f"{request.scheme}://{request.get_host()}/api/users/auth/verify-email/{token}/"
    
    subject = 'Verify Your Email - HerSpace'
    message = f'Please click the following link to verify your email: {verification_url}'
    html_message = f'''
    <h2>Welcome to HerSpace!</h2>
    <p>Please click the button below to verify your email address:</p>
    <a href="{verification_url}" 
       style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
        Verify Email
    </a>
    <p>Or copy and paste this link into your browser:</p>
    <p>{verification_url}</p>
    <p>This link will expire in 24 hours.</p>
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )