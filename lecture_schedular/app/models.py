from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import InstructorManager


class Instructor(AbstractBaseUser):
    ROLE_CHOICES = [
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
        # Add more roles as needed
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    contact = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Admin')



    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = InstructorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "contact"]

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
         return self.is_superuser
    


class Course(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    
    def __str__(self):
        return self.name



class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.CharField( max_length=50)

    def __str__(self):
        return self.batch_name
    


class Lecture(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.instructor
    
    
    
    

