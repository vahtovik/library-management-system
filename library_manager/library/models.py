from django.db import models


class Book(models.Model):
    STATUS_CHOICES = [
        ('в наличии', 'в наличии'),
        ('выдана', 'выдана'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f'{self.title}, {self.author} ({self.year})'
