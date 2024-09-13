from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

User = get_user_model()


class Stagiaire(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True, null=True)
    ecole = models.CharField(max_length=50, blank=True, null=True)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    filiere = models.CharField(max_length=20, blank=True, null=True)
    niveau = models.CharField(max_length=20, blank=True, null=True)

    def is_absent_on(self, date):
        return Absence.objects.filter(stagiaire=self, date=date).exists()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Stage(models.Model):
    type_de_stage = models.CharField(max_length=20)
    sujet = models.CharField(max_length=50)
    description = models.TextField()
    date_de_debut = models.DateField()
    date_de_fin = models.DateField()
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sujet

class Encadreur(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    specialite = models.CharField(max_length=20)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Projet_realise(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    encadreur = models.ForeignKey(Encadreur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=50)
    description = models.TextField()
    fichier = models.FileField(upload_to='projets/', blank=True, null=True) 
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class Application(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    encadreur = models.ForeignKey(Encadreur, on_delete=models.SET_NULL, null=True, blank=True) 
    date_de_candidature = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('accepté', 'Accepté'), ('refusé', 'Refusé')], default='en attente')

    def __str__(self):
        return f"{self.stagiaire} - {self.stage}"


class ProgressUpdate(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    next_steps = models.TextField(blank=True)

    def __str__(self):
        return f"Progress update for {self.stagiaire.nom} on {self.date}"
    
class FileUpload(models.Model):
    TRAINEE_REPORT = 'rapport'
    PRESENTATION = 'presentation'
    STAGE_CONVENTION = 'convention'

    FILE_TYPE_CHOICES = [
        (TRAINEE_REPORT, 'Rapport de Stage'),
        (PRESENTATION, 'Presentations'),
        (STAGE_CONVENTION, 'Convention de Stage'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_file_type_display()}"

    def file_extension(self):
        return self.file.name.split('.')[-1]

    def is_valid_extension(self):
        valid_extensions = {
            'rapport': ['pdf'],
            'presentation': ['pptx', 'pdf'],
            'convention': ['pdf']
        }
        return self.file_extension() in valid_extensions[self.file_type]

class Absence(models.Model):
    ABSENCE_CHOICES = [
        ('absent', 'Absent'),
        ('retard', 'Retard'),
        ('quitter', 'Quitter le stage'),
    ]

    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ABSENCE_CHOICES)

    def __str__(self):
        return f"{self.stagiaire} - {self.date} - {self.status}"

class CertificateRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'En attente'),
        (APPROVED, 'Approuvé'),
        (REJECTED, 'Rejeté'),
    ]

    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.stagiaire} - {self.status}"