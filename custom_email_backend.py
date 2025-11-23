import smtplib
import socket
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.exceptions import SMTPException
import logging

logger = logging.getLogger(__name__)

class TimeoutEmailBackend(EmailBackend):
    """Custom email backend with proper timeout handling."""
    
    def open(self):
        """Open connection with timeout."""
        if self.connection:
            return False
        
        try:
            # Set socket timeout
            socket.setdefaulttimeout(10)
            
            # Call parent open method
            result = super().open()
            
            if result:
                logger.info("SMTP connection established successfully")
            else:
                logger.error("Failed to establish SMTP connection")
                
            return result
            
        except (socket.timeout, socket.error) as e:
            logger.error(f"SMTP connection timeout: {str(e)}")
            raise SMTPException(f"SMTP connection timeout: {str(e)}")
        except Exception as e:
            logger.error(f"SMTP connection error: {str(e)}")
            raise
    
    def send_messages(self, email_messages):
        """Send messages with timeout protection."""
        try:
            # Set socket timeout for sending
            socket.setdefaulttimeout(10)
            
            # Send messages
            result = super().send_messages(email_messages)
            
            if result:
                logger.info(f"Successfully sent {len(email_messages)} email(s)")
            else:
                logger.warning("No emails were sent")
                
            return result
            
        except (socket.timeout, socket.error) as e:
            logger.error(f"SMTP send timeout: {str(e)}")
            raise SMTPException(f"SMTP send timeout: {str(e)}")
        except Exception as e:
            logger.error(f"SMTP send error: {str(e)}")
            raise
        finally:
            # Reset socket timeout
            socket.setdefaulttimeout(None)
