function toggleMobileMenu() {
    var menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

function showLoading(msg) {
    var overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="text-center"><div class="spinner spinner-lg mb-4"></div><p class="text-dark-muted">' + (msg || 'Loading...') + '</p></div>';
    document.body.appendChild(overlay);
}

function hideLoading() {
    var overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.remove();
}

function showToast(msg, type) {
    var container = document.getElementById('flash-container');
    var toast = document.createElement('div');
    toast.className = 'flash-message ' + (type === 'error' ? 'flash-error' : 'flash-success');
    toast.innerHTML = '<span>' + msg + '</span><button onclick="this.parentElement.remove()" class="ml-auto">&times;</button>';
    container.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 5000);
}

async function copyToClipboard(text, msg) {
    try {
        await navigator.clipboard.writeText(text);
        showToast(msg || 'Copied!', 'success');
    } catch (err) {
        showToast('Failed to copy', 'error');
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    var k = 1024;
    var sizes = ['Bytes', 'KB', 'MB', 'GB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDate(dateStr) {
    var date = new Date(dateStr);
    var now = new Date();
    var diff = Math.ceil(Math.abs(now - date) / (1000 * 60 * 60 * 24));
    if (diff === 0) return 'Today';
    if (diff === 1) return 'Yesterday';
    if (diff < 7) return diff + ' days ago';
    return date.toLocaleDateString('de-CH', { year: 'numeric', month: 'short', day: 'numeric' });
}

// auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    var msgs = document.querySelectorAll('.flash-message');
    msgs.forEach(function(m) {
        setTimeout(function() { m.remove(); }, 5000);
    });

    // mark current nav link
    var path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function(link) {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });
});
