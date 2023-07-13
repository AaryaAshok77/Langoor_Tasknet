from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import Task, Project
from .forms import NewProjectForm, NewTaskForm
from core.models import CustomUser
from conversation.models import Comment, Conversation
from conversation.forms import CommentForm


@login_required
def board(request):
    user = request.user

    if user.role == 'director':
        projects = Project.objects.all()
        tasks = Task.objects.all()
    else:
        projects = Project.objects.filter(Q(assigned_users=user) | Q(creator=user)).distinct()
        tasks = Task.objects.filter(project__in=projects)

    status = request.GET.get('status', None)
    if status:
        projects = projects.filter(status=status)

    search_query = request.GET.get('search', None)
    if search_query:
        projects = projects.filter(name__icontains=search_query)

    assigned_only = bool(request.GET.get('assigned_only', False))
    if assigned_only:
        tasks = tasks.filter(assigned_to=user)

    return render(request, 'kanban/board.html', {
        'tasks': tasks,
        'projects': projects,
        'selected_status': status,
        'assigned_only': assigned_only,
    })


@login_required
def create_project(request):
    if request.user.role != 'product_owner' and request.user.role != 'director':
        return redirect('core:index')
    
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('kanban:project_detail', pk=project.pk)
    else:
        form = NewProjectForm()
    return render(request, 'kanban/create_project.html', {
        'form': form,
        'title': 'New Project'
    })

@login_required
def project_detail(request, pk):
    if request.user.role != 'product_owner' and request.user.role != 'director':
        return redirect('core:index')
    
    project = get_object_or_404(Project, pk=pk)

    return render(request, 'kanban/project_detail.html', {
        'project': project,
    })

@login_required
def project_list(request):
    if request.user.role != 'product_owner' and request.user.role != 'director':
        return redirect('core:index')
    
    user = request.user
    if user.role == 'director':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(creator=user)

    status = request.GET.get('status', None)
    if status:
        projects = projects.filter(status=status)

    search_query = request.GET.get('search', None)
    if search_query:
        projects = projects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    sort_by = request.GET.get('sort_by', 'start_date')
    if sort_by == 'end_date':
        projects = projects.order_by('end_date')
    else:
        projects = projects.order_by('start_date')

    my_projects = request.GET.get('my_projects')
    if my_projects and user.role == 'director':
        projects = projects.filter(creator=user)

    context = {
        'title': 'Projects',
        'projects': projects,
        'selected_status': status,
        'sort_by': sort_by,
    }

    return render(request, 'kanban/project_list.html', context)


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.creator and request.user.role != 'director':
        return redirect('core:index')
    
    if request.method == 'POST':
        form = NewProjectForm(request.POST, instance=project, is_edit_form=True)
        if form.is_valid():
            form.save()
            return redirect('kanban:project_detail', pk=pk)
    else:
        form = NewProjectForm(instance=project, is_edit_form=True)
    
    return render(request, 'kanban/project_edit.html', {
        'form': form,
        'title': 'Edit Project',
        'project': project,
    })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.creator and request.user.role != 'director':
        return redirect('core:index')
    

    if request.method == 'POST':
        project.delete()
        return redirect('kanban:project_list')

    return render(request, 'kanban/project_delete.html', {'project': project})




@login_required
def create_task(request):
    user = request.user

    if request.method == 'POST':
        form = NewTaskForm(user,request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = user
            task.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('kanban:task_detail', pk=task.pk)
    else:
        if request.user.role == 'director':
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(Q(assigned_users=user) | Q(creator=user)).distinct()
        if not projects:
            messages.error(request, 'You are not assigned to any project!!')
            return redirect('kanban:project_list')

        form = NewTaskForm(user)

    return render(request, 'kanban/create_task.html', {
        'form': form,
        'title': 'New Task',
        'projects': projects,
    })


@login_required
def get_assigned_users(request, project_id):
    project = Project.objects.get(pk=project_id)
    assigned_users = project.assigned_users.values('id', 'username')
    return JsonResponse(list(assigned_users), safe=False)

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.created_by and request.user != task.project.creator and request.user not in task.assigned_to.all() and request.user.role != 'director':
        return redirect('core:index')

    conversation = Conversation.objects.filter(task=task).filter(members__in=[request.user.id]).first()

    if conversation:
        comments = conversation.comments.order_by('-sent_at')

        paginator = Paginator(comments, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES)  # Include request.FILES for file uploads
            if form.is_valid():
                conversation_comment = form.save(commit=False)
                conversation_comment.conversation = conversation
                conversation_comment.created_by = request.user
                conversation_comment.save()

                conversation.save()

                return redirect('kanban:task_detail', pk=pk)

        else:
            form = CommentForm()
    else:
        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES)  # Include request.FILES for file uploads

            if form.is_valid():
                conversation = Conversation.objects.create(task=task)
                conversation.members.add(*task.assigned_to.all().values_list('id', flat=True))
                conversation.members.add(task.created_by)
                conversation.members.add(task.project.creator)
                directors = CustomUser.objects.filter(role='director')
                conversation.members.add(*directors)
                conversation.save()

                conversation_comment = form.save(commit=False)
                conversation_comment.conversation = conversation
                conversation_comment.created_by = request.user
                conversation_comment.save()

                return redirect('kanban:task_detail', pk=pk)
            
        else:
            form = CommentForm()

        comments = []
        page_obj = None

    context = {
        'task': task,
        'conversation': conversation,
        'comments': comments,
        'page_obj': page_obj,
        'form': form,
    }

    return render(request, 'kanban/task_detail.html', context)


@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        # Process the form submission and update the task status
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
        # Redirect to the task detail page or any other appropriate page
        return redirect('kanban:board')

    return render(request, 'kanban/update_task_status.html', {
        'task': task
    })

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.created_by and request.user != task.project.creator and request.user.role != 'director':
        return redirect('core:index')

    if request.method == 'POST':
        form = NewTaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)

            # Get the previous assigned users
            previous_assigned_users = set(task.assigned_to.all())

            # Update the assigned_to field of the task
            task.assigned_to.clear()
            assigned_to_users = form.cleaned_data['assigned_to']
            task.assigned_to.set(assigned_to_users)

            # Get the current assigned users
            current_assigned_users = set(assigned_to_users)

            # Update the members of the conversation related to the task
            conversations = Conversation.objects.filter(task=task)
            for conversation in conversations:
                previous_members = set(conversation.members.all())
                conversation.members.clear()
                conversation.members.add(*assigned_to_users.values_list('id', flat=True))
                conversation.members.add(task.created_by)
                conversation.save()

                current_members = set(conversation.members.all())

                # Find the users who were added and removed from the conversation
                added_members = current_members - previous_members
                removed_members = previous_members - current_members

                # Create comments for added members
                for added_member in added_members:
                    comment = Comment.objects.create(
                        conversation=conversation,
                        created_by=request.user,
                        content=f"*User '{added_member.username}' added to the conversation.*"
                    )

                # Create comments for removed members
                for removed_member in removed_members:
                    comment = Comment.objects.create(
                        conversation=conversation,
                        created_by=request.user,
                        content=f"*User '{removed_member.username}' removed from the conversation.*"
                    )

            task.save()

            return redirect('kanban:task_detail', pk=pk)
    else:
        form = NewTaskForm(request.user, instance=task)

    assigned_users = task.project.assigned_users.all()
    assigned_to = task.assigned_to.all()

    return render(request, 'kanban/task_edit.html', {
        'form': form,
        'task': task,
        'assigned_to': assigned_to,
        'assigned_users': assigned_users
    })


@login_required
def task_list(request):
    user = request.user

    assigned_to_me = request.GET.get('assigned_to_me')
    if user.role == 'director' and assigned_to_me:
        tasks = Task.objects.filter(assigned_to=user)
    elif user.role == 'director':
        tasks = Task.objects.all()
    elif user.role == 'product_owner':
        tasks = Task.objects.filter(Q(assigned_to=user) | Q(created_by=user) | Q(project__creator=request.user)).distinct()
    else:
        tasks = Task.objects.filter(Q(assigned_to=user) | Q(created_by=user)).distinct()

    status = request.GET.get('status', None)
    if status:
        tasks = tasks.filter(status=status)

    search_query = request.GET.get('search', None)
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    sort_by = request.GET.get('sort_by', 'created_date')

    if sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'created_date':
        tasks = tasks.order_by('created_at')

    context = {
        'title': 'Tasks',
        'tasks': tasks,
        'selected_status': status,
        'sort_by': sort_by,
        'assigned_to_me': assigned_to_me,  # Pass the assigned_to_me value to the template
        'user': user,  # Pass the user object to the template
    }

    return render(request, 'kanban/task_list.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.created_by and request.user.role != 'director':
        return redirect('core:index')

    if request.method == 'POST':
        task.delete()
        return redirect('kanban:board')

    return render(request, 'kanban/task_delete.html', {'task': task})
