from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import asyncio


@shared_task
def send_login_email(user_email):
    send_mail(
        'Вхід в систему calculator',
        'Ви успішно увійшли в систему calculator, якщо ви не робили цієї спроби, то наполегливо пропонуємо терміново змінити пароль аби протидіяти зловмисникам.',
        'anja.kuzmich@gmail.com',
        [user_email],
        fail_silently=False,
    )
    notify_admin(user_email,"Log_In")
from .models import CalculationHistory, ConversionHistory
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import os

@shared_task
def generate_pdf(user_id,user_mail):
    # Отримання історії операцій користувача
    calculation_history = CalculationHistory.objects.filter(user_id=user_id) 
    conversion_history = ConversionHistory.objects.filter(user_id=user_id)

    # Створення документу PDF
    pdf_file = os.path.join(settings.MEDIA_ROOT, f'user_{user_id}_history.pdf')
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Створення таблиці з даними
    data = []
    for calc in calculation_history:
        data.append([calc.expression, calc.result, calc.date_created.strftime('%Y-%m-%d %H:%M:%S')])
    for conv in conversion_history:
        data.append([conv.number, conv.from_base, conv.to_base, conv.result, conv.date_created.strftime('%Y-%m-%d %H:%M:%S')])

    table = Table(data)
    table.setStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 1, colors.black)])

    # Додавання таблиці до документу і збереження файлу PDF
    notify_admin(user_mail,"PDF Generation")
    doc.build([table])
    return pdf_file
def notify_admin(message, operation):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'async_operations',
        {
            'type': 'notify',
            'message': message,
            'operation': operation
        }
    )

