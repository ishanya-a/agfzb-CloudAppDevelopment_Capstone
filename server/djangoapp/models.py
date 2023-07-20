from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    founding_year = models.PositiveIntegerField()
    headquarters = models.CharField(max_length=200)
    website = models.URLField()

    def __str__(self):
        return self.name




# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    CAR_TYPE_CHOICES = (
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('wagon', 'Wagon'),
    )
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    year = models.DateField()
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=1)
    transmission = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_model_images/')  # Requires Pillow library for image field

    def __str__(self):
        return self.name



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data


# def clean_data():
#     # Delete all data to start from fresh
#     Enrollment.objects.all().delete()
#     User.objects.all().delete()
#     Learner.objects.all().delete()
#     Instructor.objects.all().delete()
#     Course.objects.all().delete()
#     Lesson.objects.all().delete()

# def write_lessons():
#     # Add lessons
#     lession1 = Lesson(title='Lesson 1', content="Object-relational mapping project")
#     lession1.save()
#     lession2 = Lesson(title='Lesson 2', content="Django full stack project")
#     lession2.save()
#     print("Lesson objects all saved... ")

class CarDealer:

    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer state
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name
        

    def __str__(self):
        return "Dealer name: " + self.full_name