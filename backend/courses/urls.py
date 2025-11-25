from django.urls import path
from .views import CoursesListView

urlpatterns = [
    path('courses/', CoursesListView.as_view(), name='courses-list'),
]
