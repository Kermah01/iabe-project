from django.db import models
from django.conf import settings


class Program(models.Model):
    DESTINATIONS = [
        ('ghana', 'Ghana'),
        ('nigeria', 'Nigeria'),
        ('burkina', 'Burkina Faso'),
        ('south_africa', 'Afrique du Sud'),
        ('kenya', 'Kenya'),
        ('other', 'Autre'),
    ]
    PROGRAM_TYPES = [
        ('immersion', "Séjour d'immersion"),
        ('camp', 'Camp de vacances'),
        ('exchange', 'Échange scolaire'),
        ('homestay', "Famille d'accueil"),
        ('teacher_training', 'Formation enseignants'),
    ]
    title = models.CharField('Titre', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    program_type = models.CharField('Type de programme', max_length=20, choices=PROGRAM_TYPES, default='immersion')
    destination = models.CharField('Destination', max_length=20, choices=DESTINATIONS)
    description = models.TextField('Description')
    duration = models.CharField('Durée', max_length=100, help_text='Ex: 4 semaines, 3 mois')
    cost = models.DecimalField('Coût (FCFA)', max_digits=10, decimal_places=0)
    partner_institution = models.CharField('Établissement partenaire', max_length=300)
    transport_partner = models.CharField('Partenaire transport', max_length=200, blank=True,
                                         help_text='Ex: STC Bus (tarif réduit)')
    image = models.ImageField('Image', upload_to='programs/', blank=True, null=True)
    start_date = models.DateField('Date de début', blank=True, null=True)
    end_date = models.DateField('Date de fin', blank=True, null=True)
    max_participants = models.PositiveIntegerField('Places disponibles', default=30)
    is_active = models.BooleanField('Actif', default=True)
    highlights = models.TextField('Points forts', blank=True, help_text='Un point par ligne')
    requirements = models.TextField('Prérequis', blank=True, help_text='Un prérequis par ligne')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Programme d'immersion"
        verbose_name_plural = "Programmes d'immersion"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.get_destination_display()}"

    @property
    def spots_left(self):
        return self.max_participants - self.registrations.filter(status='confirmed').count()


class ProgramRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
    ]
    PAYMENT_METHODS = [
        ('mtn', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
        ('moov', 'Moov Money'),
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='registrations')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='program_registrations')
    status = models.CharField('Statut', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField('Moyen de paiement', max_length=20, choices=PAYMENT_METHODS, blank=True)
    phone_number = models.CharField('Numéro de paiement', max_length=20, blank=True)
    amount_paid = models.DecimalField('Montant payé (FCFA)', max_digits=10, decimal_places=0, default=0)
    notes = models.TextField('Notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscription programme"
        verbose_name_plural = "Inscriptions programmes"
        unique_together = ['program', 'member']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member} - {self.program.title}"
