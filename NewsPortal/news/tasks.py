from datetime import *

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import news
from NewsPortal import settings
from celery import shared_task

from news.models import Post, Category
from news.signals import send_notifications
from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL


@shared_task
def weekly_email_job():
    start_date = datetime.today() - timedelta(days=6)
    this_weeks_posts = Post.objects.filter(created_at__gt=start_date)
    for cat in Category.objects.all():
        post_list = this_weeks_posts.filter(post_category=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            html_content = render_to_string(
                'email/weekly_posts_email.html', {
                    'post_list': post_list.values('pk', 'post_title'),
                    'domain': Site.objects.get_current().domain,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{cat.category_name}: Посты за прошедшую неделю',
                body="post_list",
                from_email=DEFAULT_FROM_EMAIL,
                to=recipients
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


# @shared_task
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#
#         categories = instance.post_category.all()
#         subscribers_emails = []
#         for category in categories:
#             subscribers = category.subscribers.all()
#
#             subscribers_emails += [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.post_title, subscribers_emails)


@shared_task
def notify_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category_PostCategory.all()
    title = post.post_title
    subscribers = []
    for category in categories:
        sub = category.subscribers.all()
        for user in sub:
            subscribers.append(user.email)
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': news.models.Post.post_title,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()
