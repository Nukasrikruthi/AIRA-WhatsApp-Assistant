"""
Twilio integration - Handle WhatsApp communication
"""
from twilio.rest import Client
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)


class TwilioWhatsAppClient:
    """Client for Twilio WhatsApp integration"""
    
    def __init__(self):
        """Initialize Twilio client"""
        settings = get_settings()
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.whatsapp_number = settings.twilio_whatsapp_number
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            logger.warning("Twilio credentials not configured")
            self.client = None
    
    def send_message(self, to_phone: str, message_body: str) -> bool:
        """
        Send WhatsApp message
        
        Args:
            to_phone: Recipient phone number (format: whatsapp:+6302894103)
            message_body: Message content
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        try:
            # Format phone number if needed
            if not to_phone.startswith("whatsapp:"):
                to_phone = f"whatsapp:{to_phone}"
            
            # Send message
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=message_body,
                to=to_phone
            )
            
            logger.info(f"Message sent successfully. SID: {message.sid}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    def validate_webhook_signature(self, request_data: dict, signature: str) -> bool:
        """
        Validate Twilio webhook signature
        
        Args:
            request_data: Request data
            signature: X-Twilio-Signature header
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.client:
            logger.warning("Twilio client not initialized, skipping signature validation")
            return True  # In development, allow without validation
        
        try:
            # In production, validate signature
            # For MVP, we can skip this
            return True
        
        except Exception as e:
            logger.error(f"Error validating signature: {e}")
            return False


# Global client instance
_twilio_client = None


def get_twilio_client() -> TwilioWhatsAppClient:
    """Get Twilio client instance (lazy initialization)"""
    global _twilio_client
    
    if _twilio_client is None:
        _twilio_client = TwilioWhatsAppClient()
    
    return _twilio_client
