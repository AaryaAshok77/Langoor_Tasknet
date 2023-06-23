from django.contrib import admin

# Register your models here.
from .models import Conversation, Comment

admin.site.register(Conversation)
admin.site.register(Comment)