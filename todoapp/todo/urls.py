from django.urls import path
from .views import TodoListView, CreateTodo, increment, decrease, remove, check, TodoItemViewSet
from rest_framework import routers

urlpatterns = [
    path('', TodoListView.as_view(), name='list'),
    path('create', CreateTodo.as_view(), name='create'),
    path('<int:todo_id>/increment', increment, name = 'increment'),
    path('<int:todo_id>/decrease', decrease, name='decrease'),
    path('<int:todo_id>/remove', remove, name='remove'),
    path('<int:todo_id>/check', check, name='check'),
]

todorouter = routers.DefaultRouter()
todorouter.register(r'todos',TodoItemViewSet)
