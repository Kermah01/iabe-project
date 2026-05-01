from django.db import models


class Partner(models.Model):
    PARTNER_TYPES = [
        ('school', 'École'),
        ('university', 'Université'),
        ('institution', 'Institution'),
        ('organization', 'Organisation'),
    ]
    name = models.CharField('Nom', max_length=200)
    partner_type = models.CharField('Type', max_length=20, choices=PARTNER_TYPES)
    country = models.CharField('Pays', max_length=100)
    description = models.TextField('Description', blank=True)
    logo = models.ImageField('Logo', upload_to='partners/', blank=True, null=True)
    website = models.URLField('Site web', blank=True)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'
        ordering = ['name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField('Nom', max_length=200)
    role = models.CharField('Rôle / Fonction', max_length=200)
    content = models.TextField('Témoignage')
    photo = models.ImageField('Photo', upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField('Actif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Témoignage'
        verbose_name_plural = 'Témoignages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"


class ContactMessage(models.Model):
    name = models.CharField('Nom', max_length=200)
    email = models.EmailField('Email')
    subject = models.CharField('Sujet', max_length=300)
    message = models.TextField('Message')
    is_read = models.BooleanField('Lu', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteSettings(models.Model):
    site_name = models.CharField('Nom du site', max_length=200, default='IABE')
    tagline = models.CharField('Slogan', max_length=500, default='International Association for Bilingual Education')
    about_text = models.TextField('Texte À propos', blank=True)
    mission = models.TextField('Mission', blank=True)
    vision = models.TextField('Vision', blank=True)
    objectives = models.TextField('Objectifs', blank=True)
    address = models.TextField('Adresse', blank=True)
    phone = models.CharField('Téléphone', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    tiktok_url = models.URLField('TikTok', blank=True)
    hero_image = models.ImageField('Image Hero', upload_to='site/', blank=True, null=True)

    class Meta:
        verbose_name = 'Paramètres du site'
        verbose_name_plural = 'Paramètres du site'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)
