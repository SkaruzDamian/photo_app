// Obsługa formularza wysyłania zdjęć
document.addEventListener('DOMContentLoaded', function() {
    // Obsługa formularza upload
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleImageUpload);
    }

    // Obsługa przycisków admina
    const adminButtons = document.querySelectorAll('.action-buttons button');
    adminButtons.forEach(button => {
        button.addEventListener('click', handleAdminAction);
    });
});

// Funkcja obsługująca upload zdjęć
async function handleImageUpload(e) {
    e.preventDefault();
    
    const loader = document.querySelector('.loader');
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        loader.style.display = 'block';
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Zdjęcie zostało wysłane do akceptacji', 'success');
            form.reset();
        } else {
            showAlert(result.error || 'Wystąpił błąd podczas wysyłania zdjęcia', 'error');
        }
    } catch (error) {
        showAlert('Wystąpił błąd podczas wysyłania zdjęcia', 'error');
    } finally {
        loader.style.display = 'none';
    }
}

// Funkcja obsługująca akcje admina
async function handleAdminAction(e) {
    const button = e.target;
    const imageId = button.dataset.imageId;
    const action = button.dataset.action;
    
    try {
        const response = await fetch(`/admin/images/${imageId}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Usuń element z DOM po zaakceptowaniu/odrzuceniu
            const galleryItem = button.closest('.gallery-item');
            galleryItem.remove();
            
            showAlert(`Zdjęcie zostało ${action === 'approve' ? 'zaakceptowane' : 'odrzucone'}`, 'success');
        } else {
            showAlert(result.error || 'Wystąpił błąd podczas wykonywania akcji', 'error');
        }
    } catch (error) {
        showAlert('Wystąpił błąd podczas wykonywania akcji', 'error');
    }
}

// Funkcja wyświetlająca komunikaty
function showAlert(message, type) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type}`;
    alertContainer.textContent = message;
    
    document.body.insertBefore(alertContainer, document.body.firstChild);
    
    // Usuń alert po 3 sekundach
    setTimeout(() => {
        alertContainer.remove();
    }, 3000);
}

// Funkcja podglądu zdjęcia przed wysłaniem
function previewImage(input) {
    const preview = document.getElementById('image-preview');
    const file = input.files[0];
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        
        reader.readAsDataURL(file);
    }
}

// Dynamiczne ładowanie zdjęć (lazy loading)
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.gallery img');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
});