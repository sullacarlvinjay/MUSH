"""
Brevo service - Server-friendly email sending method
Uses Brevo HTTP API (works with servers)
"""

import requests
import json
import os
from django.conf import settings

def send_email_via_brevo(to_email, subject, message, verification_link=None):
    """
    Send email using Brevo HTTP API
    This works perfectly with servers like Render
    """
    
    # Debug: Check Brevo API key
    print(f"DEBUG: Brevo API Key: {os.getenv('BREVO_API_KEY')}")
    
    api_key = os.getenv('BREVO_API_KEY', '')
    
    if not api_key:
        print("Brevo API key not configured")
        return False
    
    try:
        # Brevo API endpoint
        url = "https://api.brevo.com/v3/smtp/email"
        
        # Prepare email data
        data = {
            'sender': {
                'name': 'MushGuard',
                'email': 'noreply@brevo.com'
            },
            'to': [{'email': to_email}],
            'subject': subject,
            'htmlContent': f"""
                <p>{message}</p>
                <p><a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Click here to verify your email</a></p>
                <p>Or copy this link: <a href="{verification_link}">{verification_link}</a></p>
                <p><strong>MushGuard Team</strong></p>
                <p><small>Sent on behalf of carlsulla05@gmail.com</small></p>
            """,
            'replyTo': {'email': 'carlsulla05@gmail.com', 'name': 'MushGuard Support'}
        }
        
        print(f"DEBUG: Sending to Brevo API: {url}")
        print(f"DEBUG: Data: {data}")
        
        # Send HTTP request
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'api-key': api_key
        }
        
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        print(f"DEBUG: Brevo response status: {response.status_code}")
        print(f"DEBUG: Brevo response body: {response.text}")
        
        if response.status_code == 201:  # Brevo returns 201 for success
            print(f"Email sent via Brevo to {to_email}")
            return True
        else:
            print(f"Brevo failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Brevo error: {str(e)}")
        return False

# Keep EmailJS function for compatibility
def send_email_via_emailjs(to_email, subject, message, verification_link=None):
    """
    EmailJS doesn't work with servers - use Brevo instead
    """
    print("EmailJS disabled for server use - switching to Brevo")
    return send_email_via_brevo(to_email, subject, message, verification_link)
