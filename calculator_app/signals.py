from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .tasks import send_login_email
from .models import CalculationHistory, ConversionHistory
from .tasks import generate_pdf
from django.db.models.signals import post_save

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    send_login_email.delay(user.email)

@receiver(post_save, sender=CalculationHistory)
@receiver(post_save, sender=ConversionHistory)
def generate_pdf_on_save(sender, instance, created, **kwargs):
    if created:
        generate_pdf.delay(instance.user_id)
