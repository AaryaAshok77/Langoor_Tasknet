from django.db import models
from django.conf import settings
from django.utils import timezone

from kanban.models import Task

class Conversation(models.Model):
    task = models.ForeignKey(Task, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-modified_at',)

class Comment(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(blank=True, upload_to='comment_files')
    sent_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_comments', on_delete=models.CASCADE)
