from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import GenerationJob, Certificate

from .serializers import (
    CertificateGenerationSerializer,
    GenerationJobSerializer,
    CertificateSerializer
)

from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.core.files.base import ContentFile

from io import BytesIO


class CertificateGenerationView(APIView):

    def post(self, request):

        # 1. Validate client data
        serializer = CertificateGenerationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            # 2. Create Generation Job
            job = GenerationJob.objects.create(
                event_name=serializer.validated_data['event_name'],
                total=len(serializer.validated_data['recipients'])
            )

            job.status = 'PROCESSING'
            job.save()

            # 3. Process each recipient
            for recipient in serializer.validated_data['recipients']:

                certificate = Certificate.objects.create(
                    job=job,
                    recipient_name=recipient['name'],
                    recipient_email=recipient['email']
                )

                try:

                    # 4. Prepare template data
                    context = {
                        'name': recipient['name'],
                        'event_name': serializer.validated_data['event_name']
                    }

                    # 5. Convert Django template into HTML
                    html_string = render_to_string(
                        'certificate.html',
                        context
                    )

                    # 6. Convert HTML into PDF
                    pdf_buffer = BytesIO()

                    pdf_result = pisa.CreatePDF(
                        html_string,
                        dest=pdf_buffer
                    )

                    # 7. Check PDF generation error
                    if pdf_result.err:
                        raise Exception(
                            "PDF generation failed"
                        )

                    pdf = pdf_buffer.getvalue()

                    # 8. Create filename
                    filename = (
                        f"{recipient['name']}_certificate.pdf"
                    )

                    # 9. Save PDF
                    certificate.file.save(
                        filename,
                        ContentFile(pdf),
                        save=True
                    )

                    # 10. Mark certificate as successful
                    certificate.status = 'SUCCESS'
                    certificate.save()

                    # 11. Update successful count
                    job.successful += 1
                    job.save()

                except Exception as e:

                    # 12. Mark this certificate as failed
                    certificate.status = 'FAILED'
                    certificate.error = str(e)
                    certificate.save()

                    # 13. Update failed count
                    job.failed += 1
                    job.save()

                    # Important:
                    # Do not stop the loop.
                    # Next recipient will still be processed.

            # 14. All recipients processed
            job.status = 'COMPLETED'
            job.save()

            # 15. Return response
            return Response(
                {
                    "message": "Certificates generated successfully",
                    "job_id": job.id
                },
                status=status.HTTP_200_OK
            )

        # 16. Invalid request data
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GenerationJobDetailView(APIView):

    def get(self, request, job_id):

        try:

            # Find job
            job = GenerationJob.objects.get(
                id=job_id
            )

        except GenerationJob.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Convert job object to JSON
        serializer = GenerationJobSerializer(job)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class JobCertificatesView(APIView):

    def get(self, request, job_id):

        try:

            # Find job
            job = GenerationJob.objects.get(
                id=job_id
            )

        except GenerationJob.DoesNotExist:

            return Response(
                {
                    "error": "Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Get certificates belonging to this job
        certificates = Certificate.objects.filter(
            job=job
        )

        # Convert certificates to JSON
        serializer = CertificateSerializer(
            certificates,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
class CertificateDetailView(APIView):

    def get(self, request, certificate_id):

        try:

            certificate = Certificate.objects.get(
                id=certificate_id
            )

        except Certificate.DoesNotExist:

            return Response(
                {
                    "error": "Certificate not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CertificateSerializer(
            certificate
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )        
        
        
        
        
