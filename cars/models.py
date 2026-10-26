from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.DateField()
    price = models.IntegerField()
    mileage = models.IntegerField()
    fuel = models.CharField(max_length=30)
    image = models.ImageField(upload_to="cars/")
    description = models.TextField()

    def __str__(self):
        return f"{self.brand} {self.name}"


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    card_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.car}"
