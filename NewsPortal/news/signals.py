from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, EmailMessage, send_mail
from django.db.models.signals import m2m_changed, post_save
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from news.models import PostCategory


def send_notifications(preview, pk, title, subscribers_emails):
    html_content = render_to_string(
        'post_create_email.html',

        {
            'text': preview,
            'link': f'{SITE_URL}{pk}',

        }

    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_emails,

    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()





@receiver(post_save, sender=User)
def welcome_email(created, **kwargs):
    instance = kwargs['instance']
    if created:
        html_content = render_to_string(
            'email/welcome.html',
            {
                'text': f'{instance.username}, Ваша регистрация прошла успешно!',
            }
        )
        msg = EmailMultiAlternatives(
            subject='Добро пожаловать!',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[instance.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
