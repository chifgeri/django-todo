from django.shortcuts import render
from django.views.generic import ListView
from .models import TodoItem

# Create your views here.
class TodoListView(ListView):
    model = TodoItem
    template_name = "todo/todo_list.html"
    context_object_name = 'todo_list'
    
    def get_queryset(self):
        return super().get_queryset()
    