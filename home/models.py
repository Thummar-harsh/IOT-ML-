from django.db import models

class size_data(models.Model):
    x = models.DecimalField(max_digits=10, decimal_places=2)
    y = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    class Meta:
        verbose_name = "data detils"
        verbose_name_plural = "data detils"
        
