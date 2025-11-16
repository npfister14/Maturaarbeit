// JobTracker - Shared JavaScript Utilities

// Mobile menu toggle
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

// Show loading overlay
function showLoading(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="text-center">
            <div class="spinner spinner-lg mb-4"></div>
            <p class="text-dark-muted">${message}</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const container = document.getElementById('flash-container');
    const toast = document.createElement('div');
    toast.className = `flash-message animate-slide-down ${type === 'error' ? 'flash-error' : 'flash-success'}`;

    const icon = type === 'error'
        ? '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/>'
        : '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>';

    toast.innerHTML = `
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">${icon}</svg>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-auto">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"/>
            </svg>
        </button>
    `;

    container.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.transition = 'opacity 300ms ease-out';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Copy to clipboard (modern API)
async function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    try {
        await navigator.clipboard.writeText(text);
        showToast(successMessage, 'success');
        return true;
    } catch (err) {
        console.error('Failed to copy:', err);
        showToast('Failed to copy to clipboard', 'error');
        return false;
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Confirm dialog (modern replacement for confirm())
function confirmDialog(message, onConfirm, onCancel) {
    const dialog = document.createElement('div');
    dialog.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in';
    dialog.innerHTML = `
        <div class="bg-dark-surface border border-dark-border rounded-xl p-6 max-w-md mx-4 animate-scale-in">
            <h3 class="text-lg font-semibold mb-3">Confirm Action</h3>
            <p class="text-dark-muted mb-6">${message}</p>
            <div class="flex space-x-3 justify-end">
                <button onclick="this.closest('.fixed').remove(); ${onCancel ? 'onCancel()' : ''}" class="btn-secondary">
                    Cancel
                </button>
                <button onclick="this.closest('.fixed').remove(); ${onConfirm}()" class="btn-danger">
                    Confirm
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(dialog);
}

// Form validation helper
function validateForm(formId, rules) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;

    for (const [fieldName, validation] of Object.entries(rules)) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        const errorEl = field.parentElement.querySelector('.form-error');

        if (errorEl) errorEl.remove();

        if (validation.required && !field.value.trim()) {
            showFieldError(field, validation.message || 'This field is required');
            isValid = false;
        } else if (validation.email && !isValidEmail(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            isValid = false;
        } else if (validation.minLength && field.value.length < validation.minLength) {
            showFieldError(field, `Minimum ${validation.minLength} characters required`);
            isValid = false;
        } else if (validation.match) {
            const matchField = form.querySelector(`[name="${validation.match}"]`);
            if (field.value !== matchField.value) {
                showFieldError(field, validation.message || 'Fields do not match');
                isValid = false;
            }
        }
    }

    return isValid;
}

function showFieldError(field, message) {
    const error = document.createElement('p');
    error.className = 'form-error';
    error.textContent = message;
    field.parentElement.appendChild(error);
    field.classList.add('border-red-500');
}

// Animate elements on scroll
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(el => observer.observe(el));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Init scroll animations
    initScrollAnimations();

    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 300ms ease-out';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });

    // Add active class to current nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Handle form submissions with loading state
function handleFormSubmit(formId, loadingMessage = 'Processing...') {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', (e) => {
        showLoading(loadingMessage);
    });
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format date to readable format
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;

    return date.toLocaleDateString('de-CH', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}
