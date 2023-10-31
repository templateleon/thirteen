from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed, \
    post_delete  # К сожалению, в нашем случае нельзя использовать сигнал post_save
from django.dispatch import receiver

from .models import PostCategory, Post
from .tasks import post_created


@receiver(m2m_changed, sender=PostCategory) # Вместо сигнала post_save используем сигнал m2m_changed
def notif_subs(sender, instance, action, **kwargs):
    if action == 'post_add' and instance.__class__.__name__ == 'Post':
        post_created.apply_async((instance.id, instance.title, instance.text),
            countdown=1,)
        # for category in instance.category.all():
        #
        #     emails = User.objects.filter(
        #         subscriptions__category=category
        #     ).values_list('email', flat=True)
        #     print(emails[0])
        #
        #     subject = f'Новая публикация в категории: {category}'
        #     print(subject)
        #
        #     text_content = (
        #         f'Название: {instance.title}\n'
        #         f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
        #                     )
        #     html_content = (
        #         f'Накименование: {instance.title}<br>'
        #         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        #         f'Ссылка на публикацию</a>'
        #                     )
        #
        # for email in emails:
        #     msg = EmailMultiAlternatives(subject, text_content, None, [email])
        #     msg.attach_alternative(html_content, "text/html")
        #     msg.send()


@receiver(post_delete, sender=Post)
def post_del(sender, instance, **kwargs):
    subject = f'Новость "{instance.title}" удалена'

    send_mail(
        subject=subject,
        message=instance.text,
        from_email='@yandex.ru',
        recipient_list=['@yandex.ru']
    )