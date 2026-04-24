/**
 * Main JavaScript for DEJUC Site
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Remove Preloader - fast dismiss + failsafe on window.load
    const preloader = document.getElementById('preloader');
    
    function hidePreloader() {
        if (preloader && preloader.style.opacity !== '0') {
            preloader.style.opacity = '0';
            preloader.style.visibility = 'hidden';
            preloader.style.pointerEvents = 'none';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 450);
        }
    }
    
    // Hide after 300ms on DOMContentLoaded
    setTimeout(hidePreloader, 300);
    
    // Failsafe: hide on window.load (all resources loaded) at the latest
    window.addEventListener('load', () => {
        setTimeout(hidePreloader, 100);
    });

    // 2. Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50,
        });
    }

    // 3. Navbar Sticky Effect
    const navbar = document.querySelector('.navbar');
    
    function checkScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
            navbar.classList.remove('navbar-dark');
            navbar.classList.add('navbar-light');
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.classList.remove('navbar-light');
            navbar.classList.add('navbar-dark');
        }
    }
    
    window.addEventListener('scroll', checkScroll);
    checkScroll(); // Check on load

    // 4. Initialize Swiper for Testimonials
    if (typeof Swiper !== 'undefined' && document.querySelector('.testimonials-slider')) {
        new Swiper('.testimonials-slider', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                }
            }
        });
    }

    // 5. Initialize Swiper for Maxims
    if (typeof Swiper !== 'undefined' && document.querySelector('.maxims-slider')) {
        new Swiper('.maxims-slider', {
            slidesPerView: 1,
            loop: true,
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            },
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            }
        });
    }

    // 6. Typed.js Effect (Hero Section)
    const typedElement = document.querySelector('.typed-text');
    if (typedElement && typeof Typed !== 'undefined') {
        new Typed('.typed-text', {
            strings: [
                'Votre Partenaire Juridique en Afrique.',
                'Experts en Arbitrage & Médiation.',
                'Sécurisez Vos Projets Immobiliers.'
            ],
            typeSpeed: 50,
            backSpeed: 30,
            backDelay: 2000,
            loop: true
        });
    }

    // 7. Counter Animation (CountUp.js or custom intersection observer)
    const counters = document.querySelectorAll('.counter-value');
    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const finalValue = parseInt(target.getAttribute('data-target'));
                    
                    // Simple counter animation
                    let startValue = 0;
                    const duration = 2000; // ms
                    const interval = 20;
                    const steps = duration / interval;
                    const increment = finalValue / steps;
                    
                    const counter = setInterval(() => {
                        startValue += increment;
                        if (startValue >= finalValue) {
                            target.innerText = finalValue;
                            clearInterval(counter);
                        } else {
                            target.innerText = Math.ceil(startValue);
                        }
                    }, interval);
                    
                    observer.unobserve(target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    // 8. Custom scroll reveal (for specific elements not using AOS)
    const revealElements = document.querySelectorAll('.fade-in-up, .img-reveal, .highlight-text');
    
    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -100px 0px' });
        
        revealElements.forEach(el => revealObserver.observe(el));
    }

    // 9. Newsletter Form AJAX submission
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('newsletter-email').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const messageDiv = document.getElementById('newsletter-message');
            
            fetch('/newsletter/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `email=${encodeURIComponent(email)}`
            })
            .then(response => response.json())
            .then(data => {
                messageDiv.textContent = data.message;
                messageDiv.className = data.success ? 'text-success mt-2' : 'text-danger mt-2';
                if (data.success) {
                    newsletterForm.reset();
                }
            })
            .catch(error => {
                messageDiv.textContent = "Une erreur est survenue. Veuillez réessayer.";
                messageDiv.className = 'text-danger mt-2';
            });
        });
    }

    // 10. Contact Form Loading State
    const contactForm = document.getElementById('main-contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function() {
            const btn = document.getElementById('submit-btn');
            const btnText = document.getElementById('btn-text');
            const btnSpinner = document.getElementById('btn-spinner');
            
            btn.disabled = true;
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline-block';
        });
    }
});
