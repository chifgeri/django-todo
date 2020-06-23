from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, edit
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import TodoItem
from .forms import TodoCreateForm

# Create your views here.
class TodoListView(ListView):
    model = TodoItem
    template_name = "todo/todo_list.html"
    context_object_name = 'todo_list'
    
    def get_queryset(self):
        return super().get_queryset().order_by('-priority')
    
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


def increment(request, todo_id):
    todo = get_object_or_404(TodoItem, pk=todo_id)
    todo.update_priority('increment')

    return HttpResponseRedirect(reverse('list'))

def decrease(request, todo_id):
    todo = get_object_or_404(TodoItem, pk=todo_id)
    todo.update_priority('decrease')

    return HttpResponseRedirect(reverse('list'))