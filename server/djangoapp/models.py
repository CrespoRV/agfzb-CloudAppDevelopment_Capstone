from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null = False, max_length=30)
    description = models.TextField()
    country_origin = models.CharField(max_length= 20)

    def __str__(self):
        return self.name + " " + self.description + " " + self.country_origin



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    
    SEDAN = "Sedan"
    SUV = 'Suv'
    WAGON = "Wagon"
    HATCHBACK = "Hatchback"
    
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon'),
        (HATCHBACK, 'Hatchback')
    ]

    name = models.CharField(null = False, max_length= 50)
    mtype = models.CharField(null = False,
                             max_length = 30,
                             choices = TYPE_CHOICES,
                             default = 'Sedan'
    )
    year = models.DateField()
    dealer_id = models.IntegerField()
    car_make = models.ForeignKey(CarMake,null = False, on_delete = models.CASCADE)
    
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "MType: " + self.mtype + ", " + \
               "Dealer: " + str(self.dealer_id) + ", " + \
               "Year " + str(self.year)



# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, address, city, full_name, idcar, lat, lon, short_name, st, zi):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.idcar = idcar
        # Location lat
        self.lat = lat
        # Location long
        self.lon = lon
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zi = zi

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:

    def __init__(self, ds, name, purchase, review, purchase_date, car_make, car_model, car_year, idr):
   
        self.ds = ds
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = ""
        self.idr = idr

    def __str__(self):
        return "Review to: " + self.name + ", Carmake: " + self.car_make

