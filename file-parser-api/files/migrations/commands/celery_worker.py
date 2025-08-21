from django.core.management.base import BaseCommand
from celery.bin import worker


class Command(BaseCommand):
    help = 'Start celery worker'

    def handle(self, *args, **options):
        # Start celery worker
        worker = worker.worker(app='file_parser.celery.app')
        worker.run(
            loglevel='INFO',
            traceback=True,
        )