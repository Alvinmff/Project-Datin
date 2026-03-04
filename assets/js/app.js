/**
 * BMKG Weather Intelligence - Futuristic UI JavaScript
 * External JavaScript for interactive components
 */

// ===== DOM READY =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('BMKG Weather Intelligence v2.0 - Initialized');
    
    // Initialize all components
    initAnimations();
    initTooltips();
    initSidebar();
    initCopyButtons();
    initRefreshAnimation();
});


// ===== ANIMATIONS =====
function initAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.glass-card, .metric-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Pulse animation for risk indicators
    const riskIndicators = document.querySelectorAll('[class*="risk-"]');
    riskIndicators.forEach(indicator => {
        if (indicator.classList.contains('risk-critical') || 
            indicator.classList.contains('risk-alert')) {
            indicator.classList.add('animate-pulse');
        }
    });
}


// ===== TOOLTIPS =====
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');
        const tooltip = document.createElement('span');
        tooltip.className = 'tooltiptext';
        tooltip.textContent = tooltipText;
        element.classList.add('tooltip');
        element.appendChild(tooltip);
    });
}


// ===== SIDEBAR =====
function initSidebar() {
    const navItems = document.querySelectorAll('.sidebar-nav li');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
        });
    });
    
    // Mobile sidebar toggle
    const menuToggle = document.createElement('button');
    menuToggle.className = 'mobile-menu-toggle';
    menuToggle.innerHTML = '☰';
    menuToggle.style.cssText = `
        display: none;
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1000;
        background: var(--accent-cyan);
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1.2rem;
    `;
    
    // Add mobile styles
    const style = document.createElement('style');
    style.textContent = `
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: block !important;
            }
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            .sidebar.active {
                transform: translateX(0);
            }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(menuToggle);
    
    menuToggle.addEventListener('click', function() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('active');
    });
}


// ===== COPY BUTTONS =====
function initCopyButtons() {
    // Find all copy buttons and add functionality
    const copyButtons = document.querySelectorAll('button');
    
    copyButtons.forEach(button => {
        if (button.textContent.includes('Copy') || button.textContent.includes('📋')) {
            button.addEventListener('click', function() {
                // Find associated text area or element
                const parent = this.closest('div');
                const textArea = parent ? parent.querySelector('textarea') : null;
                
                if (textArea) {
                    copyToClipboard(textArea.value);
                    showCopyFeedback(this);
                }
            });
        }
    });
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).catch(err => {
            console.error('Failed to copy:', err);
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
}

function showCopyFeedback(button) {
    const originalText = button.textContent;
    button.textContent = '✓ Copied!';
    button.style.background = 'var(--accent-green)';
    button.style.color = 'var(--bg-primary)';
    
    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
        button.style.color = '';
    }, 2000);
}


// ===== REFRESH ANIMATION =====
function initRefreshAnimation() {
    // Add refresh animation to charts
    const charts = document.querySelectorAll('[class*="chart"]');
    
    charts.forEach(chart => {
        chart.style.transition = 'opacity 0.3s ease';
    });
}

function refreshData() {
    // Show loading state
    const content = document.querySelector('.main-content');
    if (content) {
        content.style.opacity = '0.5';
        content.style.pointerEvents = 'none';
    }
    
    // Show loader
    showLoader();
    
    // Simulate refresh (actual refresh would be handled by Streamlit)
    setTimeout(() => {
        hideLoader();
        if (content) {
            content.style.opacity = '1';
            content.style.pointerEvents = 'auto';
        }
    }, 1500);
}

function showLoader() {
    let loader = document.querySelector('.data-loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.className = 'data-loader';
        loader.innerHTML = '<div class="loader"></div>';
        loader.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 9999;
            background: rgba(10, 14, 23, 0.9);
            padding: 30px;
            border-radius: 15px;
            border: 1px solid var(--accent-cyan);
        `;
        document.body.appendChild(loader);
    }
    loader.style.display = 'block';
}

function hideLoader() {
    const loader = document.querySelector('.data-loader');
    if (loader) {
        loader.style.display = 'none';
    }
}


// ===== CHART HELPERS =====
function highlightChartData(chartId, dataIndex) {
    const chart = document.getElementById(chartId);
    if (chart) {
        // Add highlight class to specific data point
        const dataPoints = chart.querySelectorAll('.point');
        dataPoints.forEach((point, index) => {
            if (index === dataIndex) {
                point.classList.add('highlighted');
            }
        });
    }
}

function exportChartAsImage(chartId, filename) {
    const chart = document.getElementById(chartId);
    if (chart) {
        // Use html2canvas or similar library for export
        console.log('Exporting chart:', chartId);
    }
}


// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    const colors = {
        'info': 'var(--accent-cyan)',
        'success': 'var(--accent-green)',
        'warning': 'var(--accent-orange)',
        'error': 'var(--accent-red)'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: var(--bg-card);
        border-left: 4px solid ${colors[type] || colors.info};
        border-radius: 5px;
        color: var(--text-primary);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}


// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R: Refresh data
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshData();
    }
    
    // Escape: Close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => modal.style.display = 'none');
    }
});


// ===== EXPORT FUNCTIONS FOR STREAMLIT =====
// These functions can be called from Python
window.BMKGApp = {
    refreshData: refreshData,
    showNotification: showNotification,
    copyToClipboard: copyToClipboard,
    showLoader: showLoader,
    hideLoader: hideLoader
};

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyles);

