from django.test import TestCase
from rest_framework.test import APIClient

from .models import GenerationJob, Certificate


class CertificateGenerationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    # Test 1: Valid certificate generation
    def test_valid_certificate_generation(self):

        data = {
            "event_name": "Python Workshop",
            "recipients": [
                {
                    "name": "Vishnu",
                    "email": "vishnu@gmail.com"
                },
                {
                    "name": "Rahul",
                    "email": "rahul@gmail.com"
                }
            ]
        }

        response = self.client.post(
            "/api/certificates/generate/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            GenerationJob.objects.count(),
            1
        )

        self.assertEqual(
            Certificate.objects.count(),
            2
        )

    # Test 2: Invalid email
    def test_invalid_email(self):

        data = {
            "event_name": "Python Workshop",
            "recipients": [
                {
                    "name": "Vishnu",
                    "email": "wrong-email"
                }
            ]
        }

        response = self.client.post(
            "/api/certificates/generate/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "email",
            response.data["recipients"][0]
        )
    def test_job_status(self):

        job = GenerationJob.objects.create(
            event_name="Python Workshop",
            status="COMPLETED",
            total=2,
            successful=2,
            failed=0
        )

        response = self.client.get(
            f"/api/jobs/{job.id}/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["event_name"],
            "Python Workshop"
        )

        self.assertEqual(
            response.data["status"],
            "COMPLETED"
        )

        self.assertEqual(
            response.data["total"],
            2
        )

        self.assertEqual(
            response.data["successful"],
            2
        )

        self.assertEqual(
            response.data["failed"],
            0
        )
    def test_certificate_retrieval(self):

        job = GenerationJob.objects.create(
            event_name="Python Workshop",
            status="COMPLETED",
            total=2,
            successful=2,
            failed=0
        )

        Certificate.objects.create(
            job=job,
            recipient_name="Vishnu",
            recipient_email="vishnu@gmail.com",
            status="SUCCESS"
        )

        Certificate.objects.create(
            job=job,
            recipient_name="Rahul",
            recipient_email="rahul@gmail.com",
            status="SUCCESS"
        )

        response = self.client.get(
            f"/api/jobs/{job.id}/certificates/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            2
        )

        self.assertEqual(
            response.data[0]["recipient_name"],
            "Vishnu"
        )

        self.assertEqual(
            response.data[1]["recipient_name"],
            "Rahul"
        )       