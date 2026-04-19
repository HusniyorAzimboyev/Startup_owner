from django.core.management.base import BaseCommand
from datetime import datetime
import json
from apps.accounts.models import User
from apps.tasks.models import Task


class Command(BaseCommand):
    help = 'Load tasks from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            created_count = 0
            for user_tasks in data['tasks']:
                username = user_tasks['username']
                
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"User {username} not found"))
                    continue
                
                for task_data in user_tasks['tasks']:
                    task = Task.objects.create(
                        user=user,
                        title=task_data['title'],
                        description=task_data['description'],
                        status=task_data['status'],
                        priority=task_data['priority'],
                        due_date=datetime.strptime(task_data['due_date'], '%Y-%m-%d').date(),
                    )
                    created_count += 1
                    self.stdout.write(f"  ✓ Created task: {task.title}")
                
                self.stdout.write(self.style.SUCCESS(f"✓ Loaded tasks for {username}"))
            
            self.stdout.write(self.style.SUCCESS(f"\n✓ Total tasks created: {created_count}"))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {json_file}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
