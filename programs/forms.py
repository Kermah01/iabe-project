from django import forms
from .models import ProgramRegistration

INPUT_CLASS = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'


class ProgramRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProgramRegistration
        fields = ['payment_method', 'phone_number', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={'class': INPUT_CLASS + ' bg-white'}),
            'phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '+225 07 XX XX XX XX',
            }),
            'notes': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Informations complémentaires...',
                'rows': 3,
            }),
        }
