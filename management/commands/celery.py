import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery(*args, **kwargs):
    kill_worker_cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(kill_worker_cmd))
    start_worker_cmd = 'celery -A geonode.celery_app:app worker -l info'
    subprocess.call(shlex.split(start_worker_cmd))


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Starting celery worker with autoreload...')
        # You should use the following line for older version(<2.2)
        # autoreload.main(restart_celery, args=None,       kwargs=None)
        autoreload.run_with_reloader(restart_celery, args=None, kwargs=None)