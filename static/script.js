document.getElementById('bond-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/calculate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
        } else {
            resultDiv.innerHTML = `Bond Price: $${data.price}`;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<span style="color: red;">Error: ${error}</span>`;
    });
});