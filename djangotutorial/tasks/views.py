from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm


def task_list(request):
    """Main dashboard showing all tasks."""
    filter_status = request.GET.get('status', '')
    filter_priority = request.GET.get('priority', '')

    tasks = Task.objects.all()

    if filter_status:
        tasks = tasks.filter(status=filter_status)
    if filter_priority:
        tasks = tasks.filter(priority=filter_priority)

    # Stats
    total = Task.objects.count()
    completed = Task.objects.filter(completed=True).count()
    pending = total - completed
    overdue_count = sum(1 for t in Task.objects.filter(completed=False) if t.is_overdue)

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue_count': overdue_count,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


def task_update(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'task': task})


def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@require_POST
def task_toggle_complete(request, pk):
    """Toggle task completion status."""
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    if task.completed:
        task.status = 'done'
    else:
        task.status = 'todo'
    task.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'completed': task.completed, 'status': task.get_status_display()})
    return redirect('task_list')
