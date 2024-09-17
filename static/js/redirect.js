document.addEventListener('DOMContentLoaded', function() {
    // Select the return button by its ID
    const returnButton = document.getElementById('returnButton');

    const redirectUrl = returnButton.getAttribute('data-url');

    // Add a click event listener to the button
    returnButton.addEventListener('click', function() {
        window.location.href = redirectUrl; // Redirect to the specified URL
    });
});
