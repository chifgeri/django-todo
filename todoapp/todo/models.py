from django.db import models
from django.db.models import Max

# Create your models here.
class TodoItem(models.Model):
    text = models.CharField(blank=False, null=False, max_length=100)
    done = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField()
    

    class Meta:
        verbose_name = "TodoItem"
        verbose_name_plural = "TodoItems"

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("todoitem_detail", kwargs={"pk": self.pk})

    def check_todo(self):
      self.done = True
      self.priority = 0
      self.reprioritize()
      self.save()
    
    def reprioritize(self):
      items = TodoItem.objects.filter(priority__gt=self.priority)
      for item in items:
        print(item)
        item.priority = item.priority - 1
        item.save()
    
    @classmethod
    def get_max_priority(cls):
        max_prior = cls.objects.aggregate(Max('priority'))
        max_val = max_prior['priority__max']
        if max_val is None:
          return 0
        else:
          return max_val

