from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        froms =TaskForm(request.POST or  None)
        if froms.is_valid():
            froms.save(commit=False).manage=request.user
            froms.save()
        messages.success(request,("New Task Added!"))
        return redirect('todolist')
    else:    
        all_tasks=TaskList.objects.filter(manage=request.user)
        paginator =Paginator(all_tasks,5)
        page =request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        context={
            "welcome_text":"Welcome To Todo List App.",
            'all_tasks':all_tasks,
            }
        return render(request,'todolist.html',context)


@login_required
def delete_task(request,task_id):
    task =TaskList.objects.get(pk=task_id)
    
    if task.manage ==request.user:

        task.delete()
        
    else:
        messages.success(request,("You can't access this page"))
    return redirect('todolist')


@login_required
def edit_task(request,edit_id):
    if request.method=="POST":
        task =TaskList.objects.get(pk=edit_id)
        froms=TaskForm(request.POST or None,instance=task)
        if froms.is_valid():
            froms.save()
        messages.success(request,("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj=TaskList.objects.get(pk=edit_id)
        return render(request,'edit.html',{'task_obj':task_obj})

@login_required
def complete_task(request,task_id):
    task =TaskList.objects.get(pk=task_id)
    if task.manage ==request.user:
        task.done=True
        task.save()
    else:
        messages.success(request,("You can't access this page"))
    return redirect('todolist')



@login_required
def pending_task(request,task_id):
    task =TaskList.objects.get(pk=task_id)
    if task.manage ==request.user:
        task.done=False
        task.save()
    else:
        messages.success(request,("You can't access this page"))    
    return redirect('todolist')


@login_required
def about(request):
    context={
        "welcome_text":"Welcome To about page.",
        }
    return render(request,'about.html',context)



def contact(request):
    context={
        "welcome_text":"Welcome To contact page.",
        }
    return render(request,'contact.html',context)

def index(request):
    context={
        "welcome_text":"Welcome To Index page.",
        }
    return render(request,'index.html',context)