/**
 * SpartanSync — Portal Frontend Interactivity
 * Batangas State University Peer Tutoring Portal
 */

document.addEventListener('DOMContentLoaded', function () {
    // Auto dismiss flash messages after 6 seconds
    const toasts = document.querySelectorAll('.toast-message');
    toasts.forEach(function (toast) {
        setTimeout(function () {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.4s ease';
            setTimeout(function () {
                toast.remove();
            }, 400);
        }, 6000);
    });
});

// Modal Dialog Helpers
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Close modal on backdrop click or Escape key
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('modal-backdrop')) {
        e.target.closest('.modal-container').classList.add('hidden');
        document.body.style.overflow = '';
    }
});

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal-container');
        modals.forEach(function (m) {
            m.classList.add('hidden');
        });
        document.body.style.overflow = '';
    }
});
