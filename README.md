# IABE - International Association for Bilingual Education

Plateforme web Django pour l'ONG IABE dédiée à l'éducation bilingue en Côte d'Ivoire.

## Fonctionnalités

- **Site vitrine** : Présentation de l'ONG, partenaires, témoignages
- **Gestion des membres** : Inscription, profil, espace sécurisé, paiements
- **Programmes d'immersion** : Catalogue (Ghana, Nigeria...), inscription en ligne
- **Événements** : Conventions, séminaires, inscriptions
- **Tombola** : Achat de tickets, tirage automatisé, publication des gagnants
- **Blog / Ressources** : Articles, guides, opportunités
- **Multilingue** : Français / Anglais
- **Paiement Mobile Money** : MTN, Orange, Moov

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## Accès

- **Site** : http://127.0.0.1:8000/
- **Admin** : http://127.0.0.1:8000/admin/

## Structure du projet

```
├── iabe_project/    # Configuration Django
├── core/            # Site vitrine (accueil, à propos, contact)
├── members/         # Gestion des membres
├── programs/        # Programmes d'immersion
├── events/          # Événements
├── tombola/         # Module tombola
├── blog/            # Blog et ressources
├── templates/       # Templates HTML
├── static/          # Fichiers statiques (CSS, JS)
└── media/           # Fichiers uploadés
```

## Technologies

- Django 4.2
- TailwindCSS (CDN)
- SQLite (dev) / PostgreSQL (prod)
- Font Awesome
