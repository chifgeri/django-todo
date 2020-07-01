from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, edit
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import TodoItem
from .serializers import TodoItemSerializer
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
        context['max_prior'] = TodoItem.get_max_priority()
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

def remove(request, todo_id):
    todo = TodoItem.objects.get(pk=todo_id)
    todo.delete()

    return HttpResponseRedirect(reverse('list'))

def check(request, todo_id):
    todo = get_object_or_404(TodoItem, pk=todo_id)
    if request.POST.get('check', False):
      todo.check_todo()
    else:
      todo.uncheck()

    return HttpResponseRedirect(reverse('list'))


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all().order_by('-priority')
    serializer_class = TodoItemSerializer

    def create(self, request):
        serializer = TodoItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            max_prior = TodoItem.get_max_priority()
            new_todo = TodoItem.objects.create(text=data['text'], priority=max_prior+1)
            return Response(TodoItemSerializer(new_todo).data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response("Can't create this todo", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["POST"])
    def check(self, request, pk):
        try:
            todo = TodoItem.objects.get(pk=pk)
            with transaction.atomic():
                before = todo.done
                if todo.done == False:
                    todo.check_todo()
                else:
                    todo.uncheck()
            if before == todo.done:
                return Response("Can't check or uncheck this todo", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_200_OK)
        except TodoItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["POST"])
    def move(self, request, pk):
        try:
            todo = TodoItem.objects.get(pk=pk)
            with transaction.atomic():
                if 'direction' in request.data:
                    if request.data['direction'] == 'up':
                        todo.update_priority('increment')
                    elif request.data['direction'] == 'down':
                        todo.update_priority('decrease')
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        except TodoItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
