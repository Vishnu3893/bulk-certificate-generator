from rest_framework import serializers

from .models import GenerationJob,Certificate


class RecipientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()


class CertificateGenerationSerializer(serializers.Serializer):
    event_name = serializers.CharField(max_length=200)
    recipients = RecipientSerializer(many=True)


class GenerationJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenerationJob
        fields = [
            'id',
            'event_name',
            'status',
            'total',
            'successful',
            'failed',
            'created_at'
        ]
class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = [
            'id',
            'recipient_name',
            'recipient_email',
            'status',
            'file',
            'error',
            'created_at'
        ]        