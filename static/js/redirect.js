document.addEventListener('DOMContentLoaded', function() {
    const returnButton = document.getElementById('returnButton');

    const redirectUrl = returnButton.getAttribute('data-url');

    returnButton.addEventListener('click', function() {
        window.location.href = redirectUrl; // Redirect to the specified URL
    });
});
