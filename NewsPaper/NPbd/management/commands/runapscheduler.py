# import logging
# from django.core.mail import EmailMultiAlternatives
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand
# from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from datetime import timedelta
# from django.utils import timezone
# from NPbd.models import Post
#
# logger = logging.getLogger(__name__)
#
#
# def my_job():
#     week = timezone.now() - timedelta(weeks=1)
#     posts = Post.objects.filter(adding_time__gt=week)
#     if not posts:
#         return
#     for user in User.objects.all():
#         # Список названий категорий-подписок пользователя
#         userSub = user.subscriptions.all().values_list('category__name', flat=True)
#         user_news = tuple(post for post in posts
#                           if set(post.category.all().values_list('name', flat=True)).intersection(set(userSub)))
#         if user_news:
#             subject = f'Список статей по Вашим подпискам за последнюю неделю'
#             text_content = '\n'.join([f'{news.post_title}: '
#                                       f'http://127.0.0.1{news.get_absolute_url()}' for news in user_news])
#             html_content = '<br><br>'.join([f'<a href="http://127.0.0.1{news.get_absolute_url()}">'
#                                             f'{news.post_title}</a><br>{news.preview()}' for news in user_news])
#             msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#
#
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(minute="00", hour="18", day_of_week='fri'),
#             id="my_job",  # The `id` assigned to each job MUST be unique
#             max_instances=1,
#             replace_existing=True,
#             timezone='Europe/Moscow'
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#             timezone='Europe/Moscow'
#         )
#         logger.info("Added weekly job: 'delete_old_job_executions'.")
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
