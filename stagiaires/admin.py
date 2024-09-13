import csv
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from .models import Stagiaire, Stage, Encadreur, Projet_realise, Application, ProgressUpdate, FileUpload, Absence, CertificateRequest
from .forms import AbsenceForm, CSVUploadForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError


User = get_user_model()


class AbsenceInline(admin.TabularInline):
    model = Absence
    form = AbsenceForm
    extra = 1


@admin.register(Stagiaire)
class StagiaireAdmin(admin.ModelAdmin):
    change_list_template = "admin/stagiaire_changelist.html"
    list_display = ['nom', 'prenom', 'email', 'telephone', 'ecole', 'abbreviation', 'filiere', 'niveau']
    search_fields = ('nom', 'prenom', 'email')
    inlines = [AbsenceInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='import-csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                try:
                    reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
                except UnicodeDecodeError:
                    reader = csv.DictReader(csv_file.read().decode('ISO-8859-1').splitlines())
                
                default_password = "3dsf2024"  # Default password for new users
                
                for row in reader:
                    try:
                        user, created = User.objects.get_or_create(
                            email=row['email'],
                            defaults={
                                'username': row['email'], 
                            }
                        )
                        if created:
                            user.set_password(default_password)
                            user.save()
                        Stagiaire.objects.create(
                            user=user,
                            nom=row['nom'],
                            prenom=row['prenom'],
                            email=row['email'],
                            telephone=row['telephone'],
                            ecole=row['ecole'],
                            abbreviation=row['abbreviation'],
                            filiere=row['filiere'],
                            niveau=row['niveau']
                        )
                    except IntegrityError as e:
                        self.message_user(request, f"Erreur importation column {row}: {e}", level='error')
                        continue
                self.message_user(request, "Fichier CSV importé avec succès.")
                return redirect("..")
        else:
            form = CSVUploadForm()

        return render(request, "admin/csv_form.html", {"form": form})

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['csv_form'] = CSVUploadForm()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('get_stagiaire_nom_complet', 'type_de_stage', 'sujet', 'date_de_debut', 'date_de_fin')
    search_fields = ('stagiaire__nom', 'type_de_stage', 'sujet')

    def get_stagiaire_nom_complet(self, obj):
        return f"{obj.stagiaire.nom} {obj.stagiaire.prenom}"
    get_stagiaire_nom_complet.short_description = 'Stagiaire'

@admin.register(Encadreur)
class EncadreurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'specialite')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(Projet_realise)
class ProjetRealiseAdmin(admin.ModelAdmin):
    list_display = ('get_stagiaire_nom_complet', 'get_encadreur_nom_complet', 'titre')
    search_fields = ('stagiaire__nom', 'encadreur__nom', 'titre')

    def get_stagiaire_nom_complet(self, obj):
        return f"{obj.stagiaire.nom} {obj.stagiaire.prenom}"
    get_stagiaire_nom_complet.short_description = 'Stagiaire'

    def get_encadreur_nom_complet(self, obj):
        return f"{obj.encadreur.nom} {obj.encadreur.prenom}"
    get_encadreur_nom_complet.short_description = 'Encadreur'

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('stagiaire', 'stage', 'encadreur', 'date_de_candidature', 'statut')
    list_filter = ('statut',)
    search_fields = ('stagiaire__nom', 'stage__sujet')
    list_editable = ('statut', 'encadreur') 
admin.site.register(Application, ApplicationAdmin)

@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('stagiaire', 'date', 'description')
    search_fields = ('stagiaire__nom', 'stagiaire__prenom', 'description')

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_type', 'file', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('user__username',)

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('stagiaire', 'date', 'status')
    search_fields = ('stagiaire__nom', 'stagiaire__prenom', 'date', 'status')

@admin.register(CertificateRequest)
class CertificateRequestAdmin(admin.ModelAdmin):
    list_display = ('stagiaire', 'status', 'date_requested', 'date_approved')
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status=CertificateRequest.APPROVED, date_approved=timezone.now())
    approve_requests.short_description = "Approuver les demandes sélectionnées"