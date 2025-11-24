#!/usr/bin/env python
"""Test email sending functionality."""

import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

print("=== Email System Test ===")
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"Brevo API Key: {'Set' if getattr(settings, 'BREVO_API_KEY', '') else 'Not Set'}")
print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")

# Test email sending
try:
    print("\nSending test email...")
    result = send_mail(
        subject='Test Email from MushGuard',
        message='This is a test email to verify the email system is working.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['carlsulla3@gmail.com'],  # Test recipient
        fail_silently=False,
    )
    print(f"✅ Email sent successfully! Result: {result}")
except Exception as e:
    print(f"❌ Email failed: {e}")
    print(f"Error type: {type(e).__name__}")

print("\n=== Test Complete ===")
