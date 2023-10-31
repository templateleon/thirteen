import datetime
#import time

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from News.models import Post, Category


@shared_task
def weekly_news():
    today = datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscriptions', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Weekly news',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def post_created(sender, instance, action, **kwargs):

    for category in instance.category.all():
        emails = User.objects.filter(
            subscriptions__category=category
            ).values_list('email', flat=True)
        print(emails[0])

        subject = f'Новая публикация в категории: {category}'
        print(subject)

        text_content = (
                f'Название: {instance.title}\n'
                f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
                            )
        html_content = (
                f'Накименование: {instance.title}<br>'
                f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
                f'Ссылка на публикацию</a>'
                            )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()