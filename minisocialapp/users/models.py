from datetime import date
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

#We want user to be able to chose gender only from this tuple.
GENDERS = (
    ('M', 'Male'), 
    ('F', 'Female'), 
    ('D', 'Disabled'),
)

#Function calculates user's age based on his birth date.
#It uses principle: int(True) = 1 and also int(False) = 0
def calculate_age(birth):
        today = date.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

class Profile(models.Model):

    #Fields that will be stored in a database, keeping information about
    #user's profile. Fields that have both null=True and blank=True can
    #be left blank and are not required to be filled if user don't want
    #to. Image will be assigned as default if user won't provide one.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null = True, blank=True)
    age = models.IntegerField(null = True, blank=True, editable=False)
    town = models.CharField(max_length=200, null = True, blank=True)
    country = models.CharField(max_length=200, null = True, blank=True)
    company = models.CharField(max_length=200, null = True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDERS, null = True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    #How object will be printed if referred to
    def __str__(self):
        return f'{self.user.username} Profile'

    #We need to override save method to provide our own functionality
    def save(self, *args, **kwargs):

        #We do't want user to be able to set his age on his own to avoid
        #it being different from his actual age calculated from his birth date.
        #So as we set editable=False on the field before, now we need to calculate
        #it on our own and save it to database.
        if self.birth_date:
            self.age = calculate_age(self.birth_date)
        super().save(*args, **kwargs)

        #To avoid keeping large profile pictures on server we need to resize them,
        #before storing them in our database. 
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)