from django.db.transaction import atomic
from django_eventstream import send_event
from rest_framework import serializers

from .models import SnortLog, snort_type


class SnortLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnortLog
        fields = '__all__'
        extra_kwargs = {
            'type': {'required': False},
        }

    @atomic
    def create(self, data):
        type = snort_type.get(data['sid'])
        log = SnortLog.objects.create(**data, type=type)
        send_event(
            channel="snort",
            event_type="event",
            data={
                'type': type,
                'ip': log.ip,
                'date': log.date,
            }
        )
        return log