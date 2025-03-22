from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('search')

    tasks = Task.objects.filter(user=request.user)

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'current_filters': {
            'status': status_filter,
            'priority': priority_filter,
            'search': search_query
        }
    }
    return render(request, 'todo_app/task_list.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo_app:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo_app/task_detail.html', {'task': task, 'form': form})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('todo_app:task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/add_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('todo_app:task_list')
    return render(request, 'todo_app/delete_task.html', {'task': task})

@login_required
def progress(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': completion_rate
    }
    return render(request, 'todo_app/progress.html', context)

@login_required
def reports(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed')
    overdue_tasks = tasks.filter(due_date__lt=timezone.now().date(), status__in=['not_started', 'in_progress'])
    
    priority_stats = {
        'high': tasks.filter(priority='high').count(),
        'medium': tasks.filter(priority='medium').count(),
        'low': tasks.filter(priority='low').count()
    }
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks.count(),
        'overdue_tasks': overdue_tasks.count(),
        'priority_stats': priority_stats,
        'recent_completed': completed_tasks.order_by('-completed_date')[:5]
    }
    return render(request, 'todo_app/reports.html', context)
