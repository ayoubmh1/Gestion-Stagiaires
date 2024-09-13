from django.db import models

# Create your models here.

class Administrateur(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
