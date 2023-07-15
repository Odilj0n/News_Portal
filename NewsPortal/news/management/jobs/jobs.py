from django.utils.timezone import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from datetime import timedelta

from news.models import Post, Category
from NewsPortal.settings import DEFAULT_FROM_EMAIL


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