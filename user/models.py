from django.db import models

#Models inherit from django.db.models.Model
#basic model structure 
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)

#model methods
# 1. properties
# written with the @property decorator
# used to define a method that can be accessed like an attribute
# they are evaluated when accessed(after data has been fetched from the database), not stored in the database
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" or f"{self.username}"
        # queried as User.objects.all().<method_name>() e.g User.objects.all().get_full_name()