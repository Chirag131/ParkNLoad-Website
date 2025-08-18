// Mobile navigation functionality
function toggleMobileMenu() {
    const mobileNav = document.getElementById('mobileNav');
    const mobileOverlay = document.getElementById('mobileOverlay');
    
    mobileNav.classList.toggle('active');
    mobileOverlay.classList.toggle('active');
    
    // Prevent body scrolling when menu is open
    document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : 'auto';
}

function closeMobileMenu() {
    const mobileNav = document.getElementById('mobileNav');
    const mobileOverlay = document.getElementById('mobileOverlay');
    
    mobileNav.classList.remove('active');
    mobileOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

function setMobileActive(element) {
    // Remove active class from all mobile nav links
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.classList.remove('active');
    });
    element.classList.add('active');
    
    // Also update desktop nav if visible
    const text = element.textContent;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.textContent === text) {
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });
    
    closeMobileMenu();
}

// Navigation functionality
function setActive(element) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    element.classList.add('active');
    
    // Also update mobile nav
    const text = element.textContent;
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        if (link.textContent === text) {
            document.querySelectorAll('.mobile-nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });
}

// Window resize handler for responsive adjustments
window.addEventListener('resize', function() {
    // Close mobile menu on resize to desktop
    if (window.innerWidth > 767) {
        closeMobileMenu();
    }
    
    // Adjust table scroll on resize
    const tableScroll = document.querySelector('.table-scroll');
    if (window.innerWidth <= 767 && tableScroll) {
        tableScroll.style.maxHeight = window.innerHeight < 600 ? '300px' : '400px';
    }
});

// Touch event handlers for better mobile interaction
let touchStartX = 0;
let touchStartY = 0;

document.addEventListener('touchstart', function(e) {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
});

document.addEventListener('touchend', function(e) {
    if (!touchStartX || !touchStartY) return;

    let touchEndX = e.changedTouches[0].clientX;
    let touchEndY = e.changedTouches[0].clientY;

    let diffX = touchStartX - touchEndX;
    let diffY = touchStartY - touchEndY;

    // Swipe detection (only if horizontal swipe is more significant than vertical)
    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
        const mobileNav = document.getElementById('mobileNav');
        
        if (diffX > 0 && mobileNav.classList.contains('active')) {
            // Swipe left - close menu
            closeMobileMenu();
        } else if (diffX < -100 && window.innerWidth <= 767 && touchStartX < 50) {
            // Swipe right from left edge - open menu
            toggleMobileMenu();
        }
    }

    touchStartX = 0;
    touchStartY = 0;
});

// Stats card animation
function animateCard(card) {
    card.style.transform = 'translateY(-5px) scale(0.98)';
    setTimeout(() => {
        card.style.transform = 'translateY(-5px) scale(1)';
    }, 150);
}

// Workspace dropdown functionality
function toggleWorkspace() {
    const selector = document.getElementById('workspaceSelector');
    selector.classList.toggle('active');
    
    setTimeout(() => {
        selector.classList.remove('active');
    }, 2000);
}

// Map functionality
function openFullMap() {
    window.open('https://www.google.com/maps/@28.7144068,77.0909803,15z?entry=ttu&g_ep=EgoyMDI1MDgxMy4wIKXMDSoASAFQAw%3D%3D', '_blank');
}

function refreshMap() {
    const mapDisplay = document.querySelector('.map-display');
    mapDisplay.style.background = 'linear-gradient(135deg, #ccfbf1, #a7f3d0)';
    setTimeout(() => {
        mapDisplay.style.background = 'linear-gradient(135deg, #f0fdfa, #e6fffa)';
    }, 500);
}



// Real-time updates simulation
const deliveryIds = ['DEL-58823', 'JXK-26543', 'MNP-78912', 'QRS-45678', 'ABC-12345', 'XYZ-67890'];

setInterval(() => {
    const randomId = deliveryIds[Math.floor(Math.random() * deliveryIds.length)];
    const rows = document.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        if (row.textContent.includes(randomId)) {
            row.classList.add('highlight');
            setTimeout(() => {
                row.classList.remove('highlight');
            }, 1000);
        }
    });
}, 7000);

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Close mobile menu on outside click
    document.addEventListener('click', function(e) {
        const mobileNav = document.getElementById('mobileNav');
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        
        if (mobileNav && mobileNav.classList.contains('active')) {
            if (!mobileNav.contains(e.target) && e.target !== mobileMenuBtn) {
                closeMobileMenu();
            }
        }
    });

    // Handle escape key for mobile menu
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMobileMenu();
        }
    });

    // Optimize scroll performance
    let ticking = false;
    function updateScroll() {
        // Add navbar scroll effect
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.background = 'white';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
        ticking = false;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateScroll);
            ticking = true;
        }
    });

    // Add loading animations
    const cards = document.querySelectorAll('.stat-card, .map-container, .upcoming-deliveries, .active-deliveries');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Enhanced table interaction for mobile
if (window.innerWidth <= 767) {
    const tableRows = document.querySelectorAll('.deliveries-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            // Highlight selected row on mobile
            tableRows.forEach(r => r.style.background = '');
            this.style.background = '#f0fdfa';
        });
    });
}