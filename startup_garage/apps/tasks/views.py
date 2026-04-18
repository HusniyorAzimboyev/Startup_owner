import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .models import Task
from .forms import TaskForm


class TaskBoardView(LoginRequiredMixin, TemplateView):
    """Kanban board view - displays tasks grouped by status"""
    template_name = 'tasks/board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get all user tasks
        all_tasks = Task.objects.filter(user=user).select_related('user')

        # Group tasks by status
        todo_tasks = all_tasks.filter(status='todo')
        in_progress_tasks = all_tasks.filter(status='in_progress')
        done_tasks = all_tasks.filter(status='done')

        # Get counts for each status
        status_counts = all_tasks.values('status').annotate(count=Count('id'))
        status_count_dict = {item['status']: item['count'] for item in status_counts}

        context.update({
            'todo_tasks': todo_tasks,
            'in_progress_tasks': in_progress_tasks,
            'done_tasks': done_tasks,
            'status_counts': status_count_dict,
            'total_tasks': all_tasks.count(),
        })

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create a new task"""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-board')

    def form_valid(self, form):
        """Set the user before saving"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create Task'
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing task"""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-board')

    def get_queryset(self):
        """Only allow users to edit their own tasks"""
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit Task'
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a task"""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-board')

    def get_queryset(self):
        """Only allow users to delete their own tasks"""
        return Task.objects.filter(user=self.request.user)


@require_POST
def task_move(request, pk):
    """Move task to a different status (AJAX endpoint)"""
    try:
        task = Task.objects.get(pk=pk, user=request.user)
        data = json.loads(request.body)
        new_status = data.get('status')

        # Validate status
        valid_statuses = ['todo', 'in_progress', 'done']
        if new_status not in valid_statuses:
            return JsonResponse({'ok': False, 'error': 'Invalid status'}, status=400)

        # Update task status
        task.status = new_status
        task.save(update_fields=['status', 'updated_at'])

        return JsonResponse({'ok': True, 'status': new_status})
    except Task.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Task not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

