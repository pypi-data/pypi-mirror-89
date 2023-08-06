import time

from django.core.management.base import BaseCommand

from django_schedule_commands.models import Group


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('group', type=str)

    def handle(self, *args, **options):
        group = Group.objects.get(name=options['group'])
        while True:
            group.run_pending()
            time.sleep(0.5)
