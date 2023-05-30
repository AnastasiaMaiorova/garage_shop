from django.contrib import admin
from .models import MailModel
from import_export.admin import ExportActionMixin

class MailAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('email', )


admin.site.register(MailModel, MailAdmin)


# Register your models here.
