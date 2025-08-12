from django.db import models
from django.utils.functional import cached_property


# Basic model structure
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    age = models.PositiveIntegerField(null=True, blank=True)

# ====================================================================================META CLASS===========================================================================
# Meta class is used to define metadata for the model
# such as ordering, verbose name, and other options
# https://docs.djangoproject.com/en/5.2/ref/models/options/
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']  # Default ordering by date joined, newest first

# =========================================================================================================================================================================
# =================================================================================MODEL METHODS==============================================================================
# =========================================================================================================================================================================
# Model methods are functions defined within a model class that can be used to perform operations on the model instances.
# They can be used to encapsulate business logic, perform calculations, or interact with the database.
# Model methods can be categorized into several types:
# 1. Property methods: Used for computed fields that should behave like attributes.
# 2. Instance methods: For operations on individual records.
# 3. Static methods: For operations that don't require an instance.
# 4. Class methods: For operations that need to access the model class itself.
# 5. Lifecycle methods: Called at specific points in the object's lifecycle, such as before saving or deleting an object.

# https://www.notion.so/Model-Methods-245789469f8880d885c3f09b96ee01ff

# ===============================================================================__str__ & __repr__=======================================================================
# __str__ is used to define the string representation of the model instance
    def __str__(self):
        return self.username or f"{self.first_name} {self.last_name}"
        # queried as str(User) e.g str(User.objects.first())
# __repr__ is used to define the official string representation of the model instance
    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
        # queried as repr(User) e.g repr(User.objects.first())

# ===============================================================================Property Methods========================================================================
# Used for computed fields that should behave like attributes
# Evaluated when accessed(after data has been fetched from the database), not stored in the database
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" or f"{self.username}"
        # queried as User.objects.all().<method_name>() e.g User.objects.all().get_full_name()
# Cached property methods can be used to store the result of a computation
    @cached_property
    def is_adult(self):
        return self.age is not None and self.age >= 18
        # queried as User.objects.all().<method_name>() e.g User.objects.all().is_adult()
    
    def invalidate_cache(self):
        """
        Invalidate the cached property.
        This is useful if the underlying data changes and you want to refresh the cached value.
        """
        if hasattr(self, 'is_adult'):
            del self.is_adult
        # This will remove the cached property, forcing it to be recalculated next time it's accessed

# ===============================================================================Instance Methods========================================================================
# For operations on individual records
# these are methods that can be called on the model instance
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" or f"{self.username}"
    
    def is_older_than(self, age):
        return self.age is not None and self.age > age
        # queried as User.objects.all().<method_name>() e.g User.objects.all().is_older_than(10)

# ===============================================================================Static Methods========================================================================
# For operations that don't require an instance
# These methods are not tied to a specific instance of the model
    @staticmethod
    def get_user_count():
        return User.objects.count()
        # queried as User.get_user_count() e.g User.get_user_count()
# ==============================================================================Class Methods=========================================================================
# For operations that need to access the model class itself
# These methods are bound to the class, not the instance
# These operate on the model class itself, useful for alternative constructors:
    @classmethod
    def create_user(cls, username, first_name=None, last_name=None, email=None):
        return cls.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
        # queried as User.create_user('new_user') e.g User.create_user()

# =============================================================================Lifecycle Methods=========================================================================
# These methods are called at specific points in the object's lifecycle
# Examples include:
# - `save()` is called before an object is saved to the database
# - `delete()` is called before an object is deleted from the database
    def save(self, *args, **kwargs):
        # Custom logic before saving
        super().save(*args, **kwargs)  # Call the original save method

    def delete(self, *args, **kwargs):
        # Custom logic before deleting
        super().delete(*args, **kwargs)  # Call the original delete method
    
    def clean(self):
        # Custom validation logic before saving
        if not self.username:
            raise ValueError("Username cannot be empty")
        if self.age is not None and self.age < 0:
            raise ValueError("Age cannot be negative")
        super().clean()

# =============================================================================Meta Methods===============================================================================
# Comparison methods allow you to define how model instances are compared
# These methods are used to compare model instances for equality and ordering
    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id
    def __lt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.date_joined < other.date_joined
# others include __ne__ (not equal), __gt__ (greater than), __le__ (less than or equal), __ge__ (greater than or equal)

# Hash and iter methods allow you to define how model instances are hashed and iterated
    def __hash__(self):
        return hash(self.id)
    
    def __iter__(self):
        yield from (self.first_name, self.last_name, self.username, self.email, self.date_joined, self.age)
        # This allows you to iterate over the model instance like a tuple
        return iter((self.first_name, self.last_name, self.username, self.email, self.date_joined, self.age))

# ======================================================================================================================================================================
# =========================================================================MODEL INHERITANCE=============================================================================
# ======================================================================================================================================================================
# Model inheritance allows you to create a base model with common fields and methods
# and then create child models that inherit from it.
# Models inherit from django.db.models.Model
# There are three types of model inheritance in Django:
# 1. Abstract Base Classes
# 2. Multi-table Inheritance
# 3. Proxy Models

# =============================================================================ABSTRACT BASE CLASSES==========================================================================
# Abstract models are used to define common fields and methods that can be inherited by other models
# They are not created as separate database tables, but their fields are included in the child models
class BaseUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        abstract = True  # This model will not create a table in the database

class UserProfile(BaseUser):
    username = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    age = models.PositiveIntegerField(null=True, blank=True)

# ==========================================================================MULTI-TABLE INHERITANCE===========================================================================
# Multi-table inheritance allows you to create a base model that is stored in its own table,
# and child models that have a one-to-one relationship with the base model.


# ===========================================================================PROXY MODELS========================================================================================
# Proxy models allow you to change the behavior of a model without changing its fields or database table
# They are useful for adding custom methods or changing the default ordering of a model