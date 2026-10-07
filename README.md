# Bulk Certificate Generator

## Project Overview

Bulk Certificate Generator is a Django REST API application that generates certificates for multiple recipients in a single request.

The application accepts an event name and a list of recipients. It validates the recipient information, creates certificates in PDF format, stores the generated files, and tracks the status of the generation job.

The system also allows users to check the status of a generation job and retrieve the certificates generated for that job.

## Features

- Generate certificates for multiple recipients
- Validate recipient names and email addresses
- Generate certificates in PDF format
- Store generated certificate files
- Track certificate generation jobs
- Track total, successful, and failed certificates
- Handle individual certificate generation failures
- Continue processing remaining recipients if one certificate fails
- Retrieve job status
- Retrieve certificates belonging to a job
- Open and download generated PDF certificates
- REST API support
- Automated tests

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- xhtml2pdf
- HTML
- REST API

## Project Structure

```text
certificate_project/
│
├── certificate_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── certificates/
│   ├── migrations/
│   ├── templates/
│   │   └── certificate.html
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── ...
│
├── media/
│   └── certificates/
│       └── generated PDF files
│
├── manage.py
└── README.md

## Database Models

### GenerationJob

`GenerationJob` represents one bulk certificate generation request.

Fields:

- `id`
- `event_name`
- `status`
- `total`
- `successful`
- `failed`
- `created_at`

Job statuses:

- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `FAILED`

### Certificate

`Certificate` represents an individual certificate generated for a recipient.

Fields:

- `id`
- `job`
- `recipient_name`
- `recipient_email`
- `status`
- `file`
- `error`
- `created_at`

Certificate statuses:

- `PENDING`
- `SUCCESS`
- `FAILED`

### Relationship

One `GenerationJob` can have multiple `Certificate` records.

```text
GenerationJob
      |
      | 1
      |
      |------ * Certificate



## Installation

### Step 1: Create a Virtual Environment

```bash
python -m venv .venv

### Step 2: Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate

## API Endpoints

### 1. Generate Certificates

**Method:** `POST`

**Endpoint:**

```text
/api/certificates/generate/

## Certificate Generation Flow

The certificate generation process follows these steps:

```text
Client
   |
   | POST Request
   v
Validate Request
   |
   v
Create Generation Job
   |
   v
Process Each Recipient
   |
   v
Create Certificate Record
   |
   v
Generate PDF
   |
   +------ SUCCESS
   |
   +------ FAILED
   |
   v
Update Job Statistics
   |
   v
Return Job ID

## Request Validation

The application validates the recipient information before generating certificates.

For example, if an invalid email address is provided:

```json
{
    "event_name": "Python Workshop",
    "recipients": [
        {
            "name": "Vishnu",
            "email": "wrong-email"
        }
    ]
}

## PDF Generation

The application uses `xhtml2pdf` to convert the HTML certificate template into a PDF file.

The certificate template is located at:

```text
certificates/templates/certificate.html

## Generated Files

Generated PDF files are stored inside:

```text
media/certificates/


## Error Handling

Each recipient is processed independently.

If certificate generation fails for one recipient:

1. The certificate status is changed to `FAILED`.
2. The error message is stored in the `error` field.
3. The failed count is increased.
4. The application continues processing the next recipient.

This prevents one failed certificate from stopping the complete bulk generation process.

## Job Status Tracking

The `GenerationJob` model tracks the overall certificate generation request.

The following information is stored:

- Total number of recipients
- Number of successful certificates
- Number of failed certificates
- Current job status

Example:

```text
Total       : 5
Successful  : 4
Failed      : 1
Status      : COMPLETED

## Testing

Automated tests are implemented in:

```text
certificates/tests.py
## Media Configuration

Generated certificate files are stored using Django media configuration.

The following settings are used:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


## API Architecture

The project follows a simple Django REST Framework architecture:

```text
Client
   |
   v
API URL
   |
   v
View
   |
   v
Serializer
   |
   v
Model
   |
   v
Database

## Future Improvements

The following features can be added in future versions:

- Background certificate processing
- Real-time progress tracking
- Multiple certificate templates
- Authentication and authorization
- Email certificates directly to recipients
- ZIP download for multiple certificates
- Improved certificate design
- API documentation using Swagger/OpenAPI

## Conclusion

The Bulk Certificate Generator is a Django REST API application that generates certificates for multiple recipients in a single request.

The project demonstrates the use of:

- Django
- Django REST Framework
- Models
- Serializers
- REST APIs
- Request validation
- PDF generation
- File handling
- Job status tracking
- Error handling
- Automated testing

The application provides a complete workflow for submitting certificate generation requests, generating PDF certificates, tracking job results, and retrieving generated certificates.