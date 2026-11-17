// TestFlow Client-Side Utilities
document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Risk Score & Badge Preview in Test Case Form
    const likelihoodInput = document.getElementById('risk_likelihood');
    const impactInput = document.getElementById('risk_impact');
    const riskPreview = document.getElementById('risk_preview');

    function updateRiskPreview() {
        if (!likelihoodInput || !impactInput || !riskPreview) return;
        const l = parseInt(likelihoodInput.value) || 1;
        const i = parseInt(impactInput.value) || 1;
        const score = l * i;

        let category = 'Low';
        let badgeClass = 'bg-success';
        if (score >= 16) {
            category = 'Critical';
            badgeClass = 'bg-danger';
        } else if (score >= 10) {
            category = 'High';
            badgeClass = 'bg-warning text-dark';
        } else if (score >= 5) {
            category = 'Medium';
            badgeClass = 'bg-info text-dark';
        }

        riskPreview.innerHTML = `
            <span class="badge ${badgeClass} fs-6">
                Score: ${score} (${category} Risk)
            </span>
            <small class="text-muted ms-2">RPN = Likelihood (${l}) &times; Impact (${i})</small>
        `;
    }

    if (likelihoodInput && impactInput) {
        likelihoodInput.addEventListener('input', updateRiskPreview);
        impactInput.addEventListener('input', updateRiskPreview);
        updateRiskPreview();
    }
});
