from django.contrib import admin
from .models import Template, DocumentMeta, DocumentFile
# Register your models here.
admin.site.register(Template)
admin.site.register(DocumentMeta)
admin.site.register(DocumentFile)
