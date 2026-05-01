from django.db import models
from django.conf import settings


class Event(models.Model):
    EVENT_TYPES = [
        ('convention', 'Convention annuelle'),
        ('seminar', 'Séminaire'),
        ('workshop', 'Atelier'),
        ('conference', 'Conférence'),
        ('campaign', 'Campagne de sensibilisation'),
    ]
    title = models.CharField('Titre', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    event_type = models.CharField('Type', max_length=20, choices=EVENT_TYPES)
    description = models.TextField('Description')
    location = models.CharField('Lieu', max_length=300)
    start_date = models.DateTimeField('Date de début')
    end_date = models.DateTimeField('Date de fin')
    image = models.ImageField('Image', upload_to='events/', blank=True, null=True)
    max_participants = models.PositiveIntegerField('Places disponibles', default=100)
    registration_fee = models.DecimalField('Frais d\'inscription (FCFA)', max_digits=10, decimal_places=0, default=0)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Événement'
        verbose_name_plural = 'Événements'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def spots_left(self):
        return self.max_participants - self.registrations.filter(status='confirmed').count()


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField('Statut', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscription événement"
        verbose_name_plural = "Inscriptions événements"
        unique_together = ['event', 'member']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member} - {self.event.title}"
