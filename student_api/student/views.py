from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from .authentication import CustomTokenAuthentication
from .connector import get_teacher_name

import logging

logger = logging.getLogger("django")


class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [SessionAuthentication, CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    # override retricve method to add class teacher name to the response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        new_data = serializer.data
        new_data.update(
            {
                "class_teacher_name": get_teacher_name(
                    serializer.data.get("class_teacher_id")
                )
            }
        )
        logger.info(
            f"Class teacher name fetched successfully updated to the response: {new_data}"
        )
        return Response(new_data)
