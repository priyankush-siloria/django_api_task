from django.shortcuts import render
from rest_framework.views import APIView
from .models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from .utils import randoem_name
from django.views import View
from django.http import StreamingHttpResponse
import csv
import io
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status







class HomeView(View):
    """
    View for download button page
    """
    template = 'api/index.html'
    
    def get(self, request, lot=None):
        return render(request, self.template, locals())
    




class CreateListStudent(APIView):
    """
    APi view for create and list student 
    """
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = []
        context = {}
        for i in range(1000):
            student_dtls = {}
            student_dtls['first_name'] = randoem_name()
            student_dtls['last_name'] = randoem_name()
            data.append(student_dtls)
        serializer = StudentSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            context['data'] = serializer.data
            context['status'] = True
            status_code = status.HTTP_201_CREATED
            context['message'] = "All Student data created"
            return Response(context, status=status_code)
    
        
class UpdateDeleteStudent(APIView):
    """
    Api view for update and delete student
    """
    def get_object(self, pk):
        try:
            student = Student.objects.get(id=pk)
            return student
        except Exception as e:
            return False
        
    def put(self, request, pk=None):
        context = {}
        try:
            student = self.get_object(pk)
            if student:
                serializer = StudentSerializer(student ,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    context['data'] = serializer.data
                    context['status'] = True
                    status_code = 200
                    context['message'] = "Student data Updated"
                    return Response(context, status=status_code)
                return Response(serializer.errors, status=400)
            else:
                return Response({'mesg': "NO student found"},
                    status=404)
        except Exception as e:
            context['data'] = []
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            context['message'] = str(e)
            return Response(context, status=status_code)

    def delete(self, request, pk=None):
        context = {}
        try:
            student = self.get_object(pk)
            if student:
                student.delete()
                context['data'] = []
                context['status'] = True
                status_code = 200
                context['message'] = "Student data delete"
                return Response(context, status=status_code)
                
            else:
                return Response({'mesg': "NO student found"},
                    status=404)
        except Exception as e:
            context['data'] = []
            context['status'] = False
            status_code = status.HTTP_400_BAD_REQUEST
            context['message'] = str(e)
            return Response(context, status=status_code)
            

class Download(APIView):
    """
    View for download student details as a streaming 
    """
    def get(self, request):
        rows =  Student.objects.all()
        header = ['id','first name', 'last name']
        def stream():
            buffer_ = io.StringIO()
            writer = csv.writer(buffer_)
            writer.writerow(header)
            for row in rows:
                data_list = [row.id, row.first_name, row.last_name]
                writer.writerow(data_list)
                buffer_.seek(0)
                data = buffer_.read()
                buffer_.seek(0)
                buffer_.truncate()
                yield data

        response = StreamingHttpResponse(
            stream(), content_type='text/csv'
        )
        disposition = "attachment; filename=file.csv"
        response['Content-Disposition'] = disposition
        return response
        