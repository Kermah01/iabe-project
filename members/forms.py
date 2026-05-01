from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Member, MembershipPayment

INPUT_CLASS = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'


class MemberRegistrationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['username', 'email', 'first_name', 'last_name', 'member_type',
                  'phone', 'city', 'country', 'organization_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = INPUT_CLASS
            if field_name == 'member_type':
                field.widget.attrs['class'] += ' bg-white'
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['organization_name'].help_text = 'Requis pour les écoles, universités et entreprises'


class MemberLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = INPUT_CLASS


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone', 'city',
                  'country', 'organization_name', 'bio', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = INPUT_CLASS


class MembershipPaymentForm(forms.ModelForm):
    class Meta:
        model = MembershipPayment
        fields = ['payment_type', 'payment_method', 'phone_number']
        widgets = {
            'payment_type': forms.Select(attrs={'class': INPUT_CLASS + ' bg-white'}),
            'payment_method': forms.Select(attrs={'class': INPUT_CLASS + ' bg-white'}),
            'phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '+225 07 XX XX XX XX',
            }),
        }
