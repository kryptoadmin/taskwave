from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Task
from .forms import TaskForm

def task_list(request):
    try:
        tasks = Task.objects.all()
    except Exception as e:
        tasks = []
        error_message = str(e)
        return render(request, 'tasks/task_list.html', {'tasks': tasks, 'error': error_message})
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
    except Http404:
        error_message = "Task not found."
        return render(request, 'tasks/task_detail.html', {'error': error_message})
    except Exception as e:
        error_message = str(e)
        return render(request, 'tasks/task_detail.html', {'error': error_message})
    
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('task_list')
            except Exception as e:
                error_message = str(e)
                return render(request, 'tasks/task_form.html', {'form': form, 'error': error_message})
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
    except Http404:
        error_message = "Task not found."
        return render(request, 'tasks/task_form.html', {'error': error_message})
    except Exception as e:
        error_message = str(e)
        return render(request, 'tasks/task_form.html', {'error': error_message})

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                form.save()
                return redirect('task_list')
            except Exception as e:
                error_message = str(e)
                return render(request, 'tasks/task_form.html', {'form': form, 'error': error_message})
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    except Http404:
        error_message = "Task not found."
        return redirect('task_list')
    except Exception as e:
        error_message = str(e)
        return redirect('task_list', {'error': error_message})
    
    return redirect('task_list')
