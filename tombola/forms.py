from django import forms
from .models import TombolaTicket

INPUT_CLASS = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent'


class TombolaTicketForm(forms.ModelForm):
    class Meta:
        model = TombolaTicket
        fields = ['payment_method', 'phone_number']
        widgets = {
            'payment_method': forms.Select(attrs={'class': INPUT_CLASS + ' bg-white'}),
            'phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '+225 07 XX XX XX XX',
            }),
        }
