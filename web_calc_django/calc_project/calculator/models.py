from django.db import models

class Operation(models.Model):
    operation = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation} = {self.result}"
