function openPurchaseModal(title, price) {
    // Update modal title and body for confirmation step
    document.getElementById('purchaseModalLabel').innerText = title;
    document.getElementById('purchaseModalBody').innerHTML = 
        `آیا مطمئنی که می‌خواهی قابلیت <strong>${title}</strong> را با <strong>${price} سکه</strong> بخری؟`;

    // Store item details for purchase
    document.getElementById('confirmPurchase').setAttribute('data-title', title);
    document.getElementById('confirmPurchase').setAttribute('data-price', price);

    // Reset buttons to show confirmation state
    document.getElementById('confirmPurchase').style.display = 'block';

    // Show the modal
    var purchaseModal = new bootstrap.Modal(document.getElementById('purchaseModal'));
    purchaseModal.show();
}

// Handle purchase confirmation
document.getElementById('confirmPurchase').addEventListener('click', function() {
    let title = this.getAttribute('data-title');
    let price = this.getAttribute('data-price');

    fetch('/purchase', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item: title, cost: price })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('purchaseModalBody').innerHTML = 
                `<div class="alert alert-success text-center">${data.message}</div>`;
        } else {
            document.getElementById('purchaseModalBody').innerHTML = 
                `<div class="alert alert-danger text-center">${data.message}</div>`;
        }

        // Hide "خرید" button after response
        document.getElementById('confirmPurchase').style.display = 'none';
    })
    .catch(error => {
        document.getElementById('purchaseModalBody').innerHTML = 
            `<div class="alert alert-danger text-center">خطایی رخ داد! لطفاً دوباره امتحان کنید.</div>`;
    });
});