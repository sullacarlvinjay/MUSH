from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def debug_email_view(request):
    """Debug email sending issues and show configuration."""
    
    debug_info = []
    debug_info.append(f"<strong>EMAIL_BACKEND:</strong> {settings.EMAIL_BACKEND}")
    debug_info.append(f"<strong>EMAIL_HOST:</strong> {settings.EMAIL_HOST}")
    debug_info.append(f"<strong>EMAIL_PORT:</strong> {settings.EMAIL_PORT}")
    debug_info.append(f"<strong>EMAIL_USE_TLS:</strong> {settings.EMAIL_USE_TLS}")
    debug_info.append(f"<strong>EMAIL_HOST_USER:</strong> {settings.EMAIL_HOST_USER}")
    debug_info.append(f"<strong>EMAIL_HOST_PASSWORD:</strong> {'✓ Set' if settings.EMAIL_HOST_PASSWORD else '✗ Not set'}")
    debug_info.append(f"<strong>DEFAULT_FROM_EMAIL:</strong> {settings.DEFAULT_FROM_EMAIL}")
    debug_info.append(f"<strong>EMAIL_TIMEOUT:</strong> {getattr(settings, 'EMAIL_TIMEOUT', 'Not set')}")
    debug_info.append(f"<strong>EMAIL_SUBJECT_PREFIX:</strong> {getattr(settings, 'EMAIL_SUBJECT_PREFIX', 'Not set')}")
    
    # Test email sending
    test_result = "Not tested"
    error_details = ""
    
    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        try:
            subject = f'{getattr(settings, "EMAIL_SUBJECT_PREFIX", "")} Test Email'
            message = 'This is a test email to verify configuration.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.EMAIL_HOST_USER]  # Send to self
            
            result = send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            if result:
                test_result = "✅ SUCCESS - Email sent!"
            else:
                test_result = "❌ FAILED - No error but email not sent"
        except Exception as e:
            test_result = "❌ FAILED - Exception occurred"
            error_details = f"<br><strong>Error:</strong> {str(e)}"
            logger.error(f"Email test failed: {str(e)}")
    else:
        test_result = "❌ SKIPPED - Email credentials not configured"
    
    # Show current users
    from django.contrib.auth.models import User
    from core.models import UserProfile
    
    users_info = []
    for user in User.objects.all():
        try:
            profile = user.profile
            users_info.append(f"{user.username}: verified={profile.email_verified}, token={profile.verification_token}")
        except:
            users_info.append(f"{user.username}: no profile")
    
    return HttpResponse(f"""
    <html>
    <head><title>Email Debug</title></head>
    <body style="font-family: Arial; margin: 20px;">
        <h2>🔍 MushGuard Email Debug</h2>
        
        <h3>📧 Email Configuration:</h3>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
            {'<br>'.join(debug_info)}
        </div>
        
        <h3>🧪 Email Test Result:</h3>
        <div style="background: {'#e8f5e8' if 'SUCCESS' in test_result else '#ffe6e6'}; padding: 15px; border-radius: 5px;">
            <strong>{test_result}</strong>{error_details}
        </div>
        
        <h3>👥 Users & Verification Status:</h3>
        <div style="background: #f0f8ff; padding: 15px; border-radius: 5px;">
            {'<br>'.join(users_info) if users_info else 'No users found'}
        </div>
        
        <h3>🔧 Setup Instructions:</h3>
        <div style="background: #fff3cd; padding: 15px; border-radius: 5px;">
            <ol>
                <li>Enable 2-Step Verification on your Google Account</li>
                <li>Generate an <strong>App Password</strong> (not regular password)</li>
                <li>Go to Render Dashboard → Service → Settings → Environment</li>
                <li>Add EMAIL_HOST_USER (your Gmail)</li>
                <li>Add EMAIL_HOST_PASSWORD (App Password)</li>
                <li>Redeploy the service</li>
            </ol>
            <p><strong>Important:</strong> Use Gmail App Password, not your regular password!</p>
        </div>
        
        <h3>🎯 Quick Fix:</h3>
        <div style="background: #d1ecf1; padding: 15px; border-radius: 5px;">
            <p>If you want to skip email verification for testing, the system now auto-verifies users when email is not configured.</p>
            <p>Users can login immediately after signup!</p>
        </div>
    </body>
    </html>
    """)
