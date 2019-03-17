from .models import DocumentMeta,Template,DocumentFile
from django import forms

class DocumentMetaForm(forms.ModelForm):
    
    class Meta:
        model = DocumentFile
        fields = ['data_file']

class TemplateForm(forms.ModelForm):
    next = forms.CharField(required=False,widget=forms.HiddenInput())

    class Meta:
        model = Template
        fields = '__all__'

class GenerationForm(forms.Form):
    file = forms.ModelChoiceField(DocumentFile.objects.all(),help_text = 'File')
    template = forms.ModelChoiceField(Template.objects.all(),help_text= 'Template')
    row = forms.IntegerField( required=True)
