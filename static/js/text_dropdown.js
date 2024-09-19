document.getElementById('showTextButton').addEventListener('click', function() {
    var text = document.getElementById('hiddenText');
    if (text.style.display === 'block') {
        text.style.display = 'none';
    } else {
        text.style.display = 'block';
    }
});