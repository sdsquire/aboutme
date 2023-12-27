document.addEventListener('DOMContentLoaded', () => {
    const scriptSrc = document.currentScript.src;
    const baseUrl = scriptSrc.substring(0, scriptSrc.lastIndexOf('/') + 1);
    fetch(baseUrl + '../header.html')
        .then(response => response.text())
        .then(data => document.getElementById('header-placeholder')
            .innerHTML = data)
        .catch(error => console.error('Error loading header:', error));
});