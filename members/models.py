from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
    MEMBER_TYPES = [
        ('individual', 'Particulier'),
        ('school', 'École'),
        ('university', 'Université'),
        ('company', 'Entreprise'),
    ]
    member_type = models.CharField('Type de membre', max_length=20, choices=MEMBER_TYPES, default='individual')
    phone = models.CharField('Téléphone', max_length=20, blank=True)
    city = models.CharField('Ville', max_length=100, blank=True)
    country = models.CharField('Pays', max_length=100, default='Côte d\'Ivoire')
    organization_name = models.CharField('Nom de l\'organisation', max_length=200, blank=True,
                                         help_text='Pour les écoles, universités et entreprises')
    bio = models.TextField('Biographie', blank=True)
    photo = models.ImageField('Photo de profil', upload_to='members/', blank=True, null=True)
    is_membership_active = models.BooleanField('Adhésion active', default=False)
    membership_paid_until = models.DateField('Adhésion valide jusqu\'au', blank=True, null=True)
    date_joined_association = models.DateField('Date d\'adhésion', blank=True, null=True)

    class Meta:
        verbose_name = 'Membre'
        verbose_name_plural = 'Membres'

    def __str__(self):
        if self.organization_name:
            return f"{self.organization_name} ({self.get_member_type_display()})"
        return f"{self.get_full_name() or self.username}"


class MembershipPayment(models.Model):
    PAYMENT_TYPES = [
        ('adhesion', "Droit d'adhésion (30 000 FCFA)"),
        ('annual', 'Cotisation mensuelle (100 000 FCFA)'),
    ]
    PAYMENT_METHODS = [
        ('mtn', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
        ('moov', 'Moov Money'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField('Type', max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField('Montant (FCFA)', max_digits=10, decimal_places=0)
    payment_method = models.CharField('Moyen de paiement', max_length=20, choices=PAYMENT_METHODS)
    phone_number = models.CharField('Numéro de paiement', max_length=20)
    transaction_id = models.CharField('ID Transaction', max_length=100, blank=True)
    status = models.CharField('Statut', max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paiement adhésion'
        verbose_name_plural = 'Paiements adhésion'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member} - {self.get_payment_type_display()} - {self.amount} FCFA"


class MemberDocument(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField('Titre', max_length=200)
    file = models.FileField('Fichier', upload_to='member_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Document membre'
        verbose_name_plural = 'Documents membres'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.member} - {self.title}"
