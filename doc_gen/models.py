from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
# Create your models here.
    


class DocumentMeta(models.Model):
    meta = models.CharField(unique=True, verbose_name='Meta Format', max_length=200,help_text='Enter the META format for the data', blank=True )

    def __str__(self):
        return str(self.meta)

class DocumentFile(models.Model):
    meta = models.ForeignKey( DocumentMeta,verbose_name='Meta for document', on_delete=models.CASCADE)
    data_file = models.FileField(verbose_name='Data File', help_text='Upload the file containing the datasets (.csv, .json, ...)',upload_to='data/')
    created = models.DateTimeField("created at:", auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{ str(self.data_file)} '
    def get_absolute_url(self):
        return reverse_lazy("doc-detail", kwargs={"pk": self.meta.pk})
    

class Template(models.Model):
    name = models.CharField(verbose_name = 'Template Name', max_length=50)
    doc_meta = models.ForeignKey(DocumentMeta, on_delete=models.CASCADE)
    template = RichTextField()

    
    def get_absolute_url(self):
        return reverse_lazy("template-detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return str(self.name)
    

# @receiver(post_save, sender=DocumentMeta)
# def create_meta(sender, instance, **kwargs):
#     if str(instance.data_file).split('.')[-1] == 'csv':
#         with open(instance.data_file.path, "r") as f:
#             reader = csv.reader(f)
#             i = next(reader)
#             i.sort()
#             if instance.meta != str(i):
#                 instance.meta = str(i)
#                 instance.save()                           