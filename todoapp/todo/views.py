from django.shortcuts import render
from django.views.generic import ListView, edit
from .models import TodoItem
from .forms import TodoCreateForm

# Create your views here.
class TodoListView(ListView):
    model = TodoItem
    template_name = "todo/todo_list.html"
    context_object_name = 'todo_list'
    
    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['add_form'] = TodoCreateForm()
        return context

class CreateTodo(edit.FormView):
    template_name = 'todo/todo_create.html'
    form_class = TodoCreateForm
    success_url = '/todos'

    def form_valid(self, form):
        form.create_todo()
        return super().form_valid(form)