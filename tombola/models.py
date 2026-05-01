import random
import string
from django.db import models
from django.conf import settings


class Tombola(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'À venir'),
        ('active', 'En cours'),
        ('drawing', 'Tirage en cours'),
        ('completed', 'Terminée'),
    ]
    title = models.CharField('Titre', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Description')
    ticket_price = models.DecimalField('Prix du ticket (FCFA)', max_digits=10, decimal_places=0, default=5000)
    image = models.ImageField('Image', upload_to='tombola/', blank=True, null=True)
    start_date = models.DateTimeField('Date de début')
    end_date = models.DateTimeField('Date de fin')
    draw_date = models.DateTimeField('Date du tirage')
    status = models.CharField('Statut', max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tombola'
        verbose_name_plural = 'Tombolas'
        ordering = ['-draw_date']

    def __str__(self):
        return self.title

    @property
    def total_tickets_sold(self):
        return self.tickets.filter(is_paid=True).count()

    @property
    def total_revenue(self):
        return self.total_tickets_sold * self.ticket_price


class TombolaPrize(models.Model):
    tombola = models.ForeignKey(Tombola, on_delete=models.CASCADE, related_name='prizes')
    rank = models.PositiveIntegerField('Rang', default=1)
    title = models.CharField('Titre du lot', max_length=300)
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Image du lot', upload_to='tombola/prizes/', blank=True, null=True)
    value = models.DecimalField('Valeur estimée (FCFA)', max_digits=10, decimal_places=0, default=0)

    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'
        ordering = ['rank']

    def __str__(self):
        return f"#{self.rank} - {self.title}"


def generate_ticket_number():
    return 'IABE-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class TombolaTicket(models.Model):
    PAYMENT_METHODS = [
        ('mtn', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
        ('moov', 'Moov Money'),
    ]
    tombola = models.ForeignKey(Tombola, on_delete=models.CASCADE, related_name='tickets')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tombola_tickets')
    ticket_number = models.CharField('Numéro de ticket', max_length=20, unique=True, default=generate_ticket_number)
    payment_method = models.CharField('Moyen de paiement', max_length=20, choices=PAYMENT_METHODS)
    phone_number = models.CharField('Numéro de paiement', max_length=20)
    is_paid = models.BooleanField('Payé', default=False)
    is_winner = models.BooleanField('Gagnant', default=False)
    prize_won = models.ForeignKey(TombolaPrize, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner_ticket')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ticket tombola'
        verbose_name_plural = 'Tickets tombola'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_number} - {self.participant}"
