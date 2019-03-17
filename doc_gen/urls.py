from django.urls import path
from . import views

urlpatterns = [
    path("document/", views.DocumentListView.as_view(), name="doc-view"),
    path("document/add/", views.DocumentCreateView.as_view(), name="doc-add"),
    path("document/<pk>/", views.DocumentMetaDetailView.as_view(), name="doc-detail"),
    path("document/<pk>/update/", views.DocumentUpdateView.as_view(), name="doc-update"),
    path("document/<pk>/delete/", views.DocumentDeleteView.as_view(), name="doc-delete"),
    path("document_meta/<pk>/delete/", views.DocumentMetaDeleteView.as_view(), name="doc-meta-delete"),

    path("template/", views.TemplateListView.as_view(), name="template-view"),
    path("template/add/<pk>", views.TemplateCreateView.as_view(), name="template-add"),
    path("template/add/", views.TemplateCreateView.as_view(), name="template-add"),
    path("template/<pk>", views.TemplateDetailView.as_view(), name='template-detail'),
    path("template/<pk>/update/", views.TemplateUpdateView.as_view(), name="template-update"),
    path("template/<pk>/delete/", views.TemplateDeleteView.as_view(), name="template-delete"),

    path('generate/', views.GenerateDocumentView.as_view(), name='generate'),
]
