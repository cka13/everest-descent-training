// DOM Elements
const navbar = document.querySelector('.navbar');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');
const contactForm = document.getElementById('contactForm');

// Smooth scrolling for navigation links
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        const offsetTop = element.offsetTop - 70; // Account for fixed navbar
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// Navigation link click handlers
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = link.getAttribute('href');
        smoothScroll(target);

        // Close mobile menu if open
        if (navMenu.classList.contains('active')) {
            toggleMobileMenu();
        }
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');

    // Animate hamburger menu
    const spans = navToggle.querySelectorAll('span');
    if (navMenu.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
    } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
}

navToggle.addEventListener('click', toggleMobileMenu);

// Navbar background on scroll
function updateNavbar() {
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(0, 0, 0, 0.95)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(0, 0, 0, 0.9)';
        navbar.style.boxShadow = 'none';
    }
}

window.addEventListener('scroll', updateNavbar);

// Form handling
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(contactForm);
    const data = Object.fromEntries(formData);

    // Basic form validation
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const course = document.getElementById('course').value;
    const message = document.getElementById('message').value;

    if (!name || !email || !phone || !course) {
        showNotification('Пожалуйста, заполните все обязательные поля', 'error');
        return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showNotification('Введите корректный email адрес', 'error');
        return;
    }

    // Prepare message for Telegram
    const telegramMessage = `
🆕 НОВАЯ ЗАЯВКА!

👤 Имя: ${name}
📧 Email: ${email}
📱 Телефон: ${phone}
🎓 Курс: ${course}
💬 Сообщение: ${message || 'Не указано'}

⏰ Время: ${new Date().toLocaleString('ru-RU')}
    `.trim();

    // Send to Telegram bot
    const botToken = 'ВАШ_BOT_TOKEN';
    const chatId = 'ВАШ_CHAT_ID';

    fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            chat_id: chatId,
            text: telegramMessage,
            parse_mode: 'HTML'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            showNotification('Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.', 'success');
            contactForm.reset();
        } else {
            showNotification('Ошибка при отправке заявки. Попробуйте еще раз.', 'error');
        }
    })
    .catch(error => {
        showNotification('Ошибка при отправке заявки. Попробуйте еще раз.', 'error');
        console.error('Error:', error);
    });
});

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 100);
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.about-card, .timeline-item, .pricing-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Video lazy loading enhancement
function enhanceVideo() {
    const videoContainer = document.querySelector('.video-container');
    if (videoContainer) {
        videoContainer.addEventListener('click', () => {
            const iframe = videoContainer.querySelector('iframe');
            if (iframe) {
                // You can add additional video enhancement logic here
                console.log('Video clicked');
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    enhanceVideo();
    updateNavbar();

    // Add loading animation to body
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';

    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Handle window resize for mobile menu
window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
        toggleMobileMenu();
    }
});

// Add CSS for notifications
const notificationStyles = `
    .notification {
        position: fixed;
        top: 90px;
        right: 20px;
        max-width: 400px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(420px);
        opacity: 0;
        transition: all 0.3s ease;
        border-left: 4px solid #ff6b35;
    }

    .notification-success {
        border-left-color: #28a745;
    }

    .notification-error {
        border-left-color: #dc3545;
    }

    .notification-content {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 20px;
    }

    .notification-content i {
        font-size: 1.2rem;
        color: #ff6b35;
    }

    .notification-success .notification-content i {
        color: #28a745;
    }

    .notification-error .notification-content i {
        color: #dc3545;
    }

    .notification-close {
        background: none;
        border: none;
        font-size: 1.2rem;
        color: #666;
        cursor: pointer;
        padding: 16px;
        transition: color 0.3s ease;
    }

    .notification-close:hover {
        color: #333;
    }

    .nav-menu.active {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 70px;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.95);
        padding: 20px;
        gap: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    @media (min-width: 769px) {
        .nav-menu.active {
            display: flex !important;
            flex-direction: row !important;
            position: static !important;
            background: none !important;
            padding: 0 !important;
            border-top: none !important;
        }
    }
`;

// Inject notification styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Parallax effect for hero section (optional enhancement)
function parallaxEffect() {
    const hero = document.querySelector('.hero');
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.5;

    if (hero) {
        hero.style.transform = `translateY(${rate}px)`;
    }
}

// Uncomment to enable parallax effect
// window.addEventListener('scroll', parallaxEffect);