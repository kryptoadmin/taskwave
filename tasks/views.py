from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

## Retrieve all the list of tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

## Retrieve the detail of the task
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})

## Create a new task
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})

# Update the existing task
def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form})

# Delete the task
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect("task_list")

