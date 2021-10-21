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

class CreateListStudent(APIView):
    
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = []
        for i in range(100):
            first_name = randoem_name()
            last_name = randoem_name()
            request.data.update({"first_name": first_name, "last_name":last_name})
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data.append(serializer.data)
        return Response(data)
    
        
class UpdateDeleteStudent(APIView):
    
    def get_object(self, pk):
        try:
            student = Student.objects.get(id=pk)
            return student
        except Exception as e:
            return False
        
    def put(self, request, pk=None):
        try:
            student = self.get_object(pk)
            if student:
                serializer = StudentSerializer(student ,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                return Response({'mesg': "NO student found"},
                    status=404)
        except Exception as e:
            return Response({'mesg': str(e)},
                            status=404)

    def delete(self, request, pk=None):
        try:
            student = self.get_object(pk)
            if student:
                student.delete()
                return Response({'mesg':"student data Deleted"},
                            status=200)
            else:
                return Response({'mesg': "NO student found"},
                    status=404)
        except Exception as e:
            return Response({'mesg': str(e)},
                    status=404)
            
            
            
class HomeView(View):
    template = 'api/index.html'
    
    def get(self, request, lot=None):
        return render(request, self.template, locals())
    
    
class Download(APIView):
    
    def get(self, request):
        rows =  Student.objects.all()
        def stream():
            buffer_ = io.StringIO()
            writer = csv.writer(buffer_)
            for row in rows:
                print(row,'+++++++++++++++++++++++++')
                writer.writerow({"first_name": row.first_name})
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
        # writer = csv.DictWriter(response, fieldnames=["email"])
        # writer.writeheader()
        # writer.writerow({"first_name": email.email})
        return response
        