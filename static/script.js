document.getElementById('predictionForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    const resultDiv = document.getElementById('predictionResult');

    if (result.predicted_price) {
        resultDiv.innerHTML = `<strong>Predicted Price: ₹${result.predicted_price.toFixed(2)}</strong>`;
    } else {
        resultDiv.innerHTML = `<strong>Error:</strong> ${result.error}`;
    }
});
