document.getElementById("quiz-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission
    
    let answers = {};
    document.querySelectorAll("input[type='radio']:checked").forEach(input => {
        answers[input.name] = input.value;
    });

    fetch("/check_exam", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(answers)
    })
    .then(response => response.json())
    .then(data => {
        if (data.score > 9) {
            var successModal = new bootstrap.Modal(document.getElementById('successModal'), {
                backdrop: 'static',
                keyboard: false
            });
            successModal.show();
        } else {
            var failedModal = new bootstrap.Modal(document.getElementById('failedModal'), {
                backdrop: 'static',
                keyboard: false
            });
            failedModal.show();
        }
    });
});

document.getElementById("buyDoc").addEventListener("click", function(event) {
    var buyModal = new bootstrap.Modal(document.getElementById('buyModal'), {
        backdrop: 'static',
        keyboard: false
    });
    buyModal.show();
});