from django.contrib import admin
from core.models import Message
from attachments.admin import AttachmentInlines


class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)
    inlines = [AttachmentInlines]

admin.site.register(Message, MessageAdmin)
