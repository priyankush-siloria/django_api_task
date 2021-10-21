from django.urls import path
from .views import CreateListStudent, UpdateDeleteStudent, HomeView, Download, DummyPage
from .apps import ApiConfig

app_name = ApiConfig.name

urlpatterns = [
    path("student", CreateListStudent.as_view(), name="student"),
    path("student/<int:pk>", UpdateDeleteStudent.as_view()),
    path('',HomeView.as_view(), name="home"),
    path('download',Download.as_view()),
    path('dummy', DummyPage.as_view())
]