document.addEventListener('DOMContentLoaded', function() {
    const apgarForm = document.getElementById('apgarForm');
    const diagnosisForm = document.getElementById('diagnosisForm');

    apgarForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (this.checkValidity()) {
            calculateApgar();
        }
        this.classList.add('was-validated');
    });

    diagnosisForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (this.checkValidity()) {
            diagnose();
        }
        this.classList.add('was-validated');
    });

    function calculateApgar() {
        const appearance = document.getElementById('appearance').value;
        const pulse = document.getElementById('pulse').value;
        const grimace = document.getElementById('grimace').value;
        const activity = document.getElementById('activity').value;
        const respiration = document.getElementById('respiration').value;
        const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
        const payload = {
            appearance: appearance,
            pulse: pulse,
            grimace: grimace,
            activity: activity,
            respiration: respiration
        };

        fetch('/api/calculate-apgar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(payload),
        })
        .then(response => response.json())
        .then(data => {
            displayApgarResult(data);
        })
        .catch((error) => {
            console.error('Error:', error);
            displayError('An error occurred while calculating the Apgar score.');
        });
    }

    function diagnose() {
        const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
        const symptoms = Array.from(document.querySelectorAll('#diagnosisForm input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);

        if (symptoms.length === 0) {
            displayError('Please select at least one symptom.');
            return;
        }

        const payload = { symptoms: symptoms };

        fetch('/api/diagnose/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(payload),
        })
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', data); // Log the response
            displayDiagnosisResult(data);
        // .then(response => response.json())
        // .then(data => {
        //     displayDiagnosisResult(data);
        })
        .catch((error) => {
            console.error('Error:', error);
            displayError('An error occurred while diagnosing.');
        });
    }

    function displayApgarResult(data) {
        const resultDiv = document.getElementById('apgarResult');
        resultDiv.innerHTML = `
            <h3>Apgar Score Result</h3>
            <p><strong>Score [0-10]:</strong> ${data.score}</p>
            <p><strong>Assessment:</strong> ${data.assessment}</p>
            <p><strong>Action:</strong> ${data.action}</p>
        `;
    }

    function displayDiagnosisResult(data) {
        const resultDiv = document.getElementById('diagnosisResult');
        let html = '<h3>Diagnosis Results</h3>';
    
        // Check if data is an array, if not, wrap it in an array
        const diseases = Array.isArray(data) ? data : [data];
    
        if (diseases.length === 0) {
            html += '<p>No matching diseases found.</p>';
        } else {
            diseases.forEach(disease => {
                html += `
                    <div class="result-card">
                        <h4>${disease.disease} (${disease.percentage_fit}% match)</h4>
                        <p><strong>Description: </strong>${disease.description}</p>
                        <p><strong>Matched Symptoms:</strong></p>
                        <ul>
                            ${Array.isArray(disease.matched_symptoms) 
                                ? disease.matched_symptoms.map(symptom => `<li>${symptom}</li>`).join('')
                                : '<li>No matched symptoms</li>'}
                        </ul>
                        <p><strong>Treatments:</strong></p>
                        <ul>
                            ${Array.isArray(disease.treatments) 
                                ? disease.treatments.map(treatment => `<li>${treatment}</li>`).join('')
                                : '<li>No treatments specified</li>'}
                        </ul>
                        <p><strong>Preventions:</strong></p>
                        <ul>
                            ${Array.isArray(disease.preventions) 
                                ? disease.preventions.map(prevention => `<li>${prevention}</li>`).join('')
                                : '<li>No preventions specified</li>'}
                        </ul>
                    </div>
                `;
            });
        }
    
        resultDiv.innerHTML = html;
    }

    // function displayDiagnosisResult(data) {
    //     const resultDiv = document.getElementById('diagnosisResult');
    //     let html = '<h3>Diagnosis Results</h3>';

    //     data.forEach(disease => {
    //         html += `
    //             <div class="result-card">
    //                 <h4>${disease.disease} (${disease.percentage_fit}% match)</h4>
    //                 <p><strong>Matched Symptoms:</strong></p>
    //                 <ul>
    //                     ${disease.matched_symptoms.map(symptom => `<li>${symptom}</li>`).join('')}
    //                 </ul>
    //                 <p><strong>Treatments:</strong></p>
    //                 <ul>
    //                     ${disease.treatments.map(treatment => `<li>${treatment}</li>`).join('')}
    //                 </ul>
    //                 <p><strong>Preventions:</strong></p>
    //                 <ul>
    //                     ${disease.preventions.map(prevention => `<li>${prevention}</li>`).join('')}
    //                 </ul>
    //             </div>
    //         `;
    //     });

    //     resultDiv.innerHTML = html;
    // }

    function displayError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger mt-3';
        errorDiv.textContent = message;
        document.querySelector('.container').insertAdjacentElement('afterbegin', errorDiv);

        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
});