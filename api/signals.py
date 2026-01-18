from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging
import threading

from .models import Lead

logger = logging.getLogger(__name__)

def _send_email_async(subject, html_message, from_email, recipient_list, lead_id, recipient_email):
    """
    Send email in a separate thread to avoid blocking the main request.
    """
    try:
        send_mail(
            subject=subject,
            message='',  # Empty message, HTML only
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Business evaluation email sent to {recipient_email} for lead ID {lead_id}")
    except Exception as e:
        logger.error(f"Failed to send business evaluation email to {recipient_email}: {str(e)}", exc_info=True)

@receiver(post_save, sender=Lead)
def send_business_evaluation_email(sender, instance, created, **kwargs):
    """
    Send business evaluation email when a new lead is created.
    Uses threading to send email asynchronously and avoid blocking the request.
    """
    if not instance.is_complete:
        return
    
    try:
        # Read valuation from database
        # Only proceed if valuation has been calculated and stored
        if instance.valuation_low is None or instance.valuation_high is None:
            logger.warning(f"Lead {instance.id} created without valuation data. Skipping email.")
            return
        
        # Format valuation numbers
        def format_currency(value):
            """Format decimal as currency string with commas."""
            return f"{float(value):,.0f}"
        
        # Prepare email context
        context = {
            'lead': instance,
            'valuation_low': instance.valuation_low,
            'valuation_high': instance.valuation_high,
            'valuation_low_formatted': format_currency(instance.valuation_low),
            'valuation_high_formatted': format_currency(instance.valuation_high),
            'sde': instance.sde,
            'site_url': getattr(settings, 'SITE_URL', 'https://chelseacorporate.com'),
            'backend_url': getattr(settings, 'BACKEND_URL', 'http://localhost:8000'),
            'contact_email': getattr(settings, 'CONTACT_EMAIL', 'info@chelseacorporate.com'),
            'contact_phone': getattr(settings, 'CONTACT_PHONE', '0117 435 4350'),
        }
        
        # Render email template
        subject = f'Your Business Valuation Estimate - {instance.company_sector}'
        html_message = render_to_string('emails/business_evaluation.html', context)
        
        # Send email asynchronously in a background thread
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        
        email_thread = threading.Thread(
            target=_send_email_async,
            args=(subject, html_message, from_email, [instance.email], instance.id, instance.email),
            daemon=True
        )
        email_thread.start()
        
        logger.info(f"Email queued for {instance.email} for lead ID {instance.id}")
        
    except Exception as e:
        logger.error(f"Failed to queue email for {instance.email}: {str(e)}", exc_info=True)
        # Don't raise exception to avoid breaking the lead creation

