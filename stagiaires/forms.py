from django import forms
from .models import ProgressUpdate, Projet_realise, FileUpload, Stagiaire, Absence, CertificateRequest


class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = ProgressUpdate
        fields = ['description', 'next_steps']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Ecrivez ce que vous avez fait aujourd\'hui, ou jusqu\'à présent'}),
            'next_steps': forms.Textarea(attrs={'placeholder': 'La procahine étape à suivre'}),
        }

class ProjetRealiseForm(forms.ModelForm):
    class Meta:
        model = Projet_realise
        fields = ['titre', 'description', 'fichier']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file_type', 'file']
        widgets = {
            'file_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        file_type = self.cleaned_data.get('file_type')
        valid_extensions = {
            'rapport': ['pdf'],
            'presentation': ['pptx', 'pdf'],
            'convention': ['pdf']
        }

        if not file.name.split('.')[-1] in valid_extensions[file_type]:
            raise forms.ValidationError(f"Invalid file type for {file_type}. Allowed types are: {', '.join(valid_extensions[file_type])}")
        
        return file
    
class StagiaireProfileForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'email', 'telephone', 'ecole', 'abbreviation', 'filiere', 'niveau']

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['stagiaire', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class CertificateRequestForm(forms.ModelForm):
    class Meta:
        model = CertificateRequest
        fields = []