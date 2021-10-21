from django.urls import path
from .views import CreateListStudent, UpdateDeleteStudent, HomeView, Download

urlpatterns = [
    path("student", CreateListStudent.as_view(), name="student"),
    path("student/<int:pk>", UpdateDeleteStudent.as_view()),
    path('',HomeView.as_view()),
    path('download',Download.as_view())
]