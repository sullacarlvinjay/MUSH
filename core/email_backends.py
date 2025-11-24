"""
Custom email backend for MushGuard using Brevo API with fallback to console.
"""

import requests
import logging
from django.core.mail.backends.console import EmailBackend as ConsoleBackend
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

class BrevoEmailBackend(ConsoleBackend):
    """
    Email backend that tries to send via Brevo API first, then falls back to console.
    """
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, 'BREVO_API_KEY', None)
        self.api_url = "https://api.brevo.com/v3/smtp/email"
        
        if not self.api_key:
            logger.warning("Brevo API key not configured, using console backend only")
    
    def send_messages(self, email_messages):
        """
        Send email messages via Brevo API, falling back to console if it fails.
        """
        if not email_messages:
            return
        
        sent_count = 0
        for message in email_messages:
            try:
                if self.api_key:
                    success = self._send_via_brevo(message)
                    if success:
                        sent_count += 1
                        continue
                
                # Fallback to console backend
                logger.info("Brevo failed, falling back to console backend")
                super().send_messages([message])
                sent_count += 1
                
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                if not self.fail_silently:
                    raise
        
        return sent_count
    
    def _send_via_brevo(self, message):
        """
        Send a single email message via Brevo API.
        """
        try:
            # Prepare Brevo API payload
            payload = {
                'sender': {
                    'name': 'MushGuard',
                    'email': 'carlsulla05@gmail.com'  # Must be verified in Brevo
                },
                'to': [{'email': email} for email in message.recipients()],
                'subject': message.subject,
                'htmlContent': message.body,
                'replyTo': {
                    'email': 'carlsulla05@gmail.com',
                    'name': 'MushGuard Support'
                }
            }
            
            headers = {
                'api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            logger.debug(f"Brevo API Key: {self.api_key}")
            logger.debug(f"Sending to Brevo API: {self.api_url}")
            logger.debug(f"Data: {payload}")
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            
            logger.debug(f"Brevo response status: {response.status_code}")
            logger.debug(f"Brevo response body: {response.text}")
            
            if response.status_code == 201:  # Success
                logger.info(f"Email sent successfully via Brevo to {message.recipients()}")
                return True
            else:
                logger.error(f"Brevo failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Brevo API request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending via Brevo: {e}")
            return False
