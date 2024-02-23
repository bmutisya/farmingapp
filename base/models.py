from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Animal(models.Model):
    COW = 'cow'
    BULL = 'bull'
    HEIFER = 'heifer'
    CALF = 'calf'

    ANIMAL_TYPE_CHOICES = [
        (COW, 'Cow'),
        (BULL, 'Bull'),
        (HEIFER, 'Heifer'),
        (CALF, 'Calf'),
    ]
    farmer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True) #a farmer will have more than one animal
    animal_id = models.CharField(max_length=50, unique=True)
    animal_name = models.CharField(max_length=100)
    ear_tag = models.CharField(max_length=50, null=True, blank=True)
    sire_id = models.CharField(max_length=50,  null=True, blank=True)
    dam_id = models.CharField(max_length=50, null=True, blank=True)
    animal_type = models.CharField(max_length=100, choices=ANIMAL_TYPE_CHOICES)
    color = models.CharField(max_length=50,  null=True, blank=True)
    breed = models.CharField(max_length=100,  null=True, blank=True)
    description=models.TextField( null=True, blank=True)
    date_of_birth = models.DateField( null=True, blank=True)
    current_age = models.IntegerField( null=True, blank=True)  # In months, years, or any other appropriate unit
    weight_at_birth = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True)  # In whatever appropriate unit
    age_at_first_service = models.IntegerField( null=True, blank=True)  # In months, years, or any other appropriate unit
    weight_at_first_service = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # In whatever appropriate unit
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.animal_name
    
    class Meta:
        ordering =['complete']
    
    #Second db table  of animal health
class AnimalHealth(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date =models.DateField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    cost = models.CharField(max_length=100,null=True, blank=True)
    vet_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.animal.animal_name} - {self.date}"
    
class MilkRecord(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    milking_date = models.DateField()
    morning_milk = models.DecimalField(max_digits=6, decimal_places=2) 
    afternoon_milk = models.DecimalField(max_digits=6, decimal_places=2)  
    evening_milk = models.DecimalField(max_digits=6, decimal_places=2)   
    
    def __str__(self):
        return f"Milk Record for {self.animal.animal_name}"