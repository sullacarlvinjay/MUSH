from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def test_simple_email():
    """Test email with basic Django SMTP backend."""
    
    print("=== Email Configuration ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'✓ Set' if settings.EMAIL_HOST_PASSWORD else '✗ Not set'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n=== Testing Basic SMTP Backend ===")
    
    # Temporarily switch to basic SMTP backend
    original_backend = settings.EMAIL_BACKEND
    settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
    try:
        subject = 'Test Email - Basic SMTP'
        message = 'This is a test email using basic SMTP backend.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.EMAIL_HOST_USER]  # Send to self
        
        print(f"Sending email to: {recipient_list[0]}")
        
        result = send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        if result:
            print("✅ Email sent successfully!")
        else:
            print("❌ Email failed to send")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore original backend
        settings.EMAIL_BACKEND = original_backend

if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    
    test_simple_email()
