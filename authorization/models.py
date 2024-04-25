from django.db import models
from django.conf import settings

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    






class File(models.Model):
    file = models.FileField(upload_to='csvfile/', max_length=250, null=True, default=None)
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='file')
    


# class DataUpload(models.Model):
#     cl1=models.CharField(max_length=255)
#     cl2=models.CharField(max_length=255)
#     user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='+')
    

class DataUpload(models.Model):
    cl1 = models.FloatField(max_length=255)
    cl2 = models.FloatField(max_length=255)
    tablename = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', default=None)



