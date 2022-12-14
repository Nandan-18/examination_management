from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.batch.api.v1.serializers import BatchSerializer
from examination_management.batch.models import Batch


class BatchCreateView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Batch.objects.create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class BatchDetailView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        student = Batch.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Batch with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class BatchListView(GenericAPIView):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        roll_no = request.GET.get('roll_no', None)
        # batch = request.GET.get('batch', None)
        # branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        students = queryset
        if roll_no:
            students = queryset.filter(roll_no=roll_no)

        response = {
            'error': False,
            'data': self.get_serializer(students, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class BatchUpdateView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Batch.objects.get(id=id)
        if not student:
            response = {
                'error': True,
                'message': f'Batch with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student = student.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class BatchDeleteView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        student = Batch.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Batch with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student.is_deleted = True
        student.save()

        response = {
            'error': False,
            'message': f'Batch with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)