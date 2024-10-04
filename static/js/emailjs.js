(function () {
            emailjs.init("et5NMLxk2z_A4J3YW");
})();
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('myForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const feedback = document.getElementById("feedback").value;

        const templateParams = {
            from_name: name,
            from_email: email,
            message: feedback,
            to_name: 'Blank University',
            to_email: 'blankuniversity293@gmail.com'
        };

        emailjs.send('service_v4yoqsa', 'template_n35gxn7', templateParams)
            .then(function(response) {
                console.log('Email sent successfully!', response.status, response.text);
                alert('Feedback sent successfully!');
            }, function(error) {
                console.error('Error sending email:', error);
                alert('Failed to send feedback. Please try again later.');
            });

        document.getElementById("name").value = '';
        document.getElementById("email").value = '';
        document.getElementById("feedback").value = '';
    });
});
