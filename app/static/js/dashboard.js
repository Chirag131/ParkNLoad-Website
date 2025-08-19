// Profile dropdown functionality
function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    const profileContainer = document.querySelector('.profile-dropdown');
    const profileBtn = document.querySelector('.profile-btn');
    
    const isActive = dropdown.classList.contains('active');
    
    dropdown.classList.toggle('active');
    profileContainer.classList.toggle('active');
    
    // Update ARIA attributes
    profileBtn.setAttribute('aria-expanded', !isActive);
}

function closeProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    const profileContainer = document.querySelector('.profile-dropdown');
    const profileBtn = document.querySelector('.profile-btn');
    
    dropdown.classList.remove('active');
    profileContainer.classList.remove('active');
    
    // Update ARIA attributes
    profileBtn.setAttribute('aria-expanded', 'false');
}

function showProfile() {
    // Close dropdown first
    closeProfileDropdown();
    // Redirect to profile page
    window.location.href = '/msme/profile';
}

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
    const options = document.getElementById('workspaceOptions');
    const arrow = document.getElementById('dropdownArrow');
    
    const isActive = options.classList.contains('active');
    console.log('toggleWorkspace called, isActive:', isActive);
    
    if (isActive) {
        // Close dropdown
        console.log('Closing dropdown');
        options.classList.remove('active');
        selector.classList.remove('active');
        arrow.textContent = '▼';
    } else {
        // Open dropdown
        console.log('Opening dropdown');
        options.classList.add('active');
        selector.classList.add('active');
        arrow.textContent = '▲';
        
        // Close dropdown after 5 seconds of inactivity
        setTimeout(() => {
            if (options.classList.contains('active')) {
                console.log('Auto-closing dropdown');
                options.classList.remove('active');
                selector.classList.remove('active');
                arrow.textContent = '▼';
            }
        }, 5000);
    }
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

// Function to select warehouse
function selectWorkspace(warehouseId, warehouseName) {
    console.log('selectWorkspace called with:', warehouseId, warehouseName);
    
    // Update the display
    document.getElementById('selectedWorkspace').textContent = warehouseName;
    
    // Close the dropdown
    const options = document.getElementById('workspaceOptions');
    const selector = document.getElementById('workspaceSelector');
    const arrow = document.getElementById('dropdownArrow');
    
    options.classList.remove('active');
    selector.classList.remove('active');
    arrow.textContent = '▼';
    
    // Redirect to set the warehouse
    console.log('Redirecting to:', "/msme/set-warehouse/" + warehouseId);
    window.location.href = "/msme/set-warehouse/" + warehouseId;
}

// Function to add new delivery
function addNewDelivery() {
    window.location.href = "/msme/add_order";
}

// Function to animate card
function animateCard(card) {
    card.style.transform = 'scale(1.05)';
    setTimeout(() => {
        card.style.transform = 'scale(1)';
    }, 200);
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
    
    // Close profile dropdown on outside click
    document.addEventListener('click', function(e) {
        const profileDropdown = document.getElementById('profileDropdown');
        const profileBtn = document.querySelector('.profile-btn');
        
        if (profileDropdown && profileDropdown.classList.contains('active')) {
            if (!profileDropdown.contains(e.target) && e.target !== profileBtn) {
                closeProfileDropdown();
            }
        }
    });
    
         // Close workspace dropdown on outside click
     document.addEventListener('click', function(e) {
         const workspaceOptions = document.getElementById('workspaceOptions');
         const workspaceSelector = document.getElementById('workspaceSelector');
         
         if (workspaceOptions && workspaceOptions.classList.contains('active')) {
             if (!workspaceOptions.contains(e.target) && !workspaceSelector.contains(e.target)) {
                 console.log('Closing workspace dropdown - clicked outside');
                 workspaceOptions.classList.remove('active');
                 workspaceSelector.classList.remove('active');
                 document.getElementById('dropdownArrow').textContent = '▼';
             }
         }
     });

    // Handle escape key for mobile menu, profile dropdown, and workspace dropdown
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMobileMenu();
            closeProfileDropdown();
            
            // Close workspace dropdown
            const workspaceOptions = document.getElementById('workspaceOptions');
            const workspaceSelector = document.getElementById('workspaceSelector');
            if (workspaceOptions && workspaceOptions.classList.contains('active')) {
                workspaceOptions.classList.remove('active');
                workspaceSelector.classList.remove('active');
                document.getElementById('dropdownArrow').textContent = '▼';
            }
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