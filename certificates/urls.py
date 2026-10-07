from django.urls import path

from .views import (
    CertificateGenerationView,
    GenerationJobDetailView,
    JobCertificatesView
)

urlpatterns = [

    path(
        'certificates/generate/',
        CertificateGenerationView.as_view(),
        name='generate-certificates'
    ),

    path(
        'jobs/<int:job_id>/',
        GenerationJobDetailView.as_view(),
        name='job-detail'
    ),

    path(
        'jobs/<int:job_id>/certificates/',
        JobCertificatesView.as_view(),
        name='job-certificates'
    ),
]