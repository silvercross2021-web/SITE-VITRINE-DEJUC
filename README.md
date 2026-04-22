# DEJUC INTERNATIONAL GROUP - Site Vitrine Officiel

## Présentation
Ce projet est le site vitrine officiel du cabinet juridique DEJUC INTERNATIONAL GROUP, spécialisé en Médiation, Arbitrage, Investissement Foncier & Immobilier à Abidjan (Côte d'Ivoire) et en Afrique Francophone.
Il a été conçu selon les standards premium d'Awwwards avec un design immersif, une architecture solide et une expérience utilisateur soignée.

## Technologies Utilisées
- **Backend:** Django 5.2+, Python 3.13+
- **Base de données:** SQLite (développement)
- **Frontend:** HTML5, CSS3 Custom (Variables CSS, Grid, Flexbox), Bootstrap 5 (grille et utilitaires)
- **JavaScript & Animations:** Vanilla JS, AOS.js (Scroll Animations), Swiper.js (Carousels), Typed.js (Hero Text)
- **Déploiement statique:** WhiteNoise

## Installation et Lancement Rapide

1. **Créer et activer un environnement virtuel :**
   ```bash
   python -m venv venv
   # Sur Windows
   venv\Scripts\activate
   # Sur macOS/Linux
   source venv/bin/activate
   ```

2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations de la base de données :**
   ```bash
   python manage.py migrate
   ```

4. **Créer un super utilisateur (pour accéder au panel d'administration) :**
   ```bash
   python manage.py createsuperuser
   ```

5. **Collecter les fichiers statiques :**
   ```bash
   python manage.py collectstatic
   ```

6. **Lancer le serveur de développement :**
   ```bash
   python manage.py runserver
   ```

7. **Accès au site :**
   - Site public : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Administration : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Architecture du Projet
- `core/` : Application principale contenant toute la logique métier (modèles, vues, formulaires, URL admin).
- `static/` : Contient tout le CSS, JS et les images.
  - `css/main.css` : Design System principal (variables, typographie, composants).
  - `css/animations.css` : Animations avancées (fade, float, pulse, img-reveal).
  - `js/main.js` : Logique d'interaction et initialisation des bibliothèques (AOS, Swiper, Typed).
- `templates/` : Architecture modulaire des fichiers HTML (base, navbar, footer, pages).

## Points Techniques Implémentés
- **Expérience Premium** : Vidéo Hero, indicateurs de scroll, preloader, curseur dynamique, et palettes harmonieuses de bleus, d'oranges et de turquoises.
- **Micro-interactions** : Hover states subtils, image reveal effects, floating actions (WhatsApp), compteurs dynamiques.
- **Sécurité et Performance** : Formulaire de contact Django natif protégé contre CSRF, assets optimisés et minifiés, typographies asynchrones.
- **Responsive Design** : Approche Mobile-First intégrale.
