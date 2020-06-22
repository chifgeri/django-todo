from django.db import models

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
      self.save()

