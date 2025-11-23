from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def test_email_now(request):
    """Test email sending configuration."""
    
    try:
        # Test email configuration
        subject = f'{settings.EMAIL_SUBJECT_PREFIX} Email Test'
        message = 'This is a test email from MushGuard to verify email configuration is working.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['test@example.com']  # You can change this
        
        # Send test email
        result = send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        config_info = f"""
        <h3>Email Configuration:</h3>
        <p><strong>Backend:</strong> {settings.EMAIL_BACKEND}</p>
        <p><strong>Host:</strong> {settings.EMAIL_HOST}</p>
        <p><strong>Port:</strong> {settings.EMAIL_PORT}</p>
        <p><strong>Use TLS:</strong> {settings.EMAIL_USE_TLS}</p>
        <p><strong>From Email:</strong> {settings.DEFAULT_FROM_EMAIL}</p>
        <p><strong>Host User:</strong> {settings.EMAIL_HOST_USER}</p>
        <p><strong>Host Password:</strong> {'✓ Set' if settings.EMAIL_HOST_PASSWORD else '✗ Not set'}</p>
        <p><strong>Timeout:</strong> {settings.EMAIL_TIMEOUT}s</p>
        <hr>
        <h3>Test Result:</h3>
        <p><strong>Send Result:</strong> {'✓ Success' if result else '✗ Failed'}</p>
        <p><strong>Recipients:</strong> {', '.join(recipient_list)}</p>
        """
        
        return HttpResponse(f"""
        <html>
        <head><title>Email Test</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>MushGuard Email Configuration Test</h2>
            <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; display: inline-block; text-align: left;">
                {config_info}
                <hr>
                <h3>Setup Instructions:</h3>
                <ol>
                    <li>Go to your Google Account settings</li>
                    <li>Enable 2-Step Verification</li>
                    <li>Generate an App Password</li>
                    <li>Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in Render dashboard</li>
                </ol>
                <p><strong>Note:</strong> Use Gmail App Password, not your regular password!</p>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HttpResponse(f"""
        <html>
        <head><title>Email Test Error</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Email Test Error</h2>
            <div style="background: #ffe6e6; padding: 20px; border-radius: 8px; display: inline-block;">
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Backend:</strong> {settings.EMAIL_BACKEND}</p>
                <p><strong>Host User:</strong> {settings.EMAIL_HOST_USER}</p>
            </div>
        </body>
        </html>
        """)
