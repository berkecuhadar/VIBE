import json
import os
from django.core.management.base import BaseCommand
from vibe.models import Character

class Command(BaseCommand):
    help = 'Imports characters into the system from a JSON file'

    def handle(self, *args, **options):
        # File path (assumed to be in the same directory as manage.py)
        file_path = 'data.json'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Error: {file_path} not found.'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            count = 0

            for item in data:
                obj, created = Character.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'description': item['desc'],
                        'pic_url': item.get('pic', ''),
                        'tier': item.get('tier', 'C'),
                        'score': 0
                    }
                )
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Operation Completed: {count} new characters have been integrated into the system.'))