// Walidacja formularza rejestracji
function validateRegistrationForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // Walidacja username
    if (username.length < 3) {
        showAlert('Nazwa użytkownika musi mieć co najmniej 3 znaki', 'error');
        return false;
    }
    
    // Walidacja hasła
    if (password.length < 6) {
        showAlert('Hasło musi mieć co najmniej 6 znaków', 'error');
        return false;
    }
    
    // Potwierdzenie hasła
    if (password !== confirmPassword) {
        showAlert('Hasła nie są identyczne', 'error');
        return false;
    }
    
    return true;
}

// Walidacja formularza upload zdjęć
function validateImageUpload() {
    const fileInput = document.getElementById('image-input');
    const file = fileInput.files[0];
    
    // Sprawdź czy plik został wybrany
    if (!file) {
        showAlert('Proszę wybrać plik', 'error');
        return false;
    }
    
    // Sprawdź typ pliku
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
        showAlert('Dozwolone są tylko pliki: JPG, PNG, GIF', 'error');
        return false;
    }
    
    // Sprawdź rozmiar pliku (max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        showAlert('Plik jest za duży. Maksymalny rozmiar to 5MB', 'error');
        return false;
    }
    
    return true;
}