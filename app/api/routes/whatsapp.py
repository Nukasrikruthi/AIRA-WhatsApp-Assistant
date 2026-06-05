"""
WhatsApp API routes - Handle WhatsApp webhook and messaging
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.schemas.schemas import WhatsAppMessageRequest, WhatsAppMessageResponse
from app.services.whatsapp_service import WhatsAppService
from app.integrations.twilio_client import get_twilio_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["WhatsApp"])


@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio WhatsApp webhook receiver
    
    This endpoint receives incoming WhatsApp messages from Twilio
    and sends back appropriate responses
    """
    try:
        # Parse form data from Twilio
        form_data = await request.form()
        
        # Extract message information
        phone_number = form_data.get("From", "").replace("whatsapp:", "")
        message_body = form_data.get("Body", "").strip()
        message_sid = form_data.get("MessageSid", "")
        
        logger.info(f"Received WhatsApp message from {phone_number}: {message_body}")
        
        if not phone_number or not message_body:
            logger.warning("Missing phone number or message body")
            return {"status": "error"}
        
        # Process message through WhatsApp service
        response_message, menu_state = WhatsAppService.handle_incoming_message(
            db, phone_number, message_body
        )
        
        logger.info(f"Response menu state: {menu_state}")
        
        # Send response via Twilio
        twilio_client = get_twilio_client()
        response_phone = f"whatsapp:{phone_number}"
        
        success = twilio_client.send_message(response_phone, response_message)
        
        if success:
            logger.info(f"Response sent to {phone_number}")
            return {
                "status": "success",
                "message_sid": message_sid,
                "menu_state": menu_state
            }
        else:
            logger.error(f"Failed to send response to {phone_number}")
            return {"status": "error"}
    
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}", exc_info=True)
        return {"status": "error"}


@router.post("/send")
async def send_whatsapp_message(
    to_phone: str,
    message: str,
    db: Session = Depends(get_db)
):
    """
    Send WhatsApp message (Admin endpoint)
    
    Note: This is for administrative purposes (notifications, alerts)
    Normal parent-admin communication goes through the webhook
    """
    try:
        if not to_phone or not message:
            raise HTTPException(status_code=400, detail="Missing phone or message")
        
        twilio_client = get_twilio_client()
        
        # Format phone
        if not to_phone.startswith("whatsapp:"):
            to_phone = f"whatsapp:{to_phone}"
        
        success = twilio_client.send_message(to_phone, message)
        
        if success:
            logger.info(f"Admin message sent to {to_phone}")
            return {
                "status": "success",
                "recipient": to_phone,
                "message": message
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send message")
    
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def whatsapp_health():
    """Health check for WhatsApp integration"""
    twilio_client = get_twilio_client()
    
    is_configured = twilio_client.account_sid and twilio_client.auth_token
    
    return {
        "status": "healthy",
        "twilio_configured": is_configured,
        "whatsapp_number": twilio_client.whatsapp_number
    }
