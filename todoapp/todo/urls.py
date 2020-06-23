from django.urls import path
from .views import TodoListView, CreateTodo

urlpatterns = [
    path('', TodoListView.as_view(), name='list'),
    path('create', CreateTodo.as_view(), name='create'),
]
