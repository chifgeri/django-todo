from django import forms
from .models import TodoItem

class TodoCreateForm(forms.Form):
  text = forms.CharField(max_length=50, required=True)

  def create_todo(self):
      priority = TodoItem.get_max_priority()
      todo = TodoItem(text=self.data['text'], priority=priority)
      todo.save()
