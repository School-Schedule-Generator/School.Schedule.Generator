const fileInput = document.querySelector('.file-input');
const fileName = document.querySelector('.file-name');
const button = document.querySelector('.custom-file-input');

button.addEventListener('click', function() {
    fileInput.click(); // Otwiera domyślny wybór pliku
});

fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
    } else {
        fileName.textContent = "Nie wybrano pliku";
    }
});