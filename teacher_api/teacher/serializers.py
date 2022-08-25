from rest_framework import serializers
from .models import Teacher

import logging

logger = logging.getLogger("django")


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

    def validate(self, attrs):
        # phone number validation
        if len(str(attrs.get("phone_number"))) != 10:
            logger.error(
                f"Phone number validation failed for {attrs.get('phone_number')}"
            )
            raise serializers.ValidationError(
                {"phone_number": "Enter valid 10 digit mobile number."}
            )
        return super().validate(attrs)
