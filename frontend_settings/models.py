from django.db import models


# Create your models here.
class Banner(models.Model):
    banner = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.banner.name


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject
