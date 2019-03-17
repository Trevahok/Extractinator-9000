from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.http import HttpResponse
from . import models
from . import forms
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
# Create your views here.
import csv
import json
from io import StringIO
from jinja2 import Template 

class DocumentListView(LoginRequiredMixin,ListView):
    model = models.DocumentMeta
    template_name = 'document_list.html'
    
class DocumentCreateView(LoginRequiredMixin,CreateView):
    form_class = forms.DocumentMetaForm
    template_name = "generic_form.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        request.POST._mutable = True
        document = self.request.FILES['data_file']
        if str(document).split('.')[-1] == 'csv':
            csvf = StringIO(document.read().decode())
            reader = csv.reader(csvf, delimiter=',')
            i = next(reader)
            i.sort()
            form.data['meta'] = str(i)
            print(i)
        elif str(document).split('.')[-1] == 'json':
            json_data = json.loads(document.read().decode())
            # print(sorted(json_data[0].keys()))
            form.data['meta'] = str(sorted(json_data[0].keys()))

        print('form received')
        if form.is_valid():
            print('form valid ')
            instance = form.save(commit=False)
            meta_instance,created = models.DocumentMeta.objects.get_or_create(meta=form.data['meta'])
            instance.meta = meta_instance
            return self.form_valid(form,*args,**kwargs)
        else:
            return self.form_invalid(form,*args,**kwargs)


class DocumentUpdateView(LoginRequiredMixin,UpdateView):
    model = models.DocumentFile
    form_class = forms.DocumentMetaForm
    template_name = "generic_form.html"

class DocumentDeleteView(LoginRequiredMixin,DeleteView):
    model = models.DocumentFile
    template_name = "delete_confirm.html"
    success_url = reverse_lazy('doc-view')

class DocumentMetaDeleteView(LoginRequiredMixin,DeleteView):
    model = models.DocumentMeta
    template_name = "delete_confirm.html"
    success_url = reverse_lazy('doc-view')

class DocumentMetaDetailView(LoginRequiredMixin,DetailView):
    model = models.DocumentMeta
    template_name = "document_detail.html"
    context_object_name = "document"

class TemplateListView(LoginRequiredMixin,ListView):
    model = models.Template
    template_name = "template_list.html"
        
class TemplateCreateView(LoginRequiredMixin,CreateView):
    model = models.Template
    form_class = forms.TemplateForm
    template_name = "generic_form.html"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        redirect = self.request.GET.get('next')
        print(redirect)
        if redirect:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': redirect})
            else:
                kwargs['initial'] = {'next': redirect}
        return kwargs


    def form_valid(self, form):
        redirect = form.cleaned_data.get('next')
        print(redirect)
        if redirect:
            self.success_url = redirect
        return super().form_valid(form)

    def get_initial(self):
        if 'pk' in self.kwargs:
            initial = super().get_initial()
            initial = initial.copy()
            initial['doc_meta'] = self.kwargs['pk']
            print(initial)
            return initial
        else:
            return super().get_initial()

class TemplateDetailView(LoginRequiredMixin,DetailView):
    model = models.Template
    context_object_name = 'template'
    template_name = 'template_detail.html'

class TemplateUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Template
    form_class = forms.TemplateForm
    template_name = "generic_form.html"

class TemplateDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Template
    template_name = "delete_confirm.html"
    success_url = reverse_lazy('template-detail')


class GenerateDocumentView(LoginRequiredMixin,FormView):
    form_class = forms.GenerationForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            file = models.DocumentFile.objects.get(pk=form.data['file'])
            template = models.Template.objects.get(pk= form.data['template'])
            print(file.data_file)
            if 'csv' in str(file.data_file):
                reader = csv.DictReader(StringIO(file.data_file.read().decode()))
            else: 
                reader = json.loads(file.data_file.read())
            row = list(reader)[form.cleaned_data['row']]
            kwargs = dict(row)
            print(template.template)
            jinja_template = Template(template.template)
            bootstrap = '''
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.2.1/lux/bootstrap.min.css" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
            <script src="https://unpkg.com/popper.js@1.12.6/dist/umd/popper.js" integrity="sha384-fA23ZRQ3G/J53mElWqVJEGJzU0sTs+SvzG8fXVWP+kJQ1lwFAOkcUOysnlKJC33U" crossorigin="anonymous"></script>
            <script src="https://unpkg.com/bootstrap-material-design@4.1.1/dist/js/bootstrap-material-design.js" integrity="sha384-CauSuKpEqAFajSpkdjv3z9t8E7RlpJ1UP0lKM/+NdtSarroVKu069AlsRPKkFBz9" crossorigin="anonymous"></script>'''
            return HttpResponse(bootstrap+jinja_template.render(**kwargs))
        else:
            return self.form_invalid(form, **kwargs)

