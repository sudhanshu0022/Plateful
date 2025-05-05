from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('AP', 'Appetizers'),
        ('MC', 'Main Course'),
        ('DS', 'Desserts'),
        ('BE', 'Beverages'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name