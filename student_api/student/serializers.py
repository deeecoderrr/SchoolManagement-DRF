from rest_framework import serializers
from .models import Student

import logging

logger = logging.getLogger("django")


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def validate(self, attrs):

        # phone number validation
        if len(str(attrs.get("parent_mobile"))) != 10:
            logger.error(
                f"Phone number validation failed for {attrs.get('parent_mobile')}"
            )
            raise serializers.ValidationError(
                {"parent_mobile": "Enter valid 10 digit mobile number."}
            )
        return super().validate(attrs)
