from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from kanban.models import Task
from core.models import CustomUser

from .models import Conversation
from .forms import CommentForm

@login_required
def new_conversation(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)

    if request.user.role != 'director' and request.user not in task.assigned_to.all() and request.user != task.created_by:
        return redirect('core:index')
    
    conversations = Conversation.objects.filter(task=task).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)  # Include request.FILES for file uploads

        if form.is_valid():
            conversation = Conversation.objects.create(task=task)
            conversation.members.add(*task.assigned_to.all().values_list('id', flat=True))
            conversation.members.add(task.created_by)
            directors = CustomUser.objects.filter(role='director')
            conversation.members.add(*directors)
            conversation.save()

            conversation_comment = form.save(commit=False)
            conversation_comment.conversation = conversation
            conversation_comment.created_by = request.user
            conversation_comment.save()

            return redirect('kanban:task_detail', pk=task_pk)
        
    else:
        form = CommentForm()

    return render(request, 'conversation/new.html', {
        'form': form,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    search_query = request.GET.get('search', None)
    if search_query:
        conversations = conversations.filter(task__title__icontains=search_query)

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.user not in conversation.members.all() and request.user.role != 'director' and request.user != conversation.created_by:
        return redirect('core:index')

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            conversation_comment = form.save(commit=False)
            conversation_comment.conversation = conversation
            conversation_comment.created_by = request.user
            conversation_comment.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)

    else:
        form = CommentForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })