"""
Views for DEJUC INTERNATIONAL GROUP website
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import Service, TeamMember, Testimonial, BlogPost, LatinMaxim, NewsletterSubscriber
from .forms import ContactForm, NewsletterForm


# ─── Données statiques (fallback si DB vide) ──────────────────────────────────

SERVICES_DATA = [
    {
        'number': '01',
        'title': 'Arbitrage & Médiation',
        'slug': 'arbitrage-mediation',
        'icon': 'scale',
        'color': 'blue',
        'short_description': 'Résolution amiable et rapide de vos litiges fonciers, familiaux et commerciaux. Confidentiel, efficace, durable.',
        'full_description': 'Notre pôle Arbitrage & Médiation offre une alternative professionnelle aux procédures judiciaires coûteuses. M. Dakouri Gnabro, arbitre et médiateur certifié, accompagne les parties vers des accords durables dans le respect de la loi et des traditions africaines.',
        'features': ['Médiation foncière', 'Arbitrage commercial', 'Litiges familiaux (héritage, divorce)', 'Conciliation rapide', 'Confidentialité garantie', 'Décisions exécutoires'],
        'image_url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80',
        'steps': [
            {'title': 'Consultation Initiale', 'description': 'Évaluation gratuite de votre situation et faisabilité.'},
            {'title': 'Saisine Officielle', 'description': 'Ouverture du dossier et invitation de l\'autre partie.'},
            {'title': 'Sessions de Médiation', 'description': 'Échanges confidentiels dirigés par notre expert.'},
            {'title': 'Accord Final', 'description': 'Rédaction de l\'accord et homologation si nécessaire.'}
        ],
        'faqs': [
            {'question': 'Combien de temps dure une procédure ?', 'answer': 'Contrairement aux tribunaux qui prennent des années, nos médiations aboutissent généralement en 1 à 3 mois.'},
            {'question': 'L\'accord est-il légalement contraignant ?', 'answer': 'Oui, une fois signé et homologué, il a force exécutoire.'}
        ]
    },
    {
        'number': '02',
        'title': 'Audit & Sécurité Juridique',
        'slug': 'audit-securite-juridique',
        'icon': 'shield-check',
        'color': 'orange',
        'short_description': 'Audit foncier complet, vérification des titres et gestion des risques avant tout investissement.',
        'full_description': 'Avant tout investissement foncier ou immobilier, notre équipe réalise un audit juridique exhaustif : vérification de titres fonciers, détection des risques, analyse de conformité réglementaire et recommandations personnalisées.',
        'features': ['Audit de titres fonciers', 'Vérification de documents', 'Analyse des risques', 'Conformité réglementaire', 'Due diligence immobilière', 'Rapports d\'audit détaillés'],
        'image_url': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80',
        'steps': [
            {'title': 'Collecte des Documents', 'description': 'Réception de tous les documents relatifs au bien.'},
            {'title': 'Vérification Institutionnelle', 'description': 'Contrôle auprès du Ministère de la Construction et des Domaines.'},
            {'title': 'Descente sur le Terrain', 'description': 'Vérification physique des limites et de l\'occupation.'},
            {'title': 'Rapport d\'Audit', 'description': 'Remise d\'un rapport détaillé validant ou déconseillant l\'investissement.'}
        ],
        'faqs': [
            {'question': 'Auditez-vous des terrains sans ACD ?', 'answer': 'Oui, nous pouvons auditer des attestations villageoises et vous accompagner vers l\'ACD.'},
            {'question': 'Intervenez-vous hors d\'Abidjan ?', 'answer': 'Absolument, notre équipe se déplace sur tout le territoire ivoirien.'}
        ]
    },
    {
        'number': '03',
        'title': 'Création de Sociétés & Contrats',
        'slug': 'creation-societes-contrats',
        'icon': 'file-text',
        'color': 'teal',
        'short_description': 'Accompagnement complet pour SARL, SA, SCI. Rédaction de contrats d\'affaires et veille juridique OHADA.',
        'full_description': 'Nous accompagnons les entrepreneurs et investisseurs dans la création et la structuration de leurs sociétés en Côte d\'Ivoire et en Afrique francophone, dans le respect du droit OHADA.',
        'features': ['Création SARL, SA, SCI', 'Rédaction de statuts', 'Contrats commerciaux', 'Baux professionnels', 'Veille juridique OHADA', 'Modification et dissolution'],
        'image_url': 'https://images.unsplash.com/photo-1444201983204-c43cbd584d93?w=800&q=80',
        'steps': [
            {'title': 'Choix du Statut', 'description': 'Conseil sur la forme juridique la plus adaptée (SARL, SA, SAS...).'},
            {'title': 'Rédaction des Statuts', 'description': 'Élaboration de statuts sur mesure protégeant les fondateurs.'},
            {'title': 'Immatriculation', 'description': 'Dépôt au CEPICI et obtention du RCCM et numéro contribuable.'},
            {'title': 'Suivi Post-Création', 'description': 'Accompagnement pour vos premiers contrats.'}
        ],
        'faqs': [
            {'question': 'Puis-je créer ma société sans être résident ?', 'answer': 'Oui, la loi permet aux investisseurs étrangers de créer leur structure. Nous vous assistons pour toutes les démarches.'},
            {'question': 'Rédigez-vous des pactes d\'actionnaires ?', 'answer': 'Tout à fait, nous rédigeons des pactes sur mesure pour anticiper tout conflit futur.'}
        ]
    },
    {
        'number': '04',
        'title': 'Représentation & Intermédiation',
        'slug': 'representation-intermediation',
        'icon': 'handshake',
        'color': 'blue',
        'short_description': 'Négociation d\'intérêts, achat-vente immobilier, gestion locative et management de projets avec discrétion.',
        'full_description': 'Notre pôle Représentation accompagne les investisseurs locaux et étrangers dans leurs transactions immobilières et commerciales, en agissant comme intermédiaire de confiance.',
        'features': ['Représentation en négociation', 'Achat-vente immobilier', 'Gestion locative', 'Management de projets', 'Intermédiation commerciale', 'Discrétion et confidentialité'],
        'image_url': 'https://images.unsplash.com/photo-1556761175-4b46a572b786?w=800&q=80',
        'steps': [
            {'title': 'Mandat de Représentation', 'description': 'Signature du mandat définissant nos limites d\'intervention.'},
            {'title': 'Prospection & Négociation', 'description': 'Recherche d\'opportunités et discussions en votre nom.'},
            {'title': 'Sécurisation de la Transaction', 'description': 'Intervention de nos juristes pour blinder les accords.'},
            {'title': 'Clôture de l\'Opération', 'description': 'Signature finale et remise des actifs/fonds en toute sécurité.'}
        ],
        'faqs': [
            {'question': 'Garantissez-vous la confidentialité ?', 'answer': 'C\'est notre principe premier. Nous agissons sous le sceau strict du secret professionnel.'}
        ]
    },
    {
        'number': '05',
        'title': 'Contentieux & Recouvrement',
        'slug': 'contentieux-recouvrement',
        'icon': 'gavel',
        'color': 'orange',
        'short_description': 'Défense de vos droits devant toutes les juridictions, recouvrement de créances et gestion RH.',
        'full_description': 'Nous assurons la défense de vos droits et intérêts devant les juridictions ivoiriennes et africaines, le recouvrement amiable et judiciaire de créances, ainsi que la gestion des litiges en droit du travail.',
        'features': ['Défense en justice', 'Recouvrement de créances', 'Litiges commerciaux', 'Droit du travail', 'Injonctions de payer', 'Saisies conservatoires'],
        'image_url': 'https://images.unsplash.com/photo-1505664173691-a28186981883?w=800&q=80',
        'steps': [
            {'title': 'Analyse du Dossier', 'description': 'Évaluation des chances de succès et des coûts.'},
            {'title': 'Mise en Demeure', 'description': 'Dernière tentative de résolution amiable forte.'},
            {'title': 'Procédure', 'description': 'Saisine du tribunal compétent ou lancement de l\'injonction.'},
            {'title': 'Exécution', 'description': 'Mise en œuvre de la décision par nos huissiers partenaires.'}
        ],
        'faqs': [
            {'question': 'Facturez-vous au résultat ?', 'answer': 'Nous fonctionnons avec des honoraires fixes et des honoraires de résultat convenus à l\'avance.'}
        ]
    },
    {
        'number': '06',
        'title': 'Formation & Coaching Stratégique',
        'slug': 'formation-coaching',
        'icon': 'graduation-cap',
        'color': 'teal',
        'short_description': 'Obtention d\'agréments, permis de construire, coaching pour décideurs et insertion professionnelle.',
        'full_description': 'Notre département Formation & Coaching accompagne les décideurs, entrepreneurs et professionnels dans leur développement stratégique, l\'obtention de licences et permis, et la montée en compétences juridiques.',
        'features': ['Coaching décideurs', 'Obtention d\'agréments', 'Permis de construire', 'ACD et autorisations', 'Formations juridiques', 'Insertion professionnelle'],
        'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80',
        'steps': [
            {'title': 'Diagnostic des Besoins', 'description': 'Identifier les lacunes ou les autorisations manquantes.'},
            {'title': 'Plan d\'Action', 'description': 'Programme de formation ou roadmap d\'obtention de permis.'},
            {'title': 'Accompagnement', 'description': 'Sessions de coaching ou montage des dossiers administratifs.'},
            {'title': 'Résultat', 'description': 'Montée en compétence validée ou permis obtenu.'}
        ],
        'faqs': [
            {'question': 'Formez-vous les équipes en entreprise ?', 'answer': 'Oui, nous proposons des formations intra-entreprise sur mesure.'}
        ]
    },
]

TESTIMONIALS_DATA = [
    {
        'name': 'Kouamé Assoumou',
        'company': 'Groupe Immobilier KOASSI',
        'role': 'Directeur Général',
        'content': 'DEJUC International nous a accompagnés dans l\'audit complet de 12 terrains à Cocody. Leur rigueur et leur connaissance du marché foncier ivoirien sont exceptionnelles. Nous travaillons exclusivement avec eux.',
        'rating': 5,
        'initials': 'KA',
        'color': 'blue',
    },
    {
        'name': 'Aminata Coulibaly',
        'company': 'SCI Soleil d\'Abidjan',
        'role': 'Associée Gérante',
        'content': 'Grâce à leur expertise en création de sociétés et droit OHADA, notre SCI a été créée en temps record. M. Gnabro est un professionnel d\'une grande intégrité. Je les recommande sans réserve.',
        'rating': 5,
        'initials': 'AC',
        'color': 'orange',
    },
    {
        'name': 'Jean-Claude Djibo',
        'company': 'Import-Export Sahel CI',
        'role': 'Président',
        'content': 'Notre litige commercial de 3 ans a été résolu en 4 mois grâce à la médiation orchestrée par DEJUC. Une approche professionnelle, équitable et efficace. Le résultat dépasse nos attentes.',
        'rating': 5,
        'initials': 'JD',
        'color': 'teal',
    },
    {
        'name': 'Marie-Claire Touré',
        'company': 'Résidence Les Palmiers',
        'role': 'Promotrice Immobilière',
        'content': 'L\'accompagnement de DEJUC pour l\'obtention de nos permis de construire et la gestion des baux a été déterminant. Une équipe réactive, compétente et toujours disponible.',
        'rating': 5,
        'initials': 'MT',
        'color': 'blue',
    },
    {
        'name': 'Mamadou Bah',
        'company': 'BTP Solutions Afrique',
        'role': 'Directeur des Opérations',
        'content': 'En tant qu\'investisseur sénégalais, j\'avais besoin d\'un partenaire de confiance en Côte d\'Ivoire. DEJUC International a été exactement cela : professionnel, honnête et efficace.',
        'rating': 5,
        'initials': 'MB',
        'color': 'orange',
    },
]

MAXIMS_DATA = [
    {'latin': 'Pacta sunt servanda', 'french': 'Les accords doivent être respectés'},
    {'latin': 'Audi alteram partem', 'french': 'Écoute toujours l\'autre partie'},
    {'latin': 'Melius est praecavere quam sanare', 'french': 'Mieux vaut prévenir que guérir'},
    {'latin': 'Bonae fidei contractus', 'french': 'Les contrats de bonne foi'},
    {'latin': 'Nemo judex in causa sua', 'french': 'Nul ne peut être juge de soi-même'},
    {'latin': 'Docendo discimus', 'french': 'C\'est en enseignant qu\'on apprend'},
]

BLOG_POSTS_DATA = [
    {
        'title': 'Le droit OHADA : Ce que tout investisseur en Afrique doit savoir',
        'category': 'droit-ohada',
        'category_label': 'Droit OHADA',
        'excerpt': 'L\'Organisation pour l\'Harmonisation en Afrique du Droit des Affaires (OHADA) offre un cadre juridique unifié qui sécurise vos investissements dans 17 pays africains.',
        'date': '15 Janvier 2025',
        'read_time': '8 min',
        'image_url': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80',
        'color': 'blue',
    },
    {
        'title': 'Investissement foncier à Abidjan : Les pièges à éviter absolument',
        'category': 'immobilier',
        'category_label': 'Immobilier & Foncier',
        'excerpt': 'Le marché foncier abidjanais est dynamique mais semé d\'embûches. Découvrez les 7 erreurs les plus fréquentes et comment les éviter grâce à un audit juridique préalable.',
        'date': '3 Février 2025',
        'read_time': '12 min',
        'image_url': 'https://images.unsplash.com/photo-1486325212027-8081e485255e?auto=format&fit=crop&w=600&q=80',
        'color': 'orange',
    },
    {
        'title': 'L\'arbitrage commercial : Une alternative moderne à la justice traditionnelle',
        'category': 'arbitrage',
        'category_label': 'Arbitrage & Médiation',
        'excerpt': 'Face aux lenteurs judiciaires, l\'arbitrage s\'impose comme la solution privilégiée des entreprises modernes. Comprendre ses mécanismes pour mieux protéger vos intérêts.',
        'date': '20 Mars 2025',
        'read_time': '10 min',
        'image_url': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=600&q=80',
        'color': 'teal',
    },
]

# ─── Vues principales ──────────────────────────────────────────────────────────

def home(request):
    """Page d'accueil"""
    context = {
        'page_title': 'DEJUC International Group — Cabinet Juridique Spécialisé à Abidjan',
        'meta_description': 'Cabinet juridique spécialisé en médiation, arbitrage, investissement foncier et immobilier en Côte d\'Ivoire et Afrique Francophone. Expert : M. Dakouri Gnabro.',
        'services': SERVICES_DATA,
        'testimonials': TESTIMONIALS_DATA,
        'maxims': MAXIMS_DATA,
        'blog_posts': BLOG_POSTS_DATA,
        'contact_form': ContactForm(),
    }
    return render(request, 'index.html', context)


def about(request):
    """Page À propos"""
    context = {
        'page_title': 'À Propos — DEJUC International Group',
        'meta_description': 'Découvrez DEJUC International Group, sa mission, son fondateur M. Dakouri Gnabro et les valeurs qui guident notre cabinet juridique à Abidjan.',
        'breadcrumb': [('Accueil', '/'), ('À Propos', None)],
    }
    return render(request, 'about.html', context)


def services_list(request):
    """Page liste des services"""
    context = {
        'page_title': 'Nos Pôles d\'Expertise — DEJUC International Group',
        'meta_description': '6 pôles d\'expertise juridique : Arbitrage, Audit, Création de sociétés, Représentation, Contentieux et Formation. Cabinet DEJUC International à Abidjan.',
        'services': SERVICES_DATA,
        'breadcrumb': [('Accueil', '/'), ('Services', None)],
    }
    return render(request, 'services/services.html', context)


def service_detail(request, slug):
    """Page détail d'un service"""
    service = next((s for s in SERVICES_DATA if s['slug'] == slug), None)
    if not service:
        from django.http import Http404
        raise Http404("Service non trouvé")

    context = {
        'page_title': f"{service['title']} — DEJUC International Group",
        'meta_description': service['short_description'],
        'service': service,
        'other_services': [s for s in SERVICES_DATA if s['slug'] != slug][:3],
        'breadcrumb': [('Accueil', '/'), ('Services', '/services/'), (service['title'], None)],
    }
    return render(request, 'services/service_detail.html', context)


def blog_list(request):
    """Page blog"""
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')

    posts = BLOG_POSTS_DATA
    if category:
        posts = [p for p in posts if p.get('category') == category]

    context = {
        'page_title': 'Blog Juridique — DEJUC International Group',
        'meta_description': 'Actualités juridiques, droit OHADA, immobilier et investissement en Côte d\'Ivoire et Afrique Francophone par les experts DEJUC.',
        'posts': posts,
        'all_posts': BLOG_POSTS_DATA,
        'current_category': category,
        'breadcrumb': [('Accueil', '/'), ('Blog', None)],
    }
    return render(request, 'blog/blog.html', context)


def contact(request):
    """Page contact avec formulaire"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save(commit=False)
            # Capture IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                contact_msg.ip_address = x_forwarded_for.split(',')[0]
            else:
                contact_msg.ip_address = request.META.get('REMOTE_ADDR')
            contact_msg.save()

            # Send notification email
            try:
                send_mail(
                    subject=f'[DEJUC] Nouveau message de {contact_msg.first_name} {contact_msg.last_name}',
                    message=f"""
Nouveau message de contact reçu sur le site DEJUC International.

Nom : {contact_msg.first_name} {contact_msg.last_name}
Email : {contact_msg.email}
Téléphone : {contact_msg.phone}
Service : {contact_msg.get_service_display() if hasattr(contact_msg, 'get_service_display') else contact_msg.service}

Message :
{contact_msg.message}

---
DEJUC International Group — Système de gestion des contacts
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['infodejucinternational@gmail.com'],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                '✅ Votre message a bien été envoyé ! Notre équipe vous répondra dans les 24 heures.'
            )
            return redirect('contact')
        else:
            messages.error(request, '❌ Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ContactForm()

    context = {
        'page_title': 'Contact — DEJUC International Group',
        'meta_description': 'Contactez DEJUC International Group à Abidjan (Cocody Angré). Consultation gratuite. Tél: +225 07 78 48 84 05. Email: infodejucinternational@gmail.com',
        'form': form,
        'breadcrumb': [('Accueil', '/'), ('Contact', None)],
    }
    return render(request, 'contact.html', context)


@require_POST
def newsletter_subscribe(request):
    """Endpoint AJAX pour inscription newsletter"""
    form = NewsletterForm(request.POST)
    if form.is_valid():
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=form.cleaned_data['email']
        )
        if created:
            return JsonResponse({'success': True, 'message': 'Inscription réussie ! Merci.'})
        else:
            return JsonResponse({'success': False, 'message': 'Cet email est déjà inscrit.'})
    return JsonResponse({'success': False, 'message': 'Email invalide.'})
