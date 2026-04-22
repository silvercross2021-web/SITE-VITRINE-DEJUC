"""
Models for DEJUC INTERNATIONAL GROUP website
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Service(models.Model):
    """6 Pôles d'expertise de DEJUC"""
    SERVICE_ICONS = [
        ('⚖️', 'Balance'),
        ('🔍', 'Loupe'),
        ('📋', 'Document'),
        ('🤝', 'Poignée de main'),
        ('⚔️', 'Contentieux'),
        ('🎓', 'Formation'),
    ]
    number = models.CharField(max_length=2, verbose_name="Numéro")
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=100, verbose_name="Classe icône (Lucide)")
    short_description = models.TextField(max_length=300, verbose_name="Description courte")
    full_description = models.TextField(verbose_name="Description complète")
    color_class = models.CharField(max_length=50, default='blue', verbose_name="Couleur thème")
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'number']
        verbose_name = "Service / Pôle d'expertise"
        verbose_name_plural = "Services / Pôles d'expertise"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number}. {self.title}"


class ServiceFeature(models.Model):
    """Ce qui est inclus dans chaque service"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} - {self.feature}"


class ServiceStep(models.Model):
    """Étapes du processus pour chaque service"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    step_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.service.title} - Étape {self.step_number}"


class ServiceFAQ(models.Model):
    """FAQ pour chaque service"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} - {self.question[:50]}"


class TeamMember(models.Model):
    """Membres de l'équipe DEJUC"""
    ROLES = [
        ('founder', 'Fondateur & Gérant'),
        ('associate', 'Associé'),
        ('counsel', 'Conseiller Juridique'),
        ('assistant', 'Assistant Juridique'),
        ('staff', 'Personnel'),
    ]
    full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    title = models.CharField(max_length=300, verbose_name="Titre / Poste")
    role = models.CharField(max_length=20, choices=ROLES, default='staff')
    bio = models.TextField(verbose_name="Biographie")
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'full_name']
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return f"{self.full_name} — {self.title}"


class Testimonial(models.Model):
    """Témoignages clients"""
    client_name = models.CharField(max_length=200, verbose_name="Nom du client")
    company = models.CharField(max_length=200, blank=True, verbose_name="Entreprise")
    role = models.CharField(max_length=200, blank=True, verbose_name="Poste")
    content = models.TextField(verbose_name="Témoignage")
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.client_name} — {self.rating}★"


class BlogPost(models.Model):
    """Articles du blog juridique"""
    CATEGORIES = [
        ('droit-ohada', 'Droit OHADA'),
        ('immobilier', 'Immobilier & Foncier'),
        ('arbitrage', 'Arbitrage & Médiation'),
        ('fiscalite', 'Fiscalité Côte d\'Ivoire'),
        ('actualites', 'Actualités Juridiques'),
        ('investissement', 'Investissement en Afrique'),
    ]
    title = models.CharField(max_length=300, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    excerpt = models.TextField(max_length=400, verbose_name="Résumé")
    content = models.TextField(verbose_name="Contenu")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_category_display_fr(self):
        return dict(self.CATEGORIES).get(self.category, self.category)


class ContactMessage(models.Model):
    """Messages de contact reçus"""
    SERVICE_CHOICES = [
        ('', '-- Sélectionnez un service --'),
        ('arbitrage', '01. Arbitrage & Médiation'),
        ('audit', '02. Audit & Sécurité Juridique'),
        ('creation', '03. Création de Sociétés & Contrats'),
        ('representation', '04. Représentation & Intermédiation'),
        ('contentieux', '05. Contentieux & Recouvrement'),
        ('formation', '06. Formation & Coaching Stratégique'),
        ('autre', 'Autre demande'),
    ]
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('replied', 'Répondu'),
        ('archived', 'Archivé'),
    ]
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True, verbose_name="Service concerné")
    message = models.TextField(verbose_name="Message")
    gdpr_consent = models.BooleanField(default=False, verbose_name="Consentement RGPD")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.created_at.strftime('%d/%m/%Y')}"


class NewsletterSubscriber(models.Model):
    """Abonnés à la newsletter"""
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"

    def __str__(self):
        return self.email


class LatinMaxim(models.Model):
    """Maximes latines pour la section design signature"""
    latin_text = models.CharField(max_length=200, verbose_name="Texte latin")
    french_translation = models.CharField(max_length=300, verbose_name="Traduction française")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Maxime latine"
        verbose_name_plural = "Maximes latines"

    def __str__(self):
        return self.latin_text
